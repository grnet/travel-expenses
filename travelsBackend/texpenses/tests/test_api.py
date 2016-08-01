from datetime import datetime, timedelta
import sys
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from texpenses.models import (
    City, TravelInfo, Petition, UserPetition, Project, UserProfile, TaxOffice,
    UserPetitionSubmission, SecretaryPetition, SecretaryPetitionSubmission,
    Country)


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

PROTOCOL_DATE_FORMAT = '%Y-%m-%d'
PROTOCOL_DATE = (datetime.now() + timedelta(days=1)).strftime(
    PROTOCOL_DATE_FORMAT)

EXTRA_DATA = {
    UserPetition: {},
    UserPetitionSubmission: {'reason': 'reason'},
    SecretaryPetition: {},
    SecretaryPetitionSubmission: {
        'additional_expenses_initial_description': 'test',
        'expenditure_protocol': 'expenditure protocol',
        'expenditure_date_protocol': PROTOCOL_DATE,
        'movement_protocol': 'movement protocol',
        'movement_date_protocol': PROTOCOL_DATE}
}

UserPetitionSubmission.mandatory_fields = ()
SecretaryPetitionSubmission.mandatory_fields = ()


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
            specialty='1', tax_reg_num=011111111,
            tax_office=tax_office, user_category='A',
            trip_days_left=5)
        self.city = City.objects.create(
            name='Athens', country=Country.objects.create(name='Greece'))
        self.project = Project.objects.create(name='Test Project',
                                              accounting_code=1,
                                              manager=self.user)
        token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        self.client.force_authenticate(user=self.user, token=token)
        self.project_url = reverse('project-detail', args=[1])
        self.user_url = reverse('userprofile-detail', args=[1])

    def test_create_user_petition(self):
        self.client.force_authenticate(user=self.user)
        self.assertRaises(ObjectDoesNotExist,
                          Petition.objects.get, project=self.project)
        data = {'project': self.project_url,
                'task_start_date': self.start_date,
                'task_end_date': self.end_date, 'travel_info': [],
                'user': self.user_url,
                'movement_id': 'movement_id'}
        for model, url in PETITION_APIS.iteritems():
            data.update(EXTRA_DATA[model])
            response = self.client.post(url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            petitions = self.client.get(url)
            fields = model.APITravel.fields
            self.assertEqual(len(petitions.data), 1)
            created_petition = petitions.data[0]

            for field in created_petition:
                self.assertTrue(field in fields)

    def test_status_400_petition(self):
        required_fields = ('project', 'travel_info')
        self.assertRaises(ObjectDoesNotExist,
                          Petition.objects.get, project=self.project)
        data = {'project': self.project_url, 'travel_info': [],
                'task_start_date': self.start_date,
                'task_end_date': self.end_date}
        url = reverse('userpetition-list')
        for field in required_fields:
            value = data.pop(field)
            response = self.client.post(url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertEqual(response.data,
                             {field: ['This field is required.']})
            data[field] = value

        city_url = reverse('city-detail', args=[1])
        travel_info = [{'arrival_point': city_url,
                        'departure_point': city_url,
                        'accommodation_cost': float('inf')}]
        data['travel_info'] = travel_info
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        validation_message = 'Accomondation cost inf for petition with DSE' +\
            ' 1 exceeds the max overnight cost.'
        self.assertEqual(response.data,
                         {'non_field_errors': [validation_message]})

    def test_submission_apis(self):
        data = {'project': self.project_url,
                'task_start_date': self.start_date,
                'task_end_date': self.end_date, 'travel_info': [],
                'reason': 'reason',
                'movement_id': 'movement_id'
                }
        for model, url in SUBMISSION_APIS.iteritems():
            data.update(EXTRA_DATA[model])
            for field, attrs in model.APITravel.extra_kwargs.iteritems():
                response = self.client.post(url, data, format='json')
                self.assertEqual(response.status_code, status.HTTP_201_CREATED)
                if attrs.get('required', False):
                    value = data.pop(field)
                    response = self.client.post(url, data, format='json')
                    self.assertEqual(response.status_code,
                                     status.HTTP_400_BAD_REQUEST)
                    self.assertEqual(response.data, {
                        field: ['This field is required.']})
                    data[field] = value

    def test_submission_permissions(self):
        data = {'project': self.project_url,
                'task_start_date': self.start_date,
                'task_end_date': self.end_date, 'travel_info': [],
                'movement_id': 'movement_id'
                }
        for model, url in SUBMISSION_APIS.iteritems():
            data.update(EXTRA_DATA[model])
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
        city_url = reverse('city-detail', args=[1])
        for model, url in PETITION_APIS.iteritems():
            travel_info = [{'arrival_point': city_url,
                            'departure_point': city_url,
                            'transport_days_manual': sys.maxint}]
            data = {'project': self.project_url,
                    'task_start_date': self.start_date,
                    'task_end_date': self.end_date,
                    'travel_info': travel_info,
                    'user': self.user_url,
                    'movement_id': 'movement_id'}
            data.update(EXTRA_DATA[model])
            response = self.client.post(url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertEqual(response.data, {
                u'non_field_errors':
                [u'You have exceeded the allowable number of trip days']
            })
            travel_info[0].pop('transport_days_manual')

            # Check nested creation.
            data = {'project': self.project_url,
                    'task_start_date': self.start_date,
                    'task_end_date': self.end_date,
                    'travel_info': travel_info,
                    'user': self.user_url,
                    'movement_id': 'movement_id'}
            data.update(EXTRA_DATA[model])
            response = self.client.post(url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            petition = response.data
            petition_url = petition['url']
            travel_info = petition['travel_info']
            self.assertEqual(len(travel_info), 1)
            response = self.client.get(travel_info[0]['url'])
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            for field in response.data:
                self.assertTrue(field in TravelInfo.APITravel.fields)

            # Check nested updates.
            accommodation_cost = 10
            travel_info = [{'arrival_point': city_url,
                            'departure_point': city_url,
                            'accommodation_cost': accommodation_cost},
                           {'arrival_point': city_url,
                            'departure_point': city_url}]
            data['travel_info'] = travel_info
            response = self.client.put(
                petition_url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            petition = response.data
            travel_info = petition['travel_info']
            self.assertEqual(len(travel_info), 2)
            response = self.client.get(travel_info[0]['url'])
            self.assertEqual(response.data['accommodation_cost'],
                             accommodation_cost)
            response = self.client.get(travel_info[1]['url'])
            self.assertEqual(response.data['accommodation_cost'], 0.0)
