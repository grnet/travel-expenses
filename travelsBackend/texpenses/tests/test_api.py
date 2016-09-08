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
    Country, UserCompensation, UserCompensationSubmission)

PETITION_APIS = [
    (UserPetition, reverse('userpetition-list')),
    (UserPetitionSubmission, reverse('userpetitionsubmission-list')),
    (SecretaryPetition, reverse('secretarypetition-list')),
    (SecretaryPetitionSubmission, reverse('secretarypetitionsubmission-list')),
    (UserCompensation, reverse('usercompensation-list')),
    (UserCompensationSubmission,
     reverse('usercompensationsubmission-list')),
]

SUBMISSION_APIS = [
    (UserPetitionSubmission, reverse('userpetitionsubmission-list')),
    (SecretaryPetitionSubmission, reverse('secretarypetitionsubmission-list'))
]

COMPENSATION_APIS = [
    (UserCompensation, reverse('usercompensation-list')),
    (UserCompensationSubmission,
     reverse('usercompensationsubmission-list')),
]

PROTOCOL_DATE_FORMAT = '%Y-%m-%d'
PROTOCOL_DATE = (datetime.now() + timedelta(days=1)).strftime(
    PROTOCOL_DATE_FORMAT)

TRAVEL_DATE_FORMAT = '%Y-%m-%dT%H:%M'
TRAVEL_DATE = (datetime.now() + timedelta(days=1)).strftime(
    TRAVEL_DATE_FORMAT)

EXTRA_DATA = {
    UserPetition: {},
    UserPetitionSubmission: {'reason': 'reason'},

    SecretaryPetition: {},
    SecretaryPetitionSubmission: {
        'additional_expenses_initial_description': 'test',
        'expenditure_protocol': 'expenditure protocol',
        'expenditure_date_protocol': PROTOCOL_DATE,
        'movement_protocol': 'movement protocol',
        'movement_date_protocol': PROTOCOL_DATE

    },
    UserCompensation: {},

    UserCompensationSubmission: {'travel_report': 'travel report'}
}
TRAVEL_INFO_MANDATORY_ELEMENTS = {
    'means_of_transport': 'AIR',
    'accommodation_cost': 80,
    'accommodation_payment_way': 'AGNT',
    'accommodation_payment_description': 'MPLAMPLA',
    'return_date': TRAVEL_DATE,
    'depart_date': TRAVEL_DATE,
    'transportation_cost': 300,
    'transportation_payment_way': 'AGNT',
    'transportation_payment_description': 'mplampla'
}

UserPetitionSubmission.mandatory_fields = ()
SecretaryPetitionSubmission.mandatory_fields = ()



