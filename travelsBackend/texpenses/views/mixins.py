from rest_framework import permissions, status
from django.db import transaction
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.conf import settings

from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response

from rest_framework.reverse import reverse
from texpenses.models import Petition, City, Project, Applications
from texpenses.actions import inform_on_action, inform
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
                              'total_cost': petition.total_cost_calculated,
                              'project': petition.project.name,
                              'compensation_cost':
                              utils.get_compensation_cost(travel_info)
                              })
        return petition_info

    def _get_related_petitions(self, project_name=None, format='csv'):

        query = Applications.objects.filter(
            Q(status__gte=Petition.USER_COMPENSATION_SUBMISSION) &
            Q(status__lte=Petition.PETITION_FINAL_APPOVAL)
        )

        petitions =  query.filter(
            project__name=project_name) if project_name else (query)

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


class ApplicationMixin(object):

    @transaction.atomic
    def update(self, request, pk=None, **kwargs):
        return super(ApplicationMixin, self).update(request, pk, **kwargs)

    @transaction.atomic
    def destroy(self, request, pk=None):
        return super(ApplicationMixin, self).destroy(request, pk)

    def create(self, request, *args, **kwargs):
        return super(ApplicationMixin, self).create(request, *args, **kwargs)

    @detail_route(methods=['post'])
    @transaction.atomic
    @inform_on_action('PETITION_WITHDRAWAL', target_user=True,
                      inform_controller=True)
    def withdraw(self, request, pk=None):

        application = self.get_object()
        try:
            application.withdraw()
            return Response({'message': 'The application is withdrawn'},
                            status=status.HTTP_200_OK)

        except PermissionDenied as e:
            return Response({'detail': e.message},
                            status=status.HTTP_403_FORBIDDEN)

    @detail_route(methods=['post'])
    @transaction.atomic
    @inform_on_action('CANCEL_PETITION_WITHDRAWAL', target_user=False,
                      inform_controller=True)
    def cancel_withdrawal(self, request, pk=None):

        application = self.get_object()
        try:
            if application.status < application.SECRETARY_COMPENSATION:
                application.cancel_withdrawal()
            else:
                application.cancel_withdrawal(roll_back=True)
            return Response({'message': 'The petition withdrawal is cancelled'},
                            status=status.HTTP_200_OK)

        except PermissionDenied as e:
            return Response({'detail': e.message},
                            status=status.HTTP_403_FORBIDDEN)


    @detail_route(methods=['post'])
    @transaction.atomic
    def cancel(self, request, pk=None):
        application = self.get_object()
        application_status = application.status
        try:
            if application.status in (
                Petition.SECRETARY_COMPENSATION_SUBMISSION,
                Petition.PETITION_FINAL_APPOVAL):
                application_id = application.status_rollback()
            else:
                application_id = application.revoke()

            per_status_email_confs = {
                Petition.SUBMITTED_BY_USER: [
                    application, 'CANCELLATION', False, False, request.user],
                Petition.USER_COMPENSATION_SUBMISSION: [
                    application, 'USER_COMPENSATION_CANCELLATION',
                    False, True, request.user],
                Petition.SECRETARY_COMPENSATION_SUBMISSION: [
                    application, 'CANCELLATION', False, True, request.user],
            }
            email_args = per_status_email_confs.get(application_status, None)

            if email_args:
                inform(*email_args)

            headers = {'location': reverse('api_applications-detail',
                                           args=[application_id])}
            return Response(headers=headers, status=status.HTTP_303_SEE_OTHER)
        except PermissionDenied as e:
            return Response({'detail': e.message},
                            status=status.HTTP_403_FORBIDDEN)

    @detail_route(methods=['post'])
    @transaction.atomic
    def submit(self, request, pk=None):
        application = self.get_object()

        application_id = application.proceed()
        application_status = application.status

        if application_status == Petition.USER_COMPENSATION:
            application.set_trip_days_left()

        per_status_email_confs = {
            Petition.SUBMITTED_BY_USER: [
                application, 'SUBMISSION', False, False, request.user],
            Petition.USER_COMPENSATION: [
                application, 'USER_COMPENSATION_SUBMISSION',
                False, True, request.user]
        }
        email_args = per_status_email_confs.get(application_status, None)

        if email_args:
            inform(*email_args)

        headers = {'location': reverse('api_applications-detail',
                                       args=[application_id])}
        return Response(status=status.HTTP_303_SEE_OTHER, headers=headers)

    @detail_route(methods=['post'])
    @transaction.atomic
    def president_approval(self, request, pk=None):

        application = self.get_object()
        application_status = application.status
        ACCEPTED_STATUSES = (Petition.SUBMITTED_BY_SECRETARY,
                             Petition.SECRETARY_COMPENSATION_SUBMISSION)
        try:
            if application_status in ACCEPTED_STATUSES:
                if not application.withdrawn:
                    application.proceed(delete=True)
                else:
                    application.withdraw(proceed=True)

                per_status_email_confs = {
                    Petition.SUBMITTED_BY_SECRETARY: [
                        application, 'PETITION_PRESIDENT_APPROVAL',
                        True, True, request.user],
                    Petition.SECRETARY_COMPENSATION_SUBMISSION: [
                        application, 'COMPENSATION_PRESIDENT_APPROVAL',
                        True, True, request.user]
                }
                email_args = per_status_email_confs[application_status]

                inform(*email_args)

                return Response(
                    {'message': 'The application is approved by the president'},
                    status=status.HTTP_200_OK)
            return Response(status=status.HTTP_501_NOT_IMPLEMENTED)

        except PermissionDenied as e:
            return Response({'detail': e.message},
                            status=status.HTTP_403_FORBIDDEN)

    @detail_route(methods=['get'])
    def application_report(self, request, pk=None):
        petition = self.get_object()
        petition_status = petition.status


        template_info = {
            Petition.SUBMITTED_BY_SECRETARY: {
                'template_path': "texpenses/movement_petition_application/"+\
                "movement_petition_application.html",
                'report_name': 'petition_application_report.pdf'},

            Petition.SECRETARY_COMPENSATION_SUBMISSION: {
                'template_path': "texpenses/movement_compensation_application/"+\
                "movement_compensation_application.html",
                'report_name': 'compensation_application_report.pdf'},

            Petition.USER_COMPENSATION: {
                'template_path': "texpenses/movement_petition_application/"+\
                "movement_petition_application.html",
                'report_name': 'petition_application_report.pdf'},

            Petition.APPROVED_BY_PRESIDENT: {
                'template_path': "texpenses/movement_petition_application/"+\
                "movement_petition_application.html",
                'report_name': 'petition_application_report.pdf'}
        }

        template_path, report_name = (
            template_info[petition_status]['template_path'],
            template_info[petition_status]['report_name'])

        data = self._extract_info(petition)

        return render_template2pdf(request, data, template_path, report_name)

    @detail_route(methods=['get'])
    def decision_report(self, request, pk=None):
        petition = self.get_object()
        petition_status = petition.status

        template_info = {
            Petition.SUBMITTED_BY_SECRETARY: {
                'template_path': "texpenses/movement_petition_decision/"+\
                "movement_petition_decision.html",
                'report_name': 'petition_decision_report.pdf'},

            Petition.SECRETARY_COMPENSATION_SUBMISSION: {
                'template_path': "texpenses/movement_compensation_decision/"+\
                "movement_compensation_decision.html",
                'report_name': 'compensation_decision_report.pdf'}
        }

        template_path, report_name = (
            template_info[petition_status]['template_path'],
            template_info[petition_status]['report_name'])


        data = self._extract_info(petition)
        return render_template2pdf(request, data, template_path, report_name)

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
        travel_info_with_visa_accommodation_payment = (
            petition_object.travel_info.filter(
                accommodation_payment_way='VISA').exists())

        if petition_object.status in (Petition.SUBMITTED_BY_SECRETARY,
                                      Petition.APPROVED_BY_PRESIDENT,
                                      Petition.USER_COMPENSATION,
                                      Petition.
                                      SECRETARY_COMPENSATION_SUBMISSION):
            # protocol info
            data.update(
                {'dse': petition_object.dse,
                 'movement_id': petition_object.movement_id,
                 'movement_date_protocol':
                 petition_object.movement_date_protocol,
                 'movement_protocol': petition_object.movement_protocol,
                 'expenditure_protocol': petition_object.expenditure_protocol,
                 'expenditure_date_protocol':
                 petition_object.expenditure_date_protocol,
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
            travel_info = petition_object.travel_info.all()
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
                         'departure_point': travel_info_first.
                         departure_point.name,
                         'arrival_point': travel_info_last.arrival_point.name,
                         'means_of_transport':
                         utils.get_means_of_transport(travel_info),
                         'transportation_cost':
                         utils.get_transportation_cost(travel_info),
                         'transportation_default_currency':
                         travel_info_first.transportation_default_currency,
                         'overnights_sum_cost_string':
                         utils.get_overnights_sum_cost_string(travel_info),
                         'overnights_sum_cost':
                         petition_object.overnights_sum_cost,
                         'accommodation_default_currency':
                         travel_info_first.accommodation_default_currency,
                         'participation_cost': petition_object.
                         participation_cost,
                         'participation_default_currency': petition_object.
                         participation_default_currency,
                         'additional_expenses_initial': (
                             petition_object.additional_expenses if (
                                 petition_object.status == (
                                     Applications.USER_COMPENSATION)) else (
                                 petition_object.additional_expenses_initial)),
                         'additional_expenses_default_currency':
                         petition_object.additional_expenses_default_currency,
                         'total_cost': petition_object.total_cost_manual if (
                             petition_object.status >= (
                                 Applications.USER_COMPENSATION_SUBMISSION)
                         ) else petition_object.total_cost_calculated() ,
                         'project': petition_object.project.name,
                         'compensation_string' :
                         utils.get_compensation_levels_string(travel_info),
                         'compensation_cost':
                         utils.get_compensation_cost(travel_info),
                         'additional_expenses':
                         petition_object.additional_expenses,
                         'additional_expenses_local_currency':
                         petition_object.additional_expenses_local_currency,
                         'compensation_final':
                         petition_object.compensation_final,
                         'travel_info_with_visa_accommodation_payment':
                         travel_info_with_visa_accommodation_payment,
                         'overnights_to_be_compensated':
                         petition_object.overnights_to_be_compensated(),
                         'transportation_compensation':
                         petition_object.transportation_cost_to_be_compensated(),
                         'participation_payment_way': (
                             petition_object.participation_payment_way),
                         'is_total_manual_cost_set':
                         petition_object.is_total_manual_cost_set,
                         'total_cost_change_reason': (
                             petition_object.total_cost_change_reason)
                         })

        return data

    @detail_route(methods=['post'])
    @transaction.atomic
    def update_timesheeted(self, request, pk=None):
        try:
            application = self.get_object()
            application.timesheeted = not application.timesheeted
            application.save()
            return Response(
                {'message': 'Successfully updated timesheeted'},
                status=status.HTTP_200_OK)
        except PermissionDenied as e:
            return Response({'detail': e.message},
                            status=status.HTTP_403_FORBIDDEN)

    def get_queryset(self):
        non_atomic_requests = permissions.SAFE_METHODS
        user = self.request.user
        query = Applications.objects.select_related(
            'tax_office', 'user', 'project').prefetch_related('travel_info')

        if user.user_group() == "USER":
            query = query.filter(user=self.request.user, withdrawn=False)

        if user.user_group() == "VIEWER":
            query = query.filter(status__gte=Petition.SUBMITTED_BY_USER)

        if user.user_group() == "MANAGER":
            manager_projects = Project.objects.filter(manager=user)
            query = query.filter(Q(user=self.request.user) |
                                 (Q(project__in=manager_projects) &
                                  Q(manager_movement_approval=False) &
                                  Q(status__gte=Petition.SUBMITTED_BY_USER) &
                                  Q(status__lt=Petition.SUBMITTED_BY_SECRETARY)))

        if user.user_group() in ["SECRETARY", "CONTROLLER"]:
            query = query.filter(status__gte=Petition.SUBMITTED_BY_USER)

        if user.user_group() == "ADMIN":
            query = query.all()

        if self.request.method in non_atomic_requests:
            return query
        else:
            return query.select_for_update(nowait=True)
