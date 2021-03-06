# -*- coding: utf-8 -*-
import os
import xlsxwriter
import StringIO
from rest_framework import permissions, status
from datetime import datetime
from django.db import transaction
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.conf import settings
from django.http import HttpResponse, StreamingHttpResponse, Http404
from django.shortcuts import get_object_or_404
from wsgiref.util import FileWrapper

from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response

from rest_framework.reverse import reverse
from texpenses.models import Petition, City, Project, \
    Applications, TravelFile
from texpenses.actions import inform_on_action, inform
from texpenses.views.utils import render_template2pdf
from texpenses.views import utils
from texpenses.serials import get_serial


class CityMixin(object):

    def get_queryset(self):
        return City.objects.select_related('country').all()


class ProjectMixin(object):

    def _extract_info(self, petition):
        petition_info = {}

        # user info
        petition_info.update({'full_name': petition.first_name + ' ' +
                                           petition.last_name,
                              'kind': petition.get_kind_display(),
                              'specialty': petition.get_specialty_display(),
                              'dse': petition.dse,
                              'tax_reg_num': petition.tax_reg_num,
                              })
        # petition info
        travel_info = petition.travel_info.all()
        travel_info_first = travel_info[0]
        travel_info_last = travel_info[len(travel_info) - 1]
        depart_date = travel_info_first.local_depart_date
        return_date = travel_info_last.local_return_date
        task_start_date = petition.local_task_start_date
        task_end_date = petition.local_task_end_date
        compensation_days_proposed = \
            sum([ti.compensation_days_proposed() for ti in travel_info])
        petition_info.update({'depart_date': depart_date.
                              strftime(settings.DATE_FORMAT_WITHOUT_TIME),
                              'return_date': return_date.
                              strftime(settings.DATE_FORMAT_WITHOUT_TIME),
                              'task_start_date': task_start_date.
                              strftime(settings.DATE_FORMAT_WITHOUT_TIME),
                              'task_end_date': task_end_date.
                              strftime(settings.DATE_FORMAT_WITHOUT_TIME),
                              'transport_days': petition.transport_days(),
                              'compensation_days_num':
                              petition.compensation_days_num(),
                              'compensation_days_proposed': compensation_days_proposed,
                              'departure_point':
                              travel_info_first.departure_point.name,
                              'arrival_points':
                              utils.get_arrival_points(travel_info),
                              'means_of_transport':
                              utils.get_means_of_transport(travel_info),
                              'transportation_cost':
                              utils.get_transportation_cost(travel_info),
                              'overnights_sum_cost':
                              petition.overnights_sum_cost(),
                              'participation_cost':
                              petition.participation_cost,
                              'additional_expenses':
                              petition.additional_expenses,
                              'total_cost': petition.total_cost_calculated(),
                              'project': petition.project.name,
                              'accommodation_cost':
                              utils.get_accommodation_cost(travel_info),
                              'compensation_cost':
                              utils.get_compensation_cost(travel_info),
                              'status': petition.status,
                              'transportation_type': petition.transportation_type,
                              })
        return petition_info

    def _get_related_petitions(self, project_name=None):

        user = self.request.user
        if user.user_group() == "CONTROLLER":
            query = Applications.objects.filter(
                Q(status__gte=Petition.USER_COMPENSATION_SUBMISSION) &
                Q(status__lte=Petition.PETITION_FINAL_APPOVAL)
            )
        elif user.user_group() == "HELPDESK":
            query = Applications.objects.filter(
                Q(status__gte=Petition.SUBMITTED_BY_SECRETARY))

        petitions = query.filter(
            project__name=project_name) if project_name else (query)

        data = []

        for petition in petitions:
            data.append(self._extract_info(petition))

        return data

    @list_route()
    def stats(self, request):
        response = HttpResponse(content_type='application/ms-excel')
        filename = 'all_applications.xlsx'
        response['Content-Disposition'] = 'attachment; filename=' + filename

        output = StringIO.StringIO()
        wb = xlsxwriter.Workbook(
            output, {'constant_memory': True})
        ws = wb.add_worksheet('Applications')

        data = self._get_related_petitions()

        fields = ['ΔΣΕ', 'Μετακινούμενος', 'ΑΦΜ', 'Ιδιότητα', 'Ειδικότητα',
                  'Status', 'Έργο', 'Είδος Μετακίνησης', 'Αφετηρία', 'Προορισμοί', 'Έναρξη Εργασιών',
                  'Λήξη Εργασιών', 'Αναχώρηση', 'Επιστροφή', 'Μέσα Μετακίνησης',
                  'Κόστος Μετακίνησης', 'Ημέρες Μετακίνησης', 'Ημέρες Αποζημίωσης',
                  'Προτεινόμενες Ημέρες Αποζημίωσης', 'Σύνολο Ημερήσιας Αποζημίωσης',
                  'Κόστος Διανυκτέρευσης', 'Κόστος συμμετοχής', 'Λοιπά Έξοδα Μετακίνησης',
                  'Συνολικό Κόστος Μετακίνησης']

        k = 0
        for field in fields:
            ws.write(0, k, field.decode('utf-8'))
            k += 1

        i = 1
        for petition in data:
            row = [
                petition['dse'],
                petition['full_name'],
                petition['tax_reg_num'],
                petition['kind'],
                petition['specialty'],
                petition['status'],
                petition['project'],
                petition['transportation_type'],
                petition['departure_point'],
                petition['arrival_points'],
                petition['task_start_date'],
                petition['task_end_date'],
                petition['depart_date'],
                petition['return_date'],
                petition['means_of_transport'],
                petition['transportation_cost'],
                petition['transport_days'],
                petition['compensation_days_num'],
                petition['compensation_days_proposed'],
                petition['compensation_cost'],
                petition['accommodation_cost'],
                petition['participation_cost'],
                petition['additional_expenses'],
                petition['total_cost'],
            ]

            utils.write_row(ws, row, i)
            i += 1

        wb.close()
        xlsx_data = output.getvalue()
        response.write(xlsx_data)
        return response

    @detail_route(methods=['post'])
    @transaction.atomic
    def toggle_active(self, request, pk=None):
        try:
            project = self.get_object()
            project.active = not project.active
            project.save()
            return Response(
                {'message': "Changed project's active status"},
                status=status.HTTP_200_OK)
        except PermissionDenied as e:
            return Response({'detail': e.message},
                            status=status.HTTP_403_FORBIDDEN)


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
    def mark_as_deleted(self, request, pk=None):
        try:
            application = self.get_object()
            application.mark_as_deleted()
            return Response({'message': 'The petition was marked as deleted'},
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

        if application.inconsistent_overnights():
            return Response({'detail': 'Overnights are invalid'},
                             status=status.HTTP_403_FORBIDDEN)

        try:
            if application.status in [Petition.SAVED_BY_SECRETARY,
                    Petition.SECRETARY_COMPENSATION]:
                application.set_trip_days_left()
        except PermissionDenied as e:
            return Response({'detail': e.message},
                            status=status.HTTP_403_FORBIDDEN)

        application_id = application.proceed()

        per_status_email_confs = {
            Petition.SUBMITTED_BY_USER: [
                application, 'SUBMISSION', False, False, request.user],
            Petition.USER_COMPENSATION_SUBMISSION: [
                application, 'USER_COMPENSATION_SUBMISSION',
                False, True, request.user]
        }
        email_args = per_status_email_confs.get(application.status, None)

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
                    application.proceed()
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
                 'base_timezone': settings.BASE_TIMEZONE,
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
                         'timezone_depart': travel_info_first.departure_point.timezone,
                         'timezone_first_destination': travel_info_first.
                         arrival_point.timezone,
                         'timezone_last_destination': travel_info_last.
                         arrival_point.timezone,
                         'trip_days_before': petition_object.trip_days_before,
                         'trip_days_after': petition_object.trip_days_after,
                         'transport_days': petition_object.transport_days,
                         'compensation_days_num': petition_object.compensation_days_num,
                         'overnights_num': petition_object.overnights_num,
                         'reason': petition_object.reason,
                         'departure_point': travel_info_first.
                         departure_point.name,
                         'arrival_point': travel_info_last.arrival_point.name,
                         'means_of_transport':
                         utils.get_means_of_transport(travel_info),
                         'transportation_cost':
                         utils.get_transportation_cost(travel_info),
                         'overnights_sum_cost_string':
                         utils.get_overnights_sum_cost_string(travel_info),
                         'overnights_sum_cost':
                         petition_object.overnights_sum_cost,
                         'participation_cost': petition_object.
                         participation_cost,
                         'additional_expenses_initial': (
                             petition_object.additional_expenses if (
                                 petition_object.status == (
                                     Applications.USER_COMPENSATION)) else (
                                 petition_object.additional_expenses_initial)),
                         'additional_expenses_grnet':
                         petition_object.additional_expenses_grnet,
                         'total_cost': petition_object.total_cost_calculated(),
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

    @detail_route(methods=['post'])
    @transaction.atomic
    def update_manager_movement_approval(self, request, pk=None):
        try:
            application = self.get_object()
            if application.project.manager != request.user:
                raise PermissionDenied(
                        "You can't approve applications of that project")
            application.manager_movement_approval = \
                not application.manager_movement_approval
            application.save()
            return Response(
                {'message': 'Successfully updated manager movement approval'},
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
                                 Q(project__in=manager_projects))

        if user.user_group() in ["SECRETARY", "CONTROLLER"]:
            query = query.filter(status__gte=Petition.SUBMITTED_BY_USER)

        if user.user_group() == "ADMIN":
            query = query.all()

        query = query.order_by('-dse')
        if self.request.method in non_atomic_requests:
            return query
        else:
            return query.select_for_update(nowait=True)

    @detail_route(methods=['post'])
    @transaction.atomic
    def reset(self, request, pk=None):
        """
        Reset an application with a status greater than 3 (SAVED_BY_SECRETARY)
        to that one, allowing to correct any mistakes in the process.
        """
        REJECTED_STATUSES = (Petition.SAVED_BY_USER,
                             Petition.SUBMITTED_BY_USER,
                             Petition.SAVED_BY_SECRETARY)
        try:
            application = self.get_object()
            if application.status in REJECTED_STATUSES:
                return Response(status=status.HTTP_403_FORBIDDEN)
            application.mark_as_deleted()

            restoredApplication = Petition.objects.filter(dse=application.dse,
                    status=Petition.SAVED_BY_SECRETARY).order_by('-updated')[0]
            restoredApplication.transport_days_total = \
                application.transport_days_total
            restoredApplication.unmark_deleted()

            return Response(
                {'message': 'The application has been reset to status 3.'},
                status=status.HTTP_200_OK)

        except PermissionDenied as e:
            return Response({'detail': e.message},
                            status=status.HTTP_403_FORBIDDEN)


class UserMixin(object):

    @detail_route(methods=['post'])
    def toggle_active(self, request, pk=None):
        try:
            user = self.get_object()
            user.is_active = not user.is_active
            user.save()
            return Response(
                {'message': "Changed user's active status"},
                status=status.HTTP_200_OK)
        except PermissionDenied as e:
            return Response({'detail': e.message},
                            status=status.HTTP_403_FORBIDDEN)


class UploadFilesViewSet(object):
    FILE_SOURCE = {
            'Applications': 'petition'
    }

    @detail_route(methods=['post'])
    @transaction.atomic
    def upload(self, request, pk=None):
        obj = self.get_object()
        if 'file_upload' not in request.FILES:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        file_upload = request.FILES.get('file_upload', None)
        if not file_upload:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        owner = request.user
        uploaded_file = TravelFile.objects.create(
            id=get_serial('travel_file'),
            owner=owner,
            source_id=obj.id,
            source=self.FILE_SOURCE[obj.__class__.__name__],
            file_content=file_upload,
            file_name=file_upload.name,
            updated_at=datetime.utcnow())

        obj.travel_files.add(uploaded_file)
        return Response(status=status.HTTP_200_OK)


USE_X_SEND_FILE = getattr(settings, 'USE_X_SEND_FILE', False)

class FilesViewSet(object):

    @detail_route(methods=['head'], url_path='download')
    def download_head(self, request, pk=None):
        response = HttpResponse(content_type='application/force-download')
        assert request.method == 'HEAD'
        user = request.user
        file = self.get_object()
        token = utils.generate_file_token(user, file)
        url = utils.urljoin(settings.HOST_URL or '/',
                      reverse('api_travel-files-downloadfile', args=(pk,)))
        response['X-File-Location'] = "%s?token=%s" % (url, token)
        return response

    @detail_route(methods=['get'], url_path='downloadfile')
    def download_get(self, request, pk=None):
        token = request.GET.get('token', None)
        if token is None:
            raise PermissionDenied("no.token")
            # url = reverse('apella-files-download', args=(pk,))
            # ui_url = getattr(settings, 'DOWNLOAD_FILE_URL', '')
            # ui_download_url = '%s?#download=%s' % (ui_url, url)
            # return HttpResponseRedirect(ui_download_url)

        file_id = utils.consume_file_token(token)
        if not file_id == int(pk):
            raise Http404

        file = get_object_or_404(TravelFile, id=file_id)
        filename = file.file_name
        if isinstance(filename, unicode):
            filename = filename.encode('utf-8')
        filename = filename.replace('"', '')
        disp = 'attachment; filename="%s"' % filename
        if USE_X_SEND_FILE:
            response['X-Sendfile'] = file.file_content.path
        else:
            chunk_size = 8192
            response = StreamingHttpResponse(
                           FileWrapper(
                               open(file.file_content.path, 'rb'), chunk_size),
                                  content_type="application/force-download")
        response['Content-Disposition'] = disp
        return response

    def destroy(self, request, pk=None):
        obj = self.get_object()
        try:
            f = utils.safe_path_join(
                settings.MEDIA_ROOT, obj.file_content.name)
            os.remove(f)
        except OSError:
            pass
        return super(FilesViewSet, self).destroy(request, pk)