class APIPetitionTest(APITestCase):
    end_date = datetime.now() + timedelta(days=7)
    start_date = datetime.now() + timedelta(days=5)

    def setUp(self):
        self.tax_office = TaxOffice.objects.create(
            name='test', description='test', address='test',
            email='test@example.com', phone='2104344444')
        self.user = UserProfile.objects.create_superuser(
            username='nick', first_name='Nick', last_name='Jones',
            email='test@email.com',
            iban='GR4902603280000910200635494',
            password='test', kind='1',
            specialty='1', tax_reg_num=011111111,
            tax_office=self.tax_office, user_category='A',
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
        city_url = reverse('city-detail', args=[1])
        travel_info = [{'arrival_point': city_url,
                        'departure_point': city_url,
                        }]
        travel_info[0].update(TRAVEL_INFO_MANDATORY_ELEMENTS)
        self.data = {'project': self.project_url,
                     'task_start_date': self.start_date,
                     'task_end_date': self.end_date, 'travel_info': [],
                     'dse': None,
                     'user': self.user_url,
                     'movement_id': 'movement_id',
                     'travel_info': travel_info,
                    }

    def test_create_user_petition(self):
        self.assertRaises(ObjectDoesNotExist,
                          Petition.objects.get, project=self.project)
        for model, url in PETITION_APIS:
            self.data.update(EXTRA_DATA[model])
            response = self.client.post(url, self.data, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            petition_url = response.data['url']
            response = self.client.get(petition_url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            fields = model.Api.fields
            created_petition = response.data

            for field in created_petition:
                self.assertTrue(field in fields)
            if model != UserPetition:
                self.data['dse'] = response.data['dse']
                response = self.client.post(url, self.data, format='json')
                self.assertEqual(
                    response.status_code, status.HTTP_403_FORBIDDEN)

                self.data['dse'] = 100
                response = self.client.post(url, self.data, format='json')
                self.assertEqual(
                    response.status_code, status.HTTP_403_FORBIDDEN)
                self.data['dse'] = None

    def test_status_400_petition(self):
        required_fields = ('project',)
        self.assertRaises(ObjectDoesNotExist,
                          Petition.objects.get, project=self.project)
        url = reverse('userpetition-list')
        for field in required_fields:
            value = self.data.pop(field)
            response = self.client.post(url, self.data, format='json')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertEqual(response.data,
                             {field: ['This field is required.']})
            self.data[field] = value

        self.data['travel_info'][0].update(
                {'accommodation_cost': float('inf')})
        response = self.client.post(url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        validation_message = 'Accomondation cost inf for petition with DSE' +\
            ' 1 exceeds the max overnight cost.'
        self.assertEqual(response.data,
                         {'non_field_errors': [validation_message]})

    def test_submission_apis(self):
        for model, url in SUBMISSION_APIS:
            self.data.update(EXTRA_DATA[model])
            for field, attrs in model.Api.extra_kwargs.iteritems():
                response = self.client.post(url, self.data, format='json')
                self.assertEqual(response.status_code, status.HTTP_201_CREATED)
                if attrs.get('required', False):
                    value = self.data.pop(field)
                    response = self.client.post(url, self.data, format='json')
                    self.assertEqual(response.status_code,
                                     status.HTTP_400_BAD_REQUEST)
                    self.assertEqual(response.data, {
                        field: ['This field is required.']})
                    self.data[field] = value

    def test_submission_permissions(self):
        for model, url in SUBMISSION_APIS:
            self.data.update(EXTRA_DATA[model])
            response = self.client.post(url, self.data, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            # test put
            response = self.client.put(url, self.data, format='json')
            self.assertEqual(
                response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
            # test patch
            response = self.client.patch(url, self.data, format='json')
            self.assertEqual(
                response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
            # test delete
            response = self.client.delete(url, self.data, format='json')
            self.assertEqual(
                response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_compensation_apis(self):
        data = {'project': self.project_url,
                'task_start_date': self.start_date,
                'task_end_date': self.end_date, 'travel_info': [],
                'reason': 'reason',
                'dse': None,
                'user': self.user_url,
                'movement_id': 'movement_id'
                }
        for model, url in COMPENSATION_APIS:
            data.update(EXTRA_DATA[model])
            for field, attrs in model.Api.extra_kwargs.iteritems():
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

    def test_compensation_permissions(self):
        data = {'project': self.project_url,
                'task_start_date': self.start_date,
                'task_end_date': self.end_date, 'travel_info': [],
                'dse': None,
                'user': self.user_url,
                'movement_id': 'movement_id'
                }
        for model, url in COMPENSATION_APIS:
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

        for model, url in PETITION_APIS:
            travel_info = [{'arrival_point': city_url,
                            'departure_point': city_url,
                            'transport_days_manual': sys.maxint,
                            }]
            travel_info[0].update(TRAVEL_INFO_MANDATORY_ELEMENTS)

            data = {'dse': None,
                    'project': self.project_url,
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
                    'dse': None,
                    'movement_id': 'movement_id'}
            data.update(EXTRA_DATA[model])
            response = self.client.post(url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            petition = response.data
            petition_url = petition['url']
            travel_info = petition['travel_info']
            self.assertEqual(len(travel_info), 1)

            # Check nested updates.
            accommodation_cost = 10
            travel_info = [{'arrival_point': city_url,
                            'departure_point': city_url,
                            'accommodation_cost': accommodation_cost,
                            },
                           {'arrival_point': city_url,
                            'departure_point': city_url,
                            }]
            travel_info[0].update(TRAVEL_INFO_MANDATORY_ELEMENTS)
            travel_info[1].update(TRAVEL_INFO_MANDATORY_ELEMENTS)
            data['travel_info'] = travel_info
            response = self.client.put(
                petition_url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            petition = response.data
            travel_info = petition['travel_info']
            self.assertEqual(len(travel_info), 2)
            del data['travel_info'][1]
            response = self.client.put(
                petition_url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            petition = response.data
            travel_info = petition['travel_info']
            self.assertEqual(len(travel_info), 1)

    def test_submission_cancellation(self):
        submission_apis = [('userpetitionsubmission',
                            Petition.SUBMITTED_BY_USER),
                           ('secretarypetitionsubmission',
                            Petition.SUBMITTED_BY_SECRETARY),
                           ('usercompensationsubmission',
                            Petition.USER_COMPENSATION_SUBMISSION)]
        for base_name, petition_status in submission_apis:
            data = {'project': self.project,
                    'task_start_date': self.start_date,
                    'task_end_date': self.end_date,
                    'status': petition_status,
                    'dse': 1,
                    'user': self.user}
            petition = Petition.objects.create(**data)
            travel_info = TravelInfo.objects.create(
                arrival_point=self.city, departure_point=self.city,
                travel_petition=petition)
            petition.travel_info.add(travel_info)
            submission_endpoint = reverse(base_name + '-list')
            cancel_url = submission_endpoint + str(petition.id) + '/cancel/'
            response = self.client.post(cancel_url, format='json')
            self.assertEqual(response.status_code, status.HTTP_303_SEE_OTHER)
            response = self.client.get(dict(response.items())['location'],
                                       format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            petition.status = petition_status + 1
            petition.save()
            petition = Petition.objects.create(**data)

            cancel_url = submission_endpoint + str(petition.id) + '/cancel/'
            response = self.client.post(cancel_url, format='json')
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_petition_filtering_per_user(self):
        # create a petition from current user(save endpoint)
        url = reverse('userpetition-list')
        response = self.client.post(url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # get petition list
        response = self.client.get(url, format='json')

        # assert petition list contains one object
        self.assertEqual(len(response.data), 1)
        self.assertIn(self.user_url, response.data[0]['user'])

        # logout current user
        self.client.logout()

        # create a new user and login
        self.user = UserProfile.objects.create_superuser(
            username='kostas', first_name='Kostas', last_name='Nikolaou',
            email='test@email.com',
            kind='1',
            iban='GR4902603280000910200635494',
            password='test', specialty='1', tax_reg_num=135362340,
            tax_office=self.tax_office, user_category='A', trip_days_left=5)
        self.city = City.objects.create(
            name='Amsterdam', country=Country.objects.create(name='Holland'))
        self.project = Project.objects.create(name='Test Project 2',
                                              accounting_code=1,
                                              manager=self.user)
        token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        self.client.force_authenticate(user=self.user, token=token)
        self.project_url = reverse('project-detail', args=[2])
        self.user_url = reverse('userprofile-detail', args=[2])

        # create a new petition from current user(save endpoint)
        response = self.client.post(url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # get petition list
        response = self.client.get(url, format='json')

        # assert petition list contains one object
        self.assertEqual(len(response.data), 1)
        self.assertIn(self.user_url, response.data[0]['user'])
