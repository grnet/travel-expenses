from datetime import datetime, timedelta

from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.core.urlresolvers import reverse
from texpenses.models import (Petition, Project, UserProfile, Applications)

DATE_FORMAT = '%Y-%m-%dT%H:%M'

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

        self.user_token = Token.objects.create(user=self.user)
        self.secretary_token = Token.objects.create(user=self.secretary)
        self.controller_token = Token.objects.create(user=self.controller)
        self.manager_token = Token.objects.create(user=self.manager)
        self.viewer_token = Token.objects.create(user=self.viewer)
        self.president_secretary_token = Token.objects.create(
            user=self.president_secretary)
        self.admin_token = Token.objects.create(user=self.admin)

    def _set_up_manager_testing(self):

        self._set_up()

        self.user = self.manager
        self.user_token = self.manager_token

    def _user_testing(self):

        self.client.logout()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' +
                                self.user_token.key)

        # USER Saves application
        url = reverse('api_applications-list')
        response = self.client.post(url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Applications.objects.count(), 1)

        # USER Submits application. It should fail and ask for mandatory
        # elements to be filled
        application_id = response.data['id']
        url_submit = reverse('api_applications-submit',
                             args=[application_id])
        response = self.client.post(url_submit, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Applications.objects.count(), 1)

        # User updates data with mandatory fields and save

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

        url_retrieve = reverse('api_applications-detail',
                               args=[application_id])
        response = self.client.put(url_retrieve, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Applications.objects.count(), 1)

        # USER GETs created application
        response = self.client.get(url_retrieve, format='json')

        # USER SUBMITs application
        response = self.client.post(url_submit, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_303_SEE_OTHER)

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
        url = reverse('api_applications-detail', args=[application_id])

        self.data.update({'manager_movement_approval': True})

        response = self.client.put(url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def _viewer_testing(self):
        self.client.logout()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' +
                                self.viewer_token.key)

        application_id = Applications.objects.get(
            status=Petition.SUBMITTED_BY_USER).id
        url = reverse('api_applications-detail', args=[application_id])

        response = self.client.put(url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def _secretary_testing(self, president_approval=True):

        self.client.logout()
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.secretary_token.key)
        application_id = Applications.objects.get(
            status=Petition.SUBMITTED_BY_USER).id
        url = reverse('api_applications-detail', args=[application_id])

        # SECRETARY GETs created application

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Applications.objects.count(), 1)

        # SECRETARY Saves application.

        url_retrieve = reverse('api_applications-detail',
                               args=[application_id])

        response = self.client.put(url_retrieve, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Applications.objects.count(), 1)

        # Secretary Submits application. It should fail and ask for mandatory
        # elements to be filled
        application_id = response.data['id']
        url_submit = reverse('api_applications-submit',
                             args=[application_id])
        response = self.client.post(url_submit, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Applications.objects.count(), 1)

        # Secretary updates application. Insert mandatory fields to self.data

        url_retrieve = reverse('api_applications-detail',
                               args=[application_id])

        self.data.update({
            'movement_date_protocol': datetime.now().strftime('%Y-%m-%d'),
            'movement_protocol': '1234',
            'expenditure_date_protocol': datetime.now().strftime('%Y-%m-%d'),
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

        url_application_report = reverse('api_applications-application-report',
                                         args=[application_id])
        response = self.client.get(url_application_report, format='pdf')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # User saves application
        url_retrieve = reverse('api_applications-detail',
                               args=[application_id])

        response = self.client.put(url_retrieve, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Applications.objects.count(), 1)
        self.assertEqual(response.data['status'], Petition.USER_COMPENSATION)

        # User Submits application. It should fail and ask for mandatory
        # elements to be filled
        application_id = response.data['id']
        url_submit = reverse('api_applications-submit',
                             args=[application_id])
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

        url_submit = reverse('api_applications-submit', args=[application_id])
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

        url_submit = reverse('api_applications-submit', args=[application_id])
        response = self.client.post(url_submit, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_303_SEE_OTHER)

    def _controller_testing(self):

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
            'compensation_decision_date': datetime.now().strftime('%Y-%m-%d'),
            'compensation_decision_protocol': '1234',
            'compensation_petition_date': datetime.now().strftime('%Y-%m-%d'),
            'compensation_petition_protocol': '4321',
        })

        response = self.client.put(url_retrieve, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

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

    def _test_workflow(self):
        self._user_testing()
        self._manager_testing()
        self._viewer_testing()
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

    # We test manager separately because he is also a user, so we need to know
    # everything that runs for user runs for manager as well.
    def test_application_per_usergroup_manager(self):

        """
        Test workflow for case where user is also manager
        """

        self._set_up_manager_testing()
        self._test_workflow()
