from datetime import datetime, timedelta

from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.core.urlresolvers import reverse
from texpenses.models import (Petition, Project, UserProfile, Applications)

DATE_FORMAT = '%Y-%m-%dT%H:%M:%SZ'

task_start_date = datetime.now() + timedelta(days=2)
task_end_date = datetime.now() + timedelta(days=4)
depart_date = task_start_date - timedelta(days=1)
return_date = task_end_date + timedelta(days=1)

task_start_date = task_start_date.strftime(DATE_FORMAT)
task_end_date = task_end_date.strftime(DATE_FORMAT)
depart_date = depart_date.strftime(DATE_FORMAT)
return_date = return_date.strftime(DATE_FORMAT)


class TestApi(APITestCase):
    fixtures = ['texpenses/fixtures/testing_data.json', ]

    def _set_up(self):
        project_id = Project.objects.get(name='Up2U').id

        self.data = {'project': reverse('api_project-detail',
                                        args=[project_id])}

        self.user = UserProfile.objects.get(username='kostas')
        self.secretary = UserProfile.objects.get(username='athina')
        self.controller = UserProfile.objects.get(username='klykou')
        self.viewer = UserProfile.objects.get(username='eutuxia')
        self.manager = UserProfile.objects.get(username='ilias')
        self.president_secretary = UserProfile.objects.get(username='dimitra')
        self.admin = UserProfile.objects.get(username='admin')
        self.helpdesk = UserProfile.objects.get(username='nmorfi')

        self.user_token = Token.objects.create(user=self.user)
        self.secretary_token = Token.objects.create(user=self.secretary)
        self.controller_token = Token.objects.create(user=self.controller)
        self.manager_token = Token.objects.create(user=self.manager)
        self.viewer_token = Token.objects.create(user=self.viewer)
        self.president_secretary_token = Token.objects.create(
            user=self.president_secretary)
        self.admin_token = Token.objects.create(user=self.admin)
        self.helpdesk_token = Token.objects.create(user=self.helpdesk)

    def _set_up_manager_testing(self):

        self._set_up()

        self.user = self.manager
        self.user_token = self.manager_token

    def _user_testing(self):

        self.client.logout()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' +
                                self.user_token.key)

        # USER Saves application. It should fail and ask for missing
        # travel infos
        url = reverse('api_applications-list')
        response = self.client.post(url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Applications.objects.count(), 0)

        departure_city = reverse('api_city-detail', args=['204'])
        arrival_city = reverse('api_city-detail', args=['124'])

        travel_info = [{'depart_date': depart_date,
                        'return_date': return_date,
                        'departure_point': departure_city,
                        'arrival_point': arrival_city,
                        }]

        self.data.update({'reason': 'reason',
                          'task_start_date': task_start_date,
                          'task_end_date': task_end_date,
                          'travel_info': travel_info})

        # It should work now
        response = self.client.post(url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Applications.objects.count(), 1)

        # USER tries to edit the application
        application_id = response.data['id']
        url_retrieve = reverse('api_applications-detail',
                               args=[application_id])
        self.data.update({'reason': 'new reason'})
        response = self.client.put(url_retrieve, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # USER Submits application.
        application_id = response.data['id']
        url_submit = reverse('api_applications-submit',
                             args=[application_id])
        response = self.client.post(url_submit, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_303_SEE_OTHER)
        self.assertEqual(Applications.objects.count(), 1)

        # USER GETs created application
        response = self.client.get(url_retrieve, format='json')

        # USER CANCELs application
        submitted_application_id = Applications.objects.get(
            status=Petition.SUBMITTED_BY_USER, user=self.user).id
        url_cancel = reverse('api_applications-cancel',
                             args=[submitted_application_id])
        response = self.client.post(url_cancel, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_303_SEE_OTHER)

        # USER RE-SUBMITs application
        application_id = Applications.objects.get(
            status=Petition.SAVED_BY_USER, user=self.user).id
        url_submit = reverse('api_applications-submit',
                             args=[application_id])
        response = self.client.post(url_submit, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_303_SEE_OTHER)

    def _manager_testing(self):

        # Manager approves application

        self.client.logout()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' +
                                self.manager_token.key)

        application_id = Applications.objects.get(
            status=Petition.SUBMITTED_BY_USER).id

        url_retrieve = reverse('api_applications-detail',
            args=[application_id])
        response = self.client.get(url_retrieve, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        previous_status = response.data['manager_movement_approval']

        url = reverse('api_applications-update-manager-movement-approval',
            args=[application_id])
        response = self.client.post(url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url_retrieve = reverse('api_applications-detail',
            args=[application_id])
        response = self.client.get(url_retrieve, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['manager_movement_approval'],
            not previous_status)


    def _viewer_testing(self):
        self.client.logout()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' +
                                self.viewer_token.key)

        application_id = Applications.objects.get(
            status=Petition.SUBMITTED_BY_USER).id
        url = reverse('api_applications-detail', args=[application_id])

        response = self.client.put(url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        url_delete = reverse(
            'api_applications-mark-as-deleted', args=[application_id])
        response = self.client.post(url_delete, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def _secretary_testing(self, withdraw=False):

        self.client.logout()
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.secretary_token.key)

        application_id = Applications.objects.get(
            status__gte=Petition.SUBMITTED_BY_USER).id
        url = reverse('api_applications-detail', args=[application_id])

        # SECRETARY GETs created application

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Applications.objects.count(), 1)

        # SECRETARY Saves application.

        url_retrieve = reverse('api_applications-detail',
                               args=[application_id])

        # Make sure required fields are cleared in case this has been
        # run again (application reset)
        self.data.update({
            'movement_date_protocol': None,
            'movement_protocol': None,
            'expenditure_date_protocol': None,
            'expenditure_protocol': None,
        })

        response = self.client.put(url_retrieve, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Applications.objects.count(), 1)

        # Secretary Submits application. It should fail and ask for mandatory
        # elements to be filled
        application_id = response.data['id']
        protocol_exists = response.data['compensation_decision_protocol']
        url_submit = reverse('api_applications-submit',
                             args=[application_id])
        response = self.client.post(url_submit, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_303_SEE_OTHER if
                         protocol_exists else status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Applications.objects.count(), 1)

        # Secretary updates application. Insert mandatory fields to self.data

        url_retrieve = reverse('api_applications-detail',
                               args=[application_id])

        self.data.update({
            'movement_date_protocol': datetime.now().strftime(DATE_FORMAT),
            'movement_protocol': '1234',
            'expenditure_date_protocol': datetime.now().strftime(DATE_FORMAT),
            'expenditure_protocol': '4567',
        })

        self.data['travel_info'][0].update({
            'transportation_cost': 230,
            'transportation_payment_description': 'transportation_description'
        })

        response = self.client.put(url_retrieve, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Secretary Submits application

        response = self.client.post(url_submit, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_303_SEE_OTHER)
        self.assertEqual(Applications.objects.count(), 1)

        # Secretary Cancels application

        application_id = Applications.objects.get(
            status=Petition.SUBMITTED_BY_SECRETARY).id

        url_cancel = reverse('api_applications-cancel',
                             args=[application_id])

        response = self.client.post(url_cancel, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_303_SEE_OTHER)
        self.assertEqual(Applications.objects.count(), 1)

        # Secretary RE-SUBMITs application
        application_id = Applications.objects.get(
            status=Petition.SAVED_BY_SECRETARY).id

        url_submit = reverse('api_applications-submit',
                             args=[application_id])
        response = self.client.post(url_submit, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_303_SEE_OTHER)

        # Secretary gets movement application report

        application_id = Applications.objects.get(
            status=Petition.SUBMITTED_BY_SECRETARY).id
        url_application_report = reverse('api_applications-application-report',
                                         args=[application_id])
        response = self.client.get(url_application_report, format='pdf')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Secretary gets movement decision report

        url_decision_report = reverse('api_applications-decision-report',
                                      args=[application_id])
        response = self.client.get(url_decision_report, format='pdf')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Secretary runs president approval action

        url_president_approval = reverse(
            'api_applications-president-approval', args=[application_id])
        response = self.client.post(url_president_approval, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Applications.objects.count(), 1)

        # Secretary cancels president approval

        application_id = Applications.objects.get(
            status=Petition.APPROVED_BY_PRESIDENT).id

        url_president_approval_cancel = reverse(
            'api_applications-cancel', args=[application_id])
        response = self.client.post(url_president_approval_cancel,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_303_SEE_OTHER)

        if withdraw:

            # withdraw application
            application_id = Applications.objects.get(
                status=Petition.SUBMITTED_BY_SECRETARY).id

            url = reverse('api_applications-withdraw', args=[application_id])
            response = self.client.post(url, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            # cancel withdrawal
            url = reverse('api_applications-cancel-withdrawal',
                          args=[application_id])
            response = self.client.post(url, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            # withdraw again
            url = reverse('api_applications-withdraw', args=[application_id])
            response = self.client.post(url, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            # cancel withdrawal again
            url = reverse('api_applications-cancel-withdrawal',
                          args=[application_id])
            response = self.client.post(url, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def _president_secretary_testing(self):

        # president secretary approves an application
        self.client.logout()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' +
                                self.president_secretary_token.key)

        application_id = Applications.objects.get(
            status=Petition.SUBMITTED_BY_SECRETARY).id

        # President secretary runs president approval action

        url_president_approval = reverse(
            'api_applications-president-approval', args=[application_id])
        response = self.client.post(url_president_approval, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Applications.objects.count(), 1)

        # President secretary cancels president approval

        application_id = Applications.objects.get(
            status=Petition.APPROVED_BY_PRESIDENT).id

        url_president_approval_cancel = reverse(
            'api_applications-cancel', args=[application_id])
        response = self.client.post(url_president_approval_cancel,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_303_SEE_OTHER)

        # President secretary resubmits president approval

        application_id = Applications.objects.get(
            status=Petition.SUBMITTED_BY_SECRETARY).id

        url_president_approval = reverse(
            'api_applications-president-approval', args=[application_id])
        response = self.client.post(url_president_approval, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Applications.objects.count(), 1)

    def _user_compensation_testing(self):

        self.client.logout()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' +
                                self.user_token.key)
        # User gets related application
        url = reverse('api_applications-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['status'], 5)

        # User gets movement application report
        application_id = response.data[0]['id']

        url_application_report = reverse(
            'api_applications-application-report', args=[application_id])
        response = self.client.get(url_application_report, format='pdf')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # User saves application
        url_retrieve = reverse('api_applications-detail',
                               args=[application_id])

        response = self.client.put(url_retrieve, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Applications.objects.count(), 1)
        self.assertEqual(response.data['status'],
                         Petition.USER_COMPENSATION)

        # User Submits application. It should fail and ask for mandatory
        # elements to be filled
        application_id = response.data['id']
        url_submit = reverse('api_applications-submit', args=[application_id])
        response = self.client.post(url_submit, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Applications.objects.count(), 1)

        # User updates application. Insert mandatory fields to self.data

        url_retrieve = reverse('api_applications-detail',
                               args=[application_id])
        from django.core.files.uploadedfile import SimpleUploadedFile
        report_file = SimpleUploadedFile("report.pdf", "file_content",
                                         content_type="text/pdf")

        self.data.update({
            'travel_report': 'Random words',
            'travel_files': report_file
        })

        del self.data['travel_info']

        response = self.client.put(url_retrieve, self.data,
                                   format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # User Submits application

        url_submit = reverse('api_applications-submit',
                             args=[application_id])
        response = self.client.post(url_submit, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_303_SEE_OTHER)
        self.assertEqual(Applications.objects.count(), 1)

        # User Cancels application

        application_id = Applications.objects.get(
            status=Petition.USER_COMPENSATION_SUBMISSION).id

        url_cancel = reverse('api_applications-cancel',
                             args=[application_id])

        response = self.client.post(url_cancel, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_303_SEE_OTHER)
        self.assertEqual(Applications.objects.count(), 1)

        # User RE-SUBMITs application
        application_id = Applications.objects.get(
            status=Petition.USER_COMPENSATION).id

        url_submit = reverse('api_applications-submit',
                             args=[application_id])
        response = self.client.post(url_submit, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_303_SEE_OTHER)

    def _controller_testing(self, withdraw=False):

        self.client.logout()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' +
                                self.controller_token.key)
        # CONTROLLER GETs created application
        url = reverse('api_applications-list')

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Applications.objects.count(), 1)

        # CONTROLLER Saves application.
        application_id = response.data[0]['id']
        url_retrieve = reverse('api_applications-detail',
                               args=[application_id])

        response = self.client.put(url_retrieve, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Applications.objects.count(), 1)

        # CONTROLLER Submits application. It should fail and ask for mandatory
        # elements to be filled

        application_id = response.data['id']
        url_submit = reverse('api_applications-submit',
                             args=[application_id])
        response = self.client.post(url_submit, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Applications.objects.count(), 1)

        # CONTROLLER updates application. Insert mandatory fields to self.data

        url_retrieve = reverse('api_applications-detail',
                               args=[application_id])

        self.data.update({
            'compensation_decision_date': datetime.now().strftime(DATE_FORMAT),
            'compensation_decision_protocol': '1234',
            'compensation_petition_date': datetime.now().strftime(DATE_FORMAT),
            'compensation_petition_protocol': '4321',
        })

        response = self.client.put(url_retrieve, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        if withdraw:
            # withdraw application

            url = reverse('api_applications-withdraw', args=[application_id])
            response = self.client.post(url, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            # cancel withdrawal
            url = reverse('api_applications-cancel-withdrawal',
                          args=[application_id])
            response = self.client.post(url, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            return

        # Controller Submits application

        url_submit = reverse('api_applications-submit', args=[application_id])
        response = self.client.post(url_submit, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_303_SEE_OTHER)
        self.assertEqual(Applications.objects.count(), 1)

        # Controller Cancels application

        application_id = Applications.objects.get(
            status=Petition.SECRETARY_COMPENSATION_SUBMISSION).id

        url_cancel = reverse('api_applications-cancel',
                             args=[application_id])

        response = self.client.post(url_cancel, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_303_SEE_OTHER)
        self.assertEqual(Applications.objects.count(), 1)

        # CONTROLLER RE-SUBMITs application
        application_id = Applications.objects.get(
            status=Petition.SECRETARY_COMPENSATION).id

        url_submit = reverse('api_applications-submit',
                             args=[application_id])
        response = self.client.post(url_submit, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_303_SEE_OTHER)

        # Controller gets movement application report

        application_id = Applications.objects.get(
            status=Petition.SECRETARY_COMPENSATION_SUBMISSION).id
        url_application_report = reverse('api_applications-application-report',
                                         args=[application_id])
        response = self.client.get(url_application_report, format='pdf')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Controller gets movement decision report

        url_decision_report = reverse('api_applications-decision-report',
                                      args=[application_id])
        response = self.client.get(url_decision_report, format='pdf')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # CONTROLLER runs president approval action

        url_president_approval = reverse('api_applications-president-approval',
                                         args=[application_id])
        response = self.client.post(url_president_approval, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Applications.objects.count(), 1)

    def _helpdesk_reset_testing(self, permitted=True):

        self.client.logout()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' +
                                self.helpdesk_token.key)
        # HELPDESK GETs created application
        url = reverse('api_applications-list')

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Applications.objects.count(), 1)

        # HELPDESK checks application
        application_id = response.data[0]['id']
        url_retrieve = reverse('api_applications-detail',
                               args=[application_id])

        response = self.client.get(url_retrieve, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Applications.objects.count(), 1)

        # HELPDESK tries to reset the application to status 3

        application_id = response.data['id']
        url_reset = reverse('api_applications-reset',
                             args=[application_id])
        response = self.client.post(url_reset, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK if
                         permitted else status.HTTP_403_FORBIDDEN)
        self.assertEqual(Applications.objects.count(), 1)

    def _test_workflow(self):
        self._user_testing()
        self._manager_testing()
        self._viewer_testing()
        self._secretary_testing()
        self._president_secretary_testing()
        self._user_compensation_testing()
        self._controller_testing()

    def _test_workflow_withdraw(self):
        self._user_testing()
        self._manager_testing()
        self._viewer_testing()
        self._secretary_testing(withdraw=True)
        self._president_secretary_testing()
        self._user_compensation_testing()
        self._controller_testing(withdraw=True)

    def _test_reset_workflow(self):
        self._user_testing()
        self._helpdesk_reset_testing(permitted=False)
        self._manager_testing()
        self._viewer_testing()
        self._secretary_testing()
        self._president_secretary_testing()
        self._helpdesk_reset_testing(permitted=True)
        self._secretary_testing()
        self._president_secretary_testing()
        self._user_compensation_testing()
        self._controller_testing()

    def test_application_per_usergroup(self):
        """
        Test workflow for case of distinct users per role
        """

        self._set_up()
        self._test_workflow()

    def test_application_per_usergroup_withdraw(self):
        """
        Test workflow for case of distinct users per role
        """

        self._set_up()
        self._test_workflow_withdraw()

    # We test manager separately because he is also a user, so we need to know
    # everything that runs for user runs for manager as well.
    def test_application_per_usergroup_manager(self):

        """
        Test workflow for case where user is also manager
        """

        self._set_up_manager_testing()
        self._test_workflow()

    def test_helpdesk_application_reset_workflow(self):
        """
        Test workflow for the case of an application that
        has been reset and processed again
        """
        self._set_up()
        self._test_reset_workflow()

    def test_users_api_as_user(self):
        self._set_up()
        self.client.logout()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' +
                                self.user_token.key)

        url_list = reverse('api_users-list')
        response = self.client.get(url_list, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        url_detail = reverse('api_users-detail',
                             args=[self.user.id])
        response = self.client.get(url_detail, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.data = {'email': 'newmail@example.com'}

        response = self.client.put(url_detail, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        url_deactivate = reverse('api_users-toggle-active',
                                 args=[self.user.id])
        response = self.client.post(url_deactivate, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.get(url_detail, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['is_active'], True)

    def test_users_api_as_helpdesk(self):
        self._set_up()
        self.client.logout()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' +
                                self.helpdesk_token.key)

        url_list = reverse('api_users-list')
        response = self.client.get(url_list, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url_detail = reverse('api_users-detail',
                      args=[self.user.id])
        response = self.client.get(url_detail, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.data = {'email': 'newmail@example.com'}

        response = self.client.put(url_detail, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url_deactivate = reverse('api_users-toggle-active',
                                 args=[self.user.id])
        response = self.client.post(url_deactivate, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(url_detail, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['is_active'], False)

        url_activate = reverse('api_users-toggle-active',
                                 args=[self.user.id])
        response = self.client.post(url_activate, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(url_detail, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['is_active'], True)

    def test_tax_office_api_as_user(self):
        self._set_up()
        self.client.logout()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' +
                                self.user_token.key)

        url = reverse('api_tax-office-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        tax_office_id = response.data[0]['id']
        url = reverse('api_tax-office-detail',
                      args=[tax_office_id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_project_api_as_user(self):
        self._set_up()
        self.client.logout()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' +
                                self.user_token.key)

        url_list = reverse('api_project-list')
        response = self.client.get(url_list, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        project_id = response.data[0]['id']
        url_detail = reverse('api_project-detail',
                      args=[project_id])
        response = self.client.get(url_detail, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        manager = reverse('api_users-detail', args=[self.manager.id])

        self.data.clear()
        self.data.update({'manager': manager,
                          'accounting_code': 12321,
                          'name': 'NewProject'})
        response = self.client.post(url_list, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.put(url_detail, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        url_activate = reverse('api_project-toggle-active',
                                 args=[project_id])
        response = self.client.post(url_activate, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.get(url_detail, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['active'], True)

        url_stats = reverse('api_project-stats')
        response = self.client.get(url_stats, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_project_api_as_helpdesk(self):
        self._set_up()
        self.client.logout()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' +
                                self.helpdesk_token.key)

        url_list = reverse('api_project-list')
        response = self.client.get(url_list, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        project_id = response.data[0]['id']
        url_detail = reverse('api_project-detail',
                      args=[project_id])
        response = self.client.get(url_detail, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        manager = reverse('api_users-detail', args=[self.manager.id])

        self.data.clear()
        self.data.update({'manager': manager,
                          'accounting_code': 12345,
                          'name': 'NeoProject'})
        response = self.client.post(url_list, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        new_project_id = response.data['id']
        url_detail = reverse('api_project-detail',
                      args=[new_project_id])
        response = self.client.put(url_detail, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url_deactivate = reverse('api_project-toggle-active',
                                 args=[new_project_id])
        response = self.client.post(url_deactivate, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(url_detail, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['active'], False)

        url_activate = reverse('api_project-toggle-active',
                                 args=[new_project_id])
        response = self.client.post(url_activate, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(url_detail, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['active'], True)

        url_stats = reverse('api_project-stats')
        response = self.client.get(url_stats, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_project_api_as_controller(self):
        self._set_up()
        self.client.logout()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' +
                                self.controller_token.key)

        url_list = reverse('api_project-list')
        response = self.client.get(url_list, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        project_id = response.data[0]['id']
        url_detail = reverse('api_project-detail',
                      args=[project_id])
        response = self.client.get(url_detail, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url_stats = reverse('api_project-stats')
        response = self.client.get(url_stats, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_countries_api_as_user(self):
        self._set_up()
        self.client.logout()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' +
                                self.user_token.key)

        url = reverse('api_countries-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        country_id = response.data[0]['id']
        url = reverse('api_countries-detail',
                      args=[country_id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_city_api_as_user(self):
        self._set_up()
        self.client.logout()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' +
                                self.user_token.key)

        url_list = reverse('api_city-list')
        response = self.client.get(url_list, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        city_id = response.data[0]['id']
        url_detail = reverse('api_city-detail',
                      args=[city_id])
        response = self.client.get(url_detail, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        country = reverse('api_countries-detail', args=[42])

        self.data.clear()
        self.data.update({'country': country,
                          'timezone': 'Europe/Athens',
                          'name': 'Larissa'})
        response = self.client.post(url_list, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.put(url_detail, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_city_api_as_helpdesk(self):
        self._set_up()
        self.client.logout()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' +
                                self.helpdesk_token.key)

        url_list = reverse('api_city-list')
        response = self.client.get(url_list, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        city_id = response.data[0]['id']
        url_detail = reverse('api_city-detail',
                      args=[city_id])
        response = self.client.get(url_detail, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        country = reverse('api_countries-detail', args=[42])

        self.data.clear()
        self.data.update({'country': country,
                          'timezone': 'Europe/Athens',
                          'name': 'Larissa'})
        #response = self.client.post(url_list, self.data, format='json')
        #self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        city_id = response.data['id']
        url_detail = reverse('api_city-detail',
                      args=[city_id])
        response = self.client.get(url_detail, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        new_timezone = 'Europe/Madrid'
        self.data.update({'timezone': new_timezone})
        #response = self.client.put(url_detail, self.data, format='json')
        #self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(url_detail, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        #self.assertEqual(response.data['timezone'], new_timezone)

    def test_city_distances_api_as_user(self):
        self._set_up()
        self.client.logout()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' +
                                self.user_token.key)

        url_list = reverse('api_city-distances-list')
        response = self.client.get(url_list, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        distance_id = response.data[0]['id']
        url_detail = reverse('api_city-distances-detail',
                      args=[distance_id])
        response = self.client.get(url_detail, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        to_city = reverse('api_city-detail', args=['199'])
        from_city = reverse('api_city-detail', args=['192'])

        self.data.update({'from_city': to_city,
                          'to_city': from_city,
                          'distance': 1231.4})
        response = self.client.post(url_list, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.put(url_detail, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_city_distances_api_as_helpdesk(self):
        self._set_up()
        self.client.logout()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' +
                                self.helpdesk_token.key)

        url_list = reverse('api_city-distances-list')
        response = self.client.get(url_list, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        distance_id = response.data[0]['id']
        url_detail = reverse('api_city-distances-detail',
                      args=[distance_id])
        response = self.client.get(url_detail, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        to_city = reverse('api_city-detail', args=['104'])
        from_city = reverse('api_city-detail', args=['24'])

        self.data.update({'from_city': to_city,
                          'to_city': from_city,
                          'distance': 1231.4})
        response = self.client.post(url_list, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        distance_id = response.data['id']
        url_detail = reverse('api_city-distances-detail',
                      args=[distance_id])
        response = self.client.get(url_detail, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        new_distance = 135
        self.data.update({'distance': new_distance})
        response = self.client.put(url_detail, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(url_detail, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['distance'], new_distance)
