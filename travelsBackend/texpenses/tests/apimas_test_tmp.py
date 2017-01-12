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
    Country, UserCompensation, SecretaryCompensation)
from django.contrib.auth.models import Group
PETITION_APIS = [
    (UserPetition, reverse('petition/user/saved-list')),
    (UserPetitionSubmission, reverse('petition/user/submitted-list')),
    (SecretaryPetition, reverse('petition/secretary/saved-list')),
]

SUBMISSION_APIS = [
    (UserPetitionSubmission, reverse('petition/user/submitted-list')),
    (SecretaryPetitionSubmission, reverse('petition/secretary/submitted-list'))
]

COMPENSATION_APIS = [
    (UserCompensation, reverse('petition/user/compensations-list')),
    (SecretaryCompensation, reverse('petition/secretary/compensations-list')),
]

PROTOCOL_DATE_FORMAT = '%Y-%m-%d'
PROTOCOL_DATE = (datetime.now() + timedelta(days=1)).strftime(
    PROTOCOL_DATE_FORMAT)

TRAVEL_DATE_FORMAT = '%Y-%m-%dT%H:%M'
TRAVEL_DEPART_DATE = (datetime.now() + timedelta(days=1)).strftime(
    TRAVEL_DATE_FORMAT)

TRAVEL_RETURN_DATE = (datetime.now() + timedelta(days=4)).strftime(
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
        'movement_date_protocol': PROTOCOL_DATE,
        'additional_expenses_initial': 100,
        'additional_expenses_initial_description': 'Test',
        'additional_expenses_default_currency': 'EUR',

    },
    UserCompensation: {},
    SecretaryCompensation: {},

}
TRAVEL_INFO_MANDATORY_ELEMENTS = {
    'means_of_transport': 'AIR',
    'accommodation_cost': 80,
    'accommodation_payment_way': 'AGNT',
    'accommodation_payment_description': 'MPLAMPLA',
    'return_date': TRAVEL_RETURN_DATE,
    'depart_date': TRAVEL_DEPART_DATE,
    'transportation_cost': 300,
    'transportation_payment_way': 'AGNT',
    'transportation_payment_description': 'mplampla',
}

UserPetitionSubmission.mandatory_fields = ()
SecretaryPetitionSubmission.mandatory_fields = ()


class APIPetitionTest(APITestCase):
    task_end_date = datetime.now() + timedelta(days=3)
    task_start_date = datetime.now() + timedelta(days=2)

    def setUp(self):

        self.testing_group = Group.objects.create(name='ADMIN')

        self.tax_office = TaxOffice.objects.create(
            name='test', description='test', address='test',
            email='test@example.com', phone='2104344444', id=1)
        self.user = UserProfile.objects.create_superuser(
            username='nick', first_name='Nick', last_name='Jones',
            email='test@email.com',
            iban='GR4902603280000910200635494',
            password='test', kind='1',
            specialty='1', tax_reg_num=011111111,
            tax_office=self.tax_office, user_category='A',
            trip_days_left=10)
        self.user.groups.add(self.testing_group)
        self.user.save()
        self.city = City.objects.create(
            name='Athens', country=Country.objects.create(name='Greece'))
        self.project = Project.objects.create(name='Test Project',
                                              accounting_code=1,
                                              manager_name=self.user.first_name,
                                              manager_surname=self.user.
                                              last_name,
                                              manager_email=self.user.email)
        token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        self.client.force_authenticate(user=self.user, token=token)
        self.project_url = reverse('resources/project-detail',
                                   args=[self.project.id])
        self.user_url = reverse('users-detail', args=[self.user.id])
        city_url = reverse('resources/city-detail', args=[self.city.id])
        travel_info = [{'arrival_point': city_url,
                        'departure_point': city_url,
                        }]
        travel_info[0].update(TRAVEL_INFO_MANDATORY_ELEMENTS)
        self.data = {'project': self.project_url,
                     'task_start_date': self.task_start_date,
                     'task_end_date': self.task_end_date, 'travel_info': [],
                     'dse': None,
                     'user': self.user_url,
                     'movement_id': 'movement_id',
                     'travel_info': travel_info,
                     }

    def test_create_user_petition(self):
        self.assertRaises(ObjectDoesNotExist,
                          Petition.objects.get, project=self.project)
        import pdb
        pdb.set_trace()

        for model, url in PETITION_APIS:
            self.data.update(EXTRA_DATA[model])
            response = self.client.post(url, self.data, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            petition_url = response.data['url']
            response = self.client.get(petition_url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            if model != UserPetition:
                self.data['dse'] = response.data['dse']
                response = self.client.post(url, self.data, format='json')
                self.assertEqual(
                    response.status_code, status.HTTP_403_FORBIDDEN)

                self.data['dse'] = self.data['dse'] + 7
                response = self.client.post(url, self.data, format='json')
                self.assertEqual(
                    response.status_code, status.HTTP_403_FORBIDDEN)
                self.data['dse'] = None

    def test_status_400_petition(self):
        required_fields = ('project',)
        self.assertRaises(ObjectDoesNotExist,
                          Petition.objects.get, project=self.project)
        url = reverse('petition/user/saved-list')
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

    def test_nested_serialization(self):
        city_url = reverse('resources/city-detail', args=[self.city.id])
        POSITIVE_SMALL_INTEGER = 32767

        for model, url in PETITION_APIS:
            travel_info = [{'arrival_point': city_url,
                            'departure_point': city_url,
                            'transport_days_manual': POSITIVE_SMALL_INTEGER,
                            }]
            travel_info[0].update(TRAVEL_INFO_MANDATORY_ELEMENTS)

            data = {'dse': None,
                    'project': self.project_url,
                    'task_start_date': self.task_start_date,
                    'task_end_date': self.task_end_date,
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
                    'task_start_date': self.task_start_date,
                    'task_end_date': self.task_end_date,
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
        submission_apis = [('petition/user/submitted',
                            Petition.SUBMITTED_BY_USER),
                           ('petition/secretary/submitted',
                            Petition.SUBMITTED_BY_SECRETARY)]
        for base_name, petition_status in submission_apis:
            data = {'project': self.project,
                    'task_start_date': self.task_start_date,
                    'task_end_date': self.task_end_date,
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
            response = self.client.get(dict(response.items())['Location'],
                                       format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            petition.status = petition_status + 2
            petition.save()
            petition = Petition.objects.create(**data)

            cancel_url = submission_endpoint + str(petition.id) + '/cancel/'
            response = self.client.post(cancel_url, format='json')

            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_petition_filtering_per_user(self):
        # create a petition from current user(save endpoint)
        url = reverse('petition/user/saved-list')
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
            tax_office=self.tax_office, user_category='A', trip_days_left=10)
        self.user.groups.add(self.testing_group)
        self.user.save()
        self.city = City.objects.create(
            name='Amsterdam', country=Country.objects.create(name='Holland'))
        self.project = Project.objects.create(name='Test Project 2',
                                              accounting_code=1,
                                              manager_name=self.user.first_name,
                                              manager_surname=self.user.
                                              last_name,
                                              manager_email=self.user.email)
        token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        self.client.force_authenticate(user=self.user, token=token)
        self.project_url = reverse(
            'resources/project-detail', args=[self.project.id])
        self.user_url = reverse('users-detail', args=[self.user.id])

        # create a new petition from current user(save endpoint)
        response = self.client.post(url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # get petition list
        response = self.client.get(url, format='json')

        # assert petition list contains one object
        self.assertEqual(len(response.data), 1)
        self.assertIn(self.user_url, response.data[0]['user'])
