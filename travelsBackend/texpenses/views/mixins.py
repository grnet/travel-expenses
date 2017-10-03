from rest_framework import permissions, status
from django.db import transaction
from django.core.exceptions import PermissionDenied
from django.conf import settings

from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response

from rest_framework.reverse import reverse
from texpenses.models import Petition, UserPetitionSubmission, UserPetition,\
    SecretaryPetition, SecretaryPetitionSubmission, UserCompensation,\
    SecretaryCompensation, City, Project
from texpenses.actions import inform_on_action
from texpenses.views.utils import render_template2pdf, render_template2csv
from texpenses.views import utils


class CityMixin(object):

    def get_queryset(self):
        return City.objects.select_related('country').all()


class ProjectMixin(object):

    def _extract_info(self, petition):
        petition_info = {}

        # user info
        petition_info.update({'first_name': petition.first_name,
                              'last_name': petition.last_name,
                              'kind': petition.get_kind_display(),
                              'specialty': petition.get_specialty_display()
                              })
        # petition info
        travel_info = petition.travel_info.all()
        travel_info_first = travel_info[0]
        travel_info_last = travel_info[len(travel_info) - 1]
        petition_info.update({'depart_date': travel_info_first.depart_date.
                              strftime(settings.DATE_FORMAT),
                              'return_date': travel_info_last.return_date.
                              strftime(settings.DATE_FORMAT),
                              'task_start_date': petition.task_start_date.
                              strftime(settings.DATE_FORMAT),
                              'task_end_date': petition.task_end_date.
                              strftime(settings.DATE_FORMAT),
                              'transport_days': petition.transport_days(),
                              'overnights_num': petition.overnights_num(),
                              'departure_point':
                              travel_info_first.departure_point.name,
                              'is_abroad': travel_info_last.is_abroad(),
                              'arrival_point':
                              travel_info_last.arrival_point.name,
                              'transportation_cost':
                              utils.get_transportation_cost(travel_info),
                              'transportation_default_currency':
                              travel_info_first.
                              transportation_default_currency,
                              'overnights_sum_cost':
                              petition.overnights_sum_cost(),
                              'accommodation_default_currency':
                              travel_info_first.
                              accommodation_default_currency,
                              'participation_cost':
                              petition.participation_cost,
                              'participation_default_currency': petition.
                              participation_default_currency,
                              'additional_expenses_initial': petition.
                              additional_expenses_initial,
                              'additional_expenses_default_currency':
                              petition.additional_expenses_default_currency,
                              'additional_expenses':
                              petition.additional_expenses,
                              'total_cost': petition.total_cost(),
                              'project': petition.project.name,
                              'compensation_cost':
                              utils.get_compensation_cost(travel_info)
                              })
        return petition_info

    def _get_related_petitions(self, project_name=None, format='csv'):
        petitions = SecretaryCompensation.objects.filter(
            project__name=project_name) if project_name else \
            SecretaryCompensation.objects.all()
        data = []

        for petition in petitions:
            data.append(self._extract_info(petition))

        return {'petitions': data} if format == 'csv' else data

    @detail_route(methods=['get'])
    def project_stats(self, request, pk=None):
        template_path = "project_stats.csv"
        project = self.get_object()
        project_name = project.name
        data = self._get_related_petitions(project_name)
        return render_template2csv(data, template_path, project_name + '_stats')

    @list_route()
    def stats(self, request):

        response_format = self.request.query_params.get(
            'response_format', 'json')
        data = self._get_related_petitions(format=response_format)

        if response_format == 'csv':
            data = self._get_related_petitions()
            template_path = "project_stats.csv"
            return render_template2csv(data, template_path, 'all_project_stats')
        else:
            return Response(data)

    def get_queryset(self):
        return Project.objects.filter(active=True)


