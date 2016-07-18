from datetime import datetime, timedelta
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.test import APITestCase
from texpenses.models import (
    City, TravelInfo, Petition, UserPetition, Project, UserProfile, TaxOffice,
    UserPetitionSubmission, SecretaryPetition, SecretaryPetitionSubmission)


PETITION_APIS = {
    UserPetition: '/api/petition/user_petition/',
    UserPetitionSubmission: '/api/petition/submitted/',
    SecretaryPetition: '/api/petition/secretary_petition/',
    SecretaryPetitionSubmission: '/api/petition/secretary_submitted/'
}

SUBMISSION_APIS = {
    UserPetitionSubmission: '/api/petition/submitted/',
    SecretaryPetitionSubmission: '/api/petition/secretary_submitted/'
}


def get_url(view, lookup=''):
    url = reverse(view)
    return url + lookup + '/' if lookup else url


class APIPetitionTest(APITestCase):
    end_date = datetime.now() + timedelta(days=7)
    start_date = datetime.now() + timedelta(days=5)

    def setUp(self):
        tax_office = TaxOffice.objects.create(
            name='test', description='test', address='test',
            email='test@example.com', phone='2104344444')
        self.user = UserProfile.objects.create(
            first_name='Nick', last_name='Jones', email='test@email.com',
            iban='GR4902603280000910200635494',
            specialty='1', tax_reg_num=150260153,
            tax_office=tax_office, category='A',
            trip_days_left=5)
        self.city = City.objects.create(name='Athens')
        self.project = Project.objects.create(name='Test Project',
                                              accounting_code=1)
        self.client.force_authenticate(user=self.user)
        self.project_url = get_url('project-list', str(self.project.id))
        self.user_url = '/api/users_related/users/1/'

    def test_create_user_petition(self):
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
        url = '/api/petition/user_petition/'
        required_fields = ('project', 'task_start_date', 'task_end_date',
                           'additional_data')
        project_url = get_url('project-list', str(self.project.id))
        self.assertRaises(ObjectDoesNotExist,
                          Petition.objects.get, project=self.project)
        data = {'project': project_url, 'task_start_date': self.start_date,
                'task_end_date': self.end_date, 'additional_data': []}
        for field in required_fields:
            value = data.pop(field)
            response = self.client.post(url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertEqual(response.data,
                             {field: ['This field is required.']})
            data[field] = value

        city_url = get_url('city-list', str(self.city.id))
        additional_data = [{'arrival_point': city_url,
                            'departure_point': city_url,
                            'accomondation_price': float('inf')}]
        data['additional_data'] = additional_data
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        validation_message = 'Accomondation price inf for petition with DSE' +\
                ' 1 exceeds the max overnight cost.'
        self.assertEqual(response.data,
                         {'non_field_errors': [validation_message]})

    def test_submission_apis(self):
        UserPetitionSubmission.required_fields = ('participation_cost',)
        SecretaryPetitionSubmission.required_fields = ('participation_cost',)
        data = {'project': self.project_url,
                'task_start_date': self.start_date,
                'task_end_date': self.end_date, 'additional_data': [],
                'participation_cost': 10.0}
        for model, url in SUBMISSION_APIS.iteritems():
            response = self.client.post(url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            participation_cost = data.pop('participation_cost')
            response = self.client.post(url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertEqual(response.data,  {
                'non_field_errors': [
                    'Field %s is required' % repr('participation_cost')]})
            data['participation_cost'] = participation_cost

    def test_nested_serialization(self):
        UserPetitionSubmission.required_fields = ()
        SecretaryPetitionSubmission.required_fields = ()
        city_url = get_url('city-list', str(self.city.id))
        additional_data = [{'arrival_point': city_url,
                            'departure_point': city_url}]
        for model, url in PETITION_APIS.iteritems():
            additional_data = [{'arrival_point': city_url,
                                'departure_point': city_url}]
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
            accomondation_price = 10
            additional_data = [{'arrival_point': city_url,
                                'departure_point': city_url,
                                'accomondation_price': accomondation_price},
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
            self.assertEqual(response.data['accomondation_price'],
                             accomondation_price)
            response = self.client.get(travel_info[1])
            self.assertEqual(response.data['accomondation_price'], 0.0)
