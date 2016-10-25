from django.core.exceptions import PermissionDenied
from django.db import transaction

from rest_framework import status
from rest_framework.decorators import detail_route
from rest_framework.reverse import reverse
from rest_framework.response import Response
from texpenses.models import Petition, SecretaryCompensation
from texpenses.actions import inform_on_action

from django.template.loader import get_template
from django.template import RequestContext
from django.http import HttpResponse
from weasyprint import HTML


EXPOSED_METHODS = ['submit', 'save', 'cancel', 'application_report',
                   'decision_report', '_extract_application_info',
                   '_render_template2pdf', 'president_approval',
                   'get_queryset']


VIEW_NAMES = {
    Petition.SECRETARY_COMPENSATION: 'secretarycompensation-detail',
    Petition.SECRETARY_COMPENSATION_SUBMISSION: 'secretarycompensation-detail',
}


def get_queryset(self):
    non_atomic_requests = ('GET', 'HEAD', 'OPTIONS', 'POST')
    if self.request.method in non_atomic_requests:
        return SecretaryCompensation.objects.\
            select_related('tax_office', 'user', 'project').\
            prefetch_related('travel_info').all()
    else:
        return SecretaryCompensation.objects.select_for_update(nowait=True).\
            select_related('tax_office', 'user', 'project').\
            prefetch_related('travel_info').all()


@detail_route(methods=['post'])
@transaction.atomic
def save(self, request, pk=None):
    instance = self.get_object()
    serializer = self.get_serializer(instance, data=request.data)
    serializer.is_valid(raise_exception=True)
    try:
        serializer.proceed(instance)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, headers=headers)
    except PermissionDenied as e:
        return Response({'detail': e.message},
                        status=status.HTTP_403_FORBIDDEN)


@detail_route(methods=['post'])
def submit(self, request, pk=None):
    instance = self.get_object()
    petition_id = instance.proceed()
    headers = {'location': reverse(
        VIEW_NAMES[instance.status], args=[petition_id])}
    return Response(status=status.HTTP_303_SEE_OTHER, headers=headers)


@detail_route(methods=['post'])
@inform_on_action('COMPENSATION_PRESIDENT_APPROVAL', target_user=True)
def president_approval(self, request, pk=None):

    petition = self.get_object()
    ACCEPTED_STATUS = petition.SECRETARY_COMPENSATION_SUBMISSION
    try:
        if petition.status is ACCEPTED_STATUS:
            petition.proceed(delete=True)
            petition.set_trip_days_left()
            return Response({'message':
                             'The petition is approved by the president'},
                            status=status.HTTP_200_OK)
        return Response(status=status.HTTP_501_NOT_IMPLEMENTED)

    except PermissionDenied as e:
        return Response({'detail': e.message}, status=status.HTTP_403_FORBIDDEN)


@detail_route(methods=['post'])
@inform_on_action('CANCELLATION')
@transaction.atomic
def cancel(self, request, pk=None):
    submitted = self.get_object()
    try:
        petition_id = submitted.revoke()
        headers = {'location': reverse(VIEW_NAMES[submitted.status],
                                       args=[petition_id])}
        return Response(headers=headers, status=status.HTTP_303_SEE_OTHER)
    except PermissionDenied as e:
        return Response({'detail': e.message},
                        status=status.HTTP_403_FORBIDDEN)


def _extract_info(petition_object):
    data = {}

    # protocol info
    data.update(
        {'dse': petition_object.dse,
         'movement_id': petition_object.movement_id,
         'movement_date_protocol': petition_object.movement_date_protocol,
         'movement_protocol': petition_object.movement_protocol
         }
    )

    # user info
    data.update({'first_name': petition_object.first_name,
                 'last_name': petition_object.last_name,
                 'kind': petition_object.get_kind_display(),
                 'specialty': petition_object.get_specialty_display(),
                 'iban': petition_object.iban,
                 'tax_reg_num': petition_object.tax_reg_num
                 })
    # petition info
    travel_info = petition_object.travel_info.all()[0]
    data.update({'depart_date': travel_info.depart_date,
                 'return_date': travel_info.return_date,
                 'task_start_date': petition_object.task_start_date,
                 'task_end_date': petition_object.task_end_date,
                 'trip_days_before': petition_object.trip_days_before,
                 'trip_days_after': petition_object.trip_days_after,
                 'transport_days': petition_object.transport_days,
                 'overnights_num': petition_object.overnights_num,
                 'reason': petition_object.reason,
                 'departure_point': travel_info.departure_point.name,
                 'arrival_point': travel_info.arrival_point.name,
                 'means_of_transport': travel_info.
                 get_means_of_transport_display(),
                 'transportation_cost': travel_info.transportation_cost,
                 'transportation_default_currency': travel_info.
                 transportation_default_currency,
                 'overnights_num_manual': travel_info.overnights_num_manual,
                 'accommodation_cost': travel_info.accommodation_cost,
                 'overnights_sum_cost': petition_object.overnights_sum_cost,
                 'accommodation_default_currency': travel_info.
                 accommodation_default_currency,
                 'participation_cost': petition_object.participation_cost,
                 'participation_default_currency': petition_object.
                 participation_local_currency,
                 'additional_expenses_initial': petition_object.
                 additional_expenses_initial,
                 'additional_expenses_default_currency': petition_object.
                 additional_expenses_default_currency,
                 'total_cost': petition_object.total_cost,
                 'project': petition_object.project.name,
                 'compensation_days_manual': travel_info.
                 compensation_days_manual,
                 'compensation_level': travel_info.compensation_level(),
                 'compensation_cost': travel_info.compensation_cost(),
                 'additional_expenses': petition_object.additional_expenses,
                 'additional_expenses_local_currency':
                 petition_object.additional_expenses_local_currency,
                 'compensation_final': petition_object.compensation_final
                 })
    return data


def _render_template2pdf(self, request, template_path,
                         default_report_name='report.pdf'):
    petition = self.get_object()

    html_template = get_template(template_path)

    rendered_html = html_template.render(
        RequestContext(request, _extract_info(petition))).\
        encode(encoding="UTF-8")
    pdf_file = HTML(string=rendered_html,
                    base_url=request.build_absolute_uri()).write_pdf()

    http_response = HttpResponse(pdf_file, content_type='application/pdf')
    http_response['Content-Disposition'] = 'filename="' +\
        default_report_name + '"'
    return http_response


@detail_route(methods=['get'])
def application_report(self, request, pk=None):
    petition = self.get_object()
    petition_status = petition.status

    if petition_status is Petition.SECRETARY_COMPENSATION_SUBMISSION:
        template_path = "texpenses/movement_compensation_application/" +\
            "movement_compensation_application.html"
        report_name = 'compensation_application_report.pdf'

        return self._render_template2pdf(
            request, template_path, report_name)

    return Response(status=status.HTTP_501_NOT_IMPLEMENTED)


@detail_route(methods=['get'])
def decision_report(self, request, pk=None):
    petition = self.get_object()
    petition_status = petition.status

    if petition_status is Petition.SECRETARY_COMPENSATION_SUBMISSION:
        template_path = "texpenses/movement_compensation_decision/" +\
            "movement_compensation_decision.html"
        report_name = 'compensation_decision_report.pdf'

        return self._render_template2pdf(
            request, template_path, report_name)
    return Response(status=status.HTTP_501_NOT_IMPLEMENTED)