class UserPetitionMixin(object):

    @transaction.atomic
    def update(self, request, pk=None, **kwargs):
        return super(UserPetitionMixin, self).update(request, pk, **kwargs)

    @transaction.atomic
    def destroy(self, request, pk=None):
        return super(UserPetitionMixin, self).destroy(request, pk)

    def get_queryset(self):
        non_atomic_requests = permissions.SAFE_METHODS
        query = UserPetition.objects.select_related('tax_office', 'user',
                                                    'project').\
            filter(user=self.request.user)
        if self.request.method in non_atomic_requests:
            return query
        else:
            return query.select_for_update(nowait=True)


class UserPetitionSubmissionMixin(object):

    @detail_route(methods=['post'])
    @transaction.atomic
    @inform_on_action('CANCELLATION')
    def cancel(self, request, pk=None):
        submitted = self.get_object()
        try:
            petition_id = submitted.status_rollback()
            headers = {'location': reverse('api_petition-user-saved-detail',
                                           args=[petition_id])}
            return Response(headers=headers, status=status.HTTP_303_SEE_OTHER)
        except PermissionDenied as e:
            return Response({'detail': e.message},
                            status=status.HTTP_403_FORBIDDEN)

    @inform_on_action('SUBMISSION')
    def create(self, request, *args, **kwargs):
        return super(UserPetitionSubmissionMixin, self).create(request,
                                                               *args,
                                                               **kwargs)

    def get_queryset(self):
        non_atomic_requests = permissions.SAFE_METHODS
        query = UserPetitionSubmission.objects.select_related('tax_office',
                                                              'user',
                                                              'project').\
            filter(user=self.request.user)
        if self.request.method in non_atomic_requests:
            return query
        else:
            return query.select_for_update(nowait=True)


class SecretaryPetitionSaveMixin(object):

    @transaction.atomic
    def update(self, request, pk=None, **kwargs):
        return super(SecretaryPetitionSaveMixin, self).update(request, pk,
                                                              **kwargs)

    @transaction.atomic
    def destroy(self, request, pk=None):
        return super(SecretaryPetitionSaveMixin, self).destroy(request, pk)

    def get_queryset(self):
        non_atomic_requests = permissions.SAFE_METHODS
        query = SecretaryPetition.objects.select_related('tax_office', 'user',
                                                         'project')
        user = self.request.user
        if user.user_group() == "MANAGER":
            manager_projects = Project.objects.filter(manager=user)
            query = query.filter(project__in=manager_projects,
                                 manager_movement_approval=False)
        else:
            query = query.all()

        if self.request.method in non_atomic_requests:
            return query
        else:
            return query.select_for_update(nowait=True)

    def _extract_info(self, petition_object):
        data = {}

        # user info
        data.update({'first_name': petition_object.first_name,
                     'last_name': petition_object.last_name,
                     'kind': petition_object.get_kind_display(),
                     'specialty': petition_object.get_specialty_display(),
                     'iban': petition_object.iban,
                     'tax_reg_num': petition_object.tax_reg_num
                     })
        # petition info
        travel_info_first = petition_object.travel_info.first()
        travel_info_last = petition_object.travel_info.last()

        data.update({'depart_date': travel_info_first.depart_date,
                     'return_date': travel_info_last.return_date,
                     'task_start_date': petition_object.task_start_date,
                     'task_end_date': petition_object.task_end_date,
                     'reason': petition_object.reason,
                     'departure_point': travel_info_first.departure_point.name,
                     'arrival_point': travel_info_last.arrival_point.name,
                     'project': petition_object.project.name
                     })
        return data

    @detail_route(methods=['get'])
    def export_csv(self, request, pk=None):
        template_path = "petition.csv"
        petition = self.get_object()
        data = self._extract_info(petition)
        return render_template2csv(data, template_path)


