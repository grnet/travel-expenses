from datetime import datetime, timedelta
import sys
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from texpenses.models import (
    City, TravelInfo, Petition, UserPetition, Project, UserProfile, TaxOffice,
    UserPetitionSubmission, SecretaryPetition, SecretaryPetitionSubmission)


PETITION_APIS = {
    UserPetition: reverse('userpetition-list'),
    UserPetitionSubmission: reverse('userpetitionsubmission-list'),
    SecretaryPetition: reverse('secretarypetition-list'),
    SecretaryPetitionSubmission: reverse('secretarypetitionsubmission-list')
}

SUBMISSION_APIS = {
    UserPetitionSubmission: reverse('userpetitionsubmission-list'),
    SecretaryPetitionSubmission: reverse('secretarypetitionsubmission-list')
}


class APIPetitionTest(APITestCase):
    end_date = datetime.now() + timedelta(days=7)
    start_date = datetime.now() + timedelta(days=5)

    def setUp(self):
        tax_office = TaxOffice.objects.create(
            name='test', description='test', address='test',
            email='test@example.com', phone='2104344444')
        self.user = UserProfile.objects.create_user(
            username='admin', first_name='Nick', last_name='Jones',
            email='test@email.com', is_staff=True,
            iban='GR4902603280000910200635494', is_superuser=True,
            password='test',
            specialty='1', tax_reg_num=150260153,
            tax_office=tax_office, category='A',
            trip_days_left=5)
        self.city = City.objects.create(name='Athens')
        self.project = Project.objects.create(name='Test Project',
                                              accounting_code=1)
        token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        self.client.force_authenticate(user=self.user, token=token)
        self.project_url = reverse('project-detail', args=[1])
        self.user_url = reverse('userprofile-detail', args=[1])

    def test_create_user_petition(self):
        self.client.force_authenticate(user=self.user)
        UserPetitionSubmission.required_fields = ()
        SecretaryPetitionSubmission.required_fields = ()
        self.assertRaises(ObjectDoesNotExist,
                          Petition.objects.get, project=self.project)
        data = {'project': self.project_url,
                'task_start_date': self.start_date,
                'task_end_date': self.end_date, 'additional_data': [],
                'user': self.user_url}
        for model, url in PETITION_APIS.iteritems():
            response = self.client.post(url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            petitions = self.client.get(url)
            fields = model.APITravel.fields
            self.assertEqual(len(petitions.data), 1)
            created_petition = petitions.data[0]

            for field in created_petition:
                self.assertTrue(field in fields)

    def test_status_400_petition(self):
        required_fields = ('project',
                           'additional_data')
        self.assertRaises(ObjectDoesNotExist,
                          Petition.objects.get, project=self.project)
        data = {'project': self.project_url, 'additional_data': []}
        url = reverse('userpetition-list')
        for field in required_fields:
            value = data.pop(field)
            response = self.client.post(url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertEqual(response.data,
                             {field: ['This field is required.']})
            data[field] = value

        city_url = reverse('city-detail', args=[1])
        additional_data = [{'arrival_point': city_url,
                            'departure_point': city_url,
                            'accommodation_price': float('inf')}]
        data['additional_data'] = additional_data
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        validation_message = 'Accomondation price inf for petition with DSE' +\
            ' 1 exceeds the max overnight cost.'
        self.assertEqual(response.data,
                         {'non_field_errors': [validation_message]})

    def test_submission_apis(self):
        UserPetitionSubmission.required_fields = ('reason',)
        SecretaryPetitionSubmission.required_fields = ('reason',)
        data = {'project': self.project_url,
                'task_start_date': self.start_date,
                'task_end_date': self.end_date, 'additional_data': [],
                'reason': 'reason'}
        for model, url in SUBMISSION_APIS.iteritems():
            response = self.client.post(url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            participation_cost = data.pop('reason')
            response = self.client.post(url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertEqual(response.data, {
                'non_field_errors': [
                    'Field %s is required' % repr('reason')]})
            data['reason'] = participation_cost

    def test_submission_permissions(self):
        UserPetitionSubmission.required_fields = ()
        SecretaryPetitionSubmission.required_fields = ()
        data = {'project': self.project_url,
                'task_start_date': self.start_date,
                'task_end_date': self.end_date, 'additional_data': []}
        for _, url in SUBMISSION_APIS.iteritems():
            response = self.client.post(url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            # test put
            response = self.client.put(url, data, format='json')
            self.assertEqual(
                response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
            # test patch
            response = self.client.patch(url, data, format='json')
            self.assertEqual(
                response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
            # test delete
            response = self.client.delete(url, data, format='json')
            self.assertEqual(
                response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_nested_serialization(self):
        UserPetitionSubmission.required_fields = ()
        SecretaryPetitionSubmission.required_fields = ()
        city_url = reverse('city-detail', args=[1])
        for model, url in PETITION_APIS.iteritems():
            additional_data = [{'arrival_point': city_url,
                                'departure_point': city_url,
                                'transport_days_manual': sys.maxint}]
            data = {'project': self.project_url,
                    'task_start_date': self.start_date,
                    'task_end_date': self.end_date,
                    'additional_data': additional_data,
                    'user': self.user_url}
            response = self.client.post(url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertEqual(response.data, {
                u'non_field_errors':
                    [u'You have exceeded the allowable number of trip days']
            })
            additional_data[0].pop('transport_days_manual')

            # Check nested creation.
            data = {'project': self.project_url,
                    'task_start_date': self.start_date,
                    'task_end_date': self.end_date,
                    'additional_data': additional_data,
                    'user': self.user_url}
            response = self.client.post(url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            petition = response.data
            petition_url = petition['url']
            travel_info = petition['travel_info']
            self.assertEqual(len(travel_info), 1)
            response = self.client.get(travel_info[0])
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            for field in response.data:
                self.assertTrue(field in TravelInfo.APITravel.fields)

            # Check nested updates.
            accommodation_price = 10
            additional_data = [{'arrival_point': city_url,
                                'departure_point': city_url,
                                'accommodation_price': accommodation_price},
                               {'arrival_point': city_url,
                                'departure_point': city_url}]
            data['additional_data'] = additional_data
            response = self.client.put(
                petition_url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            petition = response.data
            travel_info = petition['travel_info']
            self.assertEqual(len(travel_info), 2)
            response = self.client.get(travel_info[0])
            self.assertEqual(response.data['accommodation_price'],
                             accommodation_price)
            response = self.client.get(travel_info[1])
            self.assertEqual(response.data['accommodation_price'], 0.0)