class SecretaryPetitionSubmissionMixin(object):

    @detail_route(methods=['post'])
    @transaction.atomic
    def cancel(self, request, pk=None):
        submitted = self.get_object()
        try:
            petition_id = submitted.status_rollback()
            headers = {'location': reverse(
                'api_petition-secretary-saved-detail',
                args=[petition_id])}
            return Response(headers=headers, status=status.HTTP_303_SEE_OTHER)
        except PermissionDenied as e:
            return Response({'detail': e.message},
                            status=status.HTTP_403_FORBIDDEN)

    @detail_route(methods=['get'])
    def export_csv(self, request, pk=None):
        template_path = "petition.csv"
        petition = self.get_object()
        data = self._extract_info(petition)
        return render_template2csv(data, template_path)

    @detail_route(methods=['post'])
    @transaction.atomic
    @inform_on_action('PETITION_PRESIDENT_APPROVAL', target_user=True,
                      inform_controller=True)
    def president_approval(self, request, pk=None):

        petition = self.get_object()
        ACCEPTED_STATUS = petition.SUBMITTED_BY_SECRETARY
        try:
            if petition.status is ACCEPTED_STATUS:
                petition.proceed(delete=True)
                return Response({'message':
                                 'The petition is approved by the president'},
                                status=status.HTTP_200_OK)
            return Response(status=status.HTTP_501_NOT_IMPLEMENTED)

        except PermissionDenied as e:
            return Response({'detail': e.message},
                            status=status.HTTP_403_FORBIDDEN)

    def _extract_info(self, petition_object):
        data = {}

        # protocol info
        data.update(
            {'dse': petition_object.dse,
             'movement_id': petition_object.movement_id,
             'movement_date_protocol': petition_object.movement_date_protocol,
             'movement_protocol': petition_object.movement_protocol,
             'expenditure_protocol': petition_object.expenditure_protocol,
             'expenditure_date_protocol':
             petition_object.expenditure_date_protocol,

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
        travel_info = petition_object.travel_info.all()
        travel_info_first = petition_object.travel_info.first()
        travel_info_last = petition_object.travel_info.last()
        data.update({'depart_date': travel_info_first.depart_date,
                     'return_date': travel_info_last.return_date,
                     'travel_info': travel_info,
                     'task_start_date': petition_object.task_start_date,
                     'task_end_date': petition_object.task_end_date,
                     'trip_days_before': petition_object.trip_days_before,
                     'trip_days_after': petition_object.trip_days_after,
                     'transport_days': petition_object.transport_days,
                     'overnights_num': petition_object.overnights_num,
                     'reason': petition_object.reason,
                     'departure_point': travel_info_first.departure_point.name,
                     'arrival_point': travel_info_last.arrival_point.name,
                     'means_of_transport': \
                     utils.get_means_of_transport(travel_info),
                     'transportation_cost': \
                     utils.get_transportation_cost(travel_info),
                     'transportation_default_currency': \
                     travel_info_first.transportation_default_currency,
                     'overnights_sum_cost_string': \
                     utils.get_overnights_sum_cost_string(travel_info),
                     'overnights_sum_cost':
                     petition_object.overnights_sum_cost,
                     'accommodation_default_currency':\
                     travel_info_first.accommodation_default_currency,
                     'participation_cost': petition_object.participation_cost,
                     'participation_default_currency': petition_object.
                     participation_default_currency,
                     'additional_expenses_initial': petition_object.
                     additional_expenses_initial,
                     'additional_expenses_default_currency': petition_object.
                     additional_expenses_default_currency,
                     'total_cost': petition_object.total_cost,
                     'project': petition_object.project.name,
                     'compensation_string' :
                     utils.get_compensation_levels_string(travel_info),
                     'compensation_cost': \
                     utils.get_compensation_cost(travel_info)
                     })
        return data

    @detail_route(methods=['get'])
    def application_report(self, request, pk=None):
        template_path = "texpenses/movement_petition_application/" +\
            "movement_petition_application.html"
        report_name = 'petition_application_report.pdf'
        petition = self.get_object()
        data = self._extract_info(petition)
        return render_template2pdf(request, data, template_path, report_name)

    @detail_route(methods=['get'])
    def decision_report(self, request, pk=None):
        template_path = "texpenses/movement_petition_decision/" +\
            "movement_petition_decision.html"
        report_name = 'petition_decision_report.pdf'

        petition = self.get_object()
        data = self._extract_info(petition)
        return render_template2pdf(request, data, template_path, report_name)

    def get_queryset(self):
        non_atomic_requests = permissions.SAFE_METHODS
        query = SecretaryPetitionSubmission.objects.\
            select_related('tax_office', 'user', 'project').\
            prefetch_related('travel_info').all()
        if self.request.method in non_atomic_requests:
            return query
        else:
            return query.select_for_update(nowait=True)


class UserCompensationMixin(object):

    VIEW_NAMES = {
        Petition.USER_COMPENSATION: 'api_petition-user-compensations-detail',
        Petition.USER_COMPENSATION_SUBMISSION: "api_petition-user-compensations-"
        "detail"
    }

    @transaction.atomic
    def update(self, request, pk=None, **kwargs):
        return super(UserCompensationMixin, self).update(request, pk, **kwargs)

    @transaction.atomic
    def destroy(self, request, pk=None):
        return super(UserCompensationMixin, self).destroy(request, pk)

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
    @transaction.atomic
    @inform_on_action('USER_COMPENSATION_SUBMISSION', inform_controller=True)
    def submit(self, request, pk=None):
        instance = self.get_object()
        petition_id = instance.proceed()
        headers = {'location': reverse(
            self.VIEW_NAMES[instance.status], args=[petition_id])}
        instance.set_trip_days_left()
        return Response(status=status.HTTP_303_SEE_OTHER, headers=headers)

    @detail_route(methods=['post'])
    @transaction.atomic
    @inform_on_action('USER_COMPENSATION_CANCELLATION', inform_controller=True)
    def cancel(self, request, pk=None):
        submitted = self.get_object()
        try:
            petition_id = submitted.revoke()
            headers = {'location': reverse(self.VIEW_NAMES[submitted.status],
                                           args=[petition_id])}
            return Response(headers=headers, status=status.HTTP_303_SEE_OTHER)
        except PermissionDenied as e:
            return Response({'detail': e.message},
                            status=status.HTTP_403_FORBIDDEN)

    def get_queryset(self):
        non_atomic_requests = permissions.SAFE_METHODS
        query = UserCompensation.objects.select_related('tax_office',
                                                        'user',
                                                        'project').\
            filter(user=self.request.user)

        if self.request.method in non_atomic_requests:
            return query
        else:
            return query.select_for_update(nowait=True)
        pass

    def _extract_info(self, petition_object):
        data = {}

        # protocol info
        data.update(
            {'dse': petition_object.dse,
             'movement_id': petition_object.movement_id,
             'movement_date_protocol': petition_object.movement_date_protocol,
             'movement_protocol': petition_object.movement_protocol,
             'expenditure_protocol': petition_object.expenditure_protocol,
             'expenditure_date_protocol':
             petition_object.expenditure_date_protocol,

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
        travel_info = petition_object.travel_info.all()
        travel_info_first = petition_object.travel_info.first()
        travel_info_last = petition_object.travel_info.last()
        data.update({'depart_date': travel_info_first.depart_date,
                     'return_date': travel_info_last.return_date,
                     'travel_info': travel_info,
                     'task_start_date': petition_object.task_start_date,
                     'task_end_date': petition_object.task_end_date,
                     'trip_days_before': petition_object.trip_days_before,
                     'trip_days_after': petition_object.trip_days_after,
                     'transport_days': petition_object.transport_days,
                     'overnights_num': petition_object.overnights_num,
                     'reason': petition_object.reason,
                     'departure_point': travel_info_first.departure_point.name,
                     'arrival_point': travel_info_last.arrival_point.name,
                     'means_of_transport':\
                     utils.get_means_of_transport(travel_info),
                     'transportation_cost': \
                     utils.get_transportation_cost(travel_info),
                     'transportation_default_currency': \
                     travel_info_first.transportation_default_currency,
                     'overnights_sum_cost_string': \
                     utils.get_overnights_sum_cost_string(travel_info),
                     'overnights_sum_cost':
                     petition_object.overnights_sum_cost,
                     'accommodation_default_currency': \
                     travel_info_first.accommodation_default_currency,
                     'participation_cost': petition_object.participation_cost,
                     'participation_default_currency': petition_object.
                     participation_default_currency,
                     'additional_expenses_initial': petition_object.
                     additional_expenses_initial,
                     'additional_expenses_default_currency': petition_object.
                     additional_expenses_default_currency,
                     'total_cost': petition_object.total_cost,
                     'project': petition_object.project.name,
                     'compensation_string' :
                     utils.get_compensation_levels_string(travel_info),
                     'compensation_cost':\
                     utils.get_compensation_cost(travel_info)
                     })
        return data

    @detail_route(methods=['get'])
    def application_report(self, request, pk=None):
        template_path = "texpenses/movement_petition_application/" +\
            "movement_petition_application.html"
        report_name = 'petition_application_report.pdf'
        petition = self.get_object()
        data = self._extract_info(petition)
        return render_template2pdf(request, data, template_path, report_name)


class SecretaryCompensationMixin(object):

    VIEW_NAMES = {
        Petition.SECRETARY_COMPENSATION: "api_petition-secretary-"
        "compensations-detail",
        Petition.SECRETARY_COMPENSATION_SUBMISSION: "api_petition-secretary-"
        "compensations-detail",
    }

    @transaction.atomic
    def update(self, request, pk=None, **kwargs):
        return super(SecretaryCompensationMixin, self).update(request, pk,
                                                              **kwargs)

    @transaction.atomic
    def destroy(self, request, pk=None):
        return super(SecretaryCompensationMixin, self).destroy(request, pk)

    def get_queryset(self):
        non_atomic_requests = permissions.SAFE_METHODS
        query = SecretaryCompensation.objects.\
            select_related('tax_office', 'user', 'project').\
            prefetch_related('travel_info').all()
        if self.request.method in non_atomic_requests:
            return query
        else:
            return query.select_for_update(nowait=True)

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
    @transaction.atomic
    def submit(self, request, pk=None):
        instance = self.get_object()
        petition_id = instance.proceed()
        headers = {'location': reverse(
            self.VIEW_NAMES[instance.status], args=[petition_id])}
        return Response(status=status.HTTP_303_SEE_OTHER, headers=headers)

    @detail_route(methods=['post'])
    @transaction.atomic
    @inform_on_action('COMPENSATION_PRESIDENT_APPROVAL', target_user=True,
                      inform_controller=True)
    def president_approval(self, request, pk=None):

        petition = self.get_object()
        ACCEPTED_STATUS = petition.SECRETARY_COMPENSATION_SUBMISSION
        try:
            if petition.status is ACCEPTED_STATUS:
                petition.proceed(delete=True)
                return Response({'message':
                                 'The petition is approved by the president'},
                                status=status.HTTP_200_OK)
            return Response(status=status.HTTP_501_NOT_IMPLEMENTED)

        except PermissionDenied as e:
            return Response({'detail': e.message},
                            status=status.HTTP_403_FORBIDDEN)

    @detail_route(methods=['post'])
    @transaction.atomic
    @inform_on_action('CANCELLATION', inform_controller=True)
    def cancel(self, request, pk=None):
        submitted = self.get_object()
        try:
            petition_id = submitted.status_rollback()
            headers = {'location': reverse(self.VIEW_NAMES[submitted.status],
                                           args=[petition_id])}
            return Response(headers=headers, status=status.HTTP_303_SEE_OTHER)
        except PermissionDenied as e:
            return Response({'detail': e.message},
                            status=status.HTTP_403_FORBIDDEN)

    def _extract_info(self, petition_object):
        data = {}

        # protocol info
        data.update(
            {'dse': petition_object.dse,
             'movement_id': petition_object.movement_id,
             'compensation_petition_protocol':
             petition_object.compensation_petition_protocol,
             'compensation_petition_date':
             petition_object.compensation_petition_date,
             'compensation_decision_protocol':
             petition_object.compensation_decision_protocol,
             'compensation_decision_date':
             petition_object.compensation_decision_date
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
        travel_info = petition_object.travel_info.all()
        travel_info_first = petition_object.travel_info.first()
        travel_info_last = petition_object.travel_info.last()
        data.update({'depart_date': travel_info_first.depart_date,
                     'travel_info': travel_info,
                     'return_date': travel_info_last.return_date,
                     'task_start_date': petition_object.task_start_date,
                     'task_end_date': petition_object.task_end_date,
                     'trip_days_before': petition_object.trip_days_before,
                     'trip_days_after': petition_object.trip_days_after,
                     'transport_days': petition_object.transport_days,
                     'overnights_num': petition_object.overnights_num,
                     'reason': petition_object.reason,
                     'departure_point': travel_info_first.departure_point.name,
                     'arrival_point': travel_info_last.arrival_point.name,
                     'means_of_transport': \
                     utils.get_means_of_transport(travel_info),
                     'transportation_cost': \
                     utils.get_transportation_cost(travel_info),
                     'transportation_default_currency': \
                     travel_info_first.transportation_default_currency,
                     'overnights_sum_cost_string': \
                     utils.get_overnights_sum_cost_string(travel_info),
                     'overnights_sum_cost':
                     petition_object.overnights_sum_cost,
                     'accommodation_default_currency': \
                     travel_info_first.accommodation_default_currency,
                     'participation_cost': petition_object.participation_cost,
                     'participation_default_currency': petition_object.
                     participation_default_currency,
                     'compensation_days_num':
                     petition_object.compensation_days_num,
                     'additional_expenses_initial': petition_object.
                     additional_expenses_initial,
                     'additional_expenses_default_currency': petition_object.
                     additional_expenses_default_currency,
                     'total_cost': petition_object.total_cost,
                     'project': petition_object.project.name,
                     'compensation_string':
                     utils.get_compensation_levels_string(travel_info),
                     'compensation_cost':
                     utils.get_compensation_cost(travel_info),
                     'additional_expenses':
                     petition_object.additional_expenses,
                     'additional_expenses_local_currency':
                     petition_object.additional_expenses_local_currency,
                     'compensation_final': petition_object.compensation_final,
                     'transportation_compensation':
                     petition_object.tranportation_cost_to_be_compensated()
                     })
        return data

    @detail_route(methods=['get'])
    def application_report(self, request, pk=None):
        petition = self.get_object()
        petition_status = petition.status

        if petition_status is Petition.SECRETARY_COMPENSATION_SUBMISSION:
            template_path = "texpenses/movement_compensation_application/" +\
                "movement_compensation_application.html"
            report_name = 'compensation_application_report.pdf'

            petition = self.get_object()
            data = self._extract_info(petition)
            return render_template2pdf(request, data, template_path,
                                       report_name)

        return Response(status=status.HTTP_501_NOT_IMPLEMENTED)

    @detail_route(methods=['get'])
    def decision_report(self, request, pk=None):
        petition = self.get_object()
        petition_status = petition.status

        if petition_status is Petition.SECRETARY_COMPENSATION_SUBMISSION:
            template_path = "texpenses/movement_compensation_decision/" +\
                "movement_compensation_decision.html"
            report_name = 'compensation_decision_report.pdf'

            petition = self.get_object()
            data = self._extract_info(petition)
            return render_template2pdf(request, data, template_path,
                                       report_name)
        return Response(status=status.HTTP_501_NOT_IMPLEMENTED)
