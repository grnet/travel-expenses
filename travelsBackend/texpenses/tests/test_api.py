from apimas.modeling.adapters.drf.testing import (
    ApimasTestCase, set_apimas_context)
from apimas.modeling.utils import load_config
from texpenses.permissions.permission_rules import PERMISSION_RULES
from texpenses.api_conf.endpoint_confs import Configuration
from django.conf import settings
from texpenses.models import (
    City, TravelInfo, Petition, UserPetition, Project, UserProfile, TaxOffice,
    UserPetitionSubmission, SecretaryPetition, SecretaryPetitionSubmission,
    Country, UserCompensation, SecretaryCompensation)
from django.contrib.auth.models import Group
from rest_framework.authtoken.models import Token
from texpenses.permissions.permission_rules import PERMISSION_RULES
from rest_framework import status
from datetime import datetime, timedelta
from django.core.urlresolvers import reverse


config = load_config(settings.APIMAS_CONFIG_PATH,
                     settings.APIMAS_CONFIG_NAME)

spec = config.get('spec')
spec['.endpoint']['permissions'] = PERMISSION_RULES

configuration = Configuration(spec)
configuration.configure_spec()


def petition_user_save_conf(petition):
    pass


def petition_user_submit_conf(petition):
    petition['task_start_date'] = datetime.now() + timedelta(days=2)
    petition['task_end_date'] = datetime.now() + timedelta(days=3)


def petition_secretary_save_conf(petition):
    pass


def petition_secretary_submit_conf(petition):
    pass


def petition_user_compensation_conf(petition):
    pass


def petition_secretary_compensation_conf(petition):
    pass

PETITION_COLLECTIONS = {
    'petition/user/saved': [Petition.SAVED_BY_USER, petition_user_save_conf],
    'petition/user/submitted': [Petition.SUBMITTED_BY_USER,
                                petition_user_submit_conf],
    'petition/secretary/saved': [Petition.SAVED_BY_SECRETARY,
                                 petition_secretary_save_conf],
    'petition/secretary/submitted': [Petition.SUBMITTED_BY_SECRETARY,
                                     petition_secretary_submit_conf],

    'petition/user/compensations': [Petition.USER_COMPENSATION,
                                    petition_user_compensation_conf],

    'petition/secretary/compensations': [Petition.SECRETARY_COMPENSATION,
                                         petition_secretary_compensation_conf]
}


def test_partial_update(self):
    pass


@set_apimas_context(__name__, spec)
class TestApi(ApimasTestCase):

    def setUp(self):
        setattr(TestApi, 'test_partial_update_petition/user/saved',
                test_partial_update)
        setattr(TestApi, 'test_partial_update_petition/user/submitted',
                test_partial_update)
        setattr(TestApi, 'test_partial_update_petition/secretary/saved',
                test_partial_update)
        setattr(TestApi, 'test_partial_update_petition/secretary/submitted',
                test_partial_update)
        setattr(TestApi, 'test_partial_update_petition/user/compensations',
                test_partial_update)
        setattr(TestApi,
                'test_partial_update_petition/secretary/compensations',
                test_partial_update)
        self.testing_group = Group.objects.create(name='ADMIN')

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
            trip_days_left=10)
        self.user.groups.add(self.testing_group)
        token = Token.objects.create(user=self.user)
        self.client.force_authenticate(user=self.user, token=token)
        super(TestApi, self).setUp()

    def setUp_collection(self, collection, action):

        if collection == 'users':
            return [self.user]
        collection_instances = super(
            TestApi, self).setUp_collection(collection, action)
        if collection in PETITION_COLLECTIONS.keys() and action != 'create':
            TravelInfo.objects.create(
                travel_petition=collection_instances[0])
            collection_instances[0].deleted = False
            collection_instances[0].user = self.user
            collection_instances[0].status = PETITION_COLLECTIONS[collection][0]
            collection_instances[0].save()
        return collection_instances

    def request_context(self, collection, action, instances):

        url, data, content_type = super(
            TestApi, self).request_context(collection, action,
                                           instances)

        if collection in PETITION_COLLECTIONS.keys():
            PETITION_COLLECTIONS[collection][1](data)
        return url, data, content_type

    def validate_response(self, collection, action, response, data,
                          response_spec, instances):
        permission = (collection, action, self.user.user_group(), '*', '*',
                      '*')
        if permission not in PERMISSION_RULES:
            self.assertIn(response.status_code,
                          [status.HTTP_405_METHOD_NOT_ALLOWED,
                           status.HTTP_403_FORBIDDEN,
                           status.HTTP_204_NO_CONTENT])
        else:
            super(TestApi, self).validate_response(collection, action,
                                                   response,
                                                   data, response_spec,
                                                   instances)

    def _petition_submit_cancel(self, collection):

        project = Project.objects.create(name='Test Project',
                                         accounting_code=1,
                                         manager_name=self.user.first_name,
                                         manager_surname=self.user.
                                         last_name,
                                         manager_email=self.user.email)
        task_start_date = datetime.now() + timedelta(days=2)
        task_end_date = datetime.now() + timedelta(days=3)
        city = City.objects.create(
            name='Athens', country=Country.objects.create(name='Greece'))
        base_name, petition_status = collection,\
            PETITION_COLLECTIONS[collection][0]
        data = {'project': project,
                'task_start_date': task_start_date,
                'task_end_date': task_end_date,
                'status': petition_status,
                'dse': 1,
                'user': self.user}
        petition = Petition.objects.create(**data)
        travel_info = TravelInfo.objects.create(
            arrival_point=city, departure_point=city,
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

    def test_petition_user_submit_cancel(self):
        self._petition_submit_cancel('petition/user/submitted')

    def test_petition_secretary_submit_cancel(self):
        self._petition_submit_cancel('petition/secretary/submitted')

    def test_petition_secretary_submit_president_approval(self):

        collection = 'petition/secretary/submitted'

        project = Project.objects.create(name='Test Project',
                                         accounting_code=1,
                                         manager_name=self.user.first_name,
                                         manager_surname=self.user.
                                         last_name,
                                         manager_email=self.user.email)
        task_start_date = datetime.now() + timedelta(days=2)
        task_end_date = datetime.now() + timedelta(days=3)
        city = City.objects.create(
            name='Athens', country=Country.objects.create(name='Greece'))
        base_name, petition_status = collection,\
            PETITION_COLLECTIONS[collection][0]
        data = {'project': project,
                'task_start_date': task_start_date,
                'task_end_date': task_end_date,
                'status': petition_status,
                'dse': 1,
                'user': self.user}
        petition = Petition.objects.create(**data)
        travel_info = TravelInfo.objects.create(
            arrival_point=city, departure_point=city,
            travel_petition=petition)
        petition.travel_info.add(travel_info)
        submission_endpoint = reverse(base_name + '-list')
        approval_url = submission_endpoint + str(petition.id) +\
            '/president_approval/'
        response = self.client.post(approval_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        petition.status = 5
        petition.save()

        approval_url = submission_endpoint + str(petition.id) +\
            '/president_approval/'
        response = self.client.post(approval_url, format='json')

        self.assertEqual(response.status_code, status.HTTP_501_NOT_IMPLEMENTED)

    def _petition_secretary_submit_reports(self, report_name):

        collection = 'petition/secretary/submitted'

        project = Project.objects.create(name='Test Project',
                                         accounting_code=1,
                                         manager_name=self.user.first_name,
                                         manager_surname=self.user.
                                         last_name,
                                         manager_email=self.user.email)
        task_start_date = datetime.now() + timedelta(days=2)
        task_end_date = datetime.now() + timedelta(days=3)
        city = City.objects.create(
            name='Athens', country=Country.objects.create(name='Greece'))
        base_name, petition_status = collection,\
            PETITION_COLLECTIONS[collection][0]
        data = {'project': project,
                'task_start_date': task_start_date,
                'task_end_date': task_end_date,
                'status': petition_status,
                'dse': 1,
                'user': self.user}
        petition = Petition.objects.create(**data)
        travel_info = TravelInfo.objects.create(
            arrival_point=city, departure_point=city,
            travel_petition=petition)
        petition.travel_info.add(travel_info)
        submission_endpoint = reverse(base_name + '-list')
        ar_url = submission_endpoint + str(petition.id) + report_name
        response = self.client.get(ar_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_petition_secretary_submit_application_report(self):
        self._petition_secretary_submit_reports('/application_report/')

    def test_petition_secretary_submit_decision_report(self):
        self._petition_secretary_submit_reports('/decision_report/')

    def test_user_compensation_submit(self):
        collection = 'petition/user/compensations'

        project = Project.objects.create(name='Test Project',
                                         accounting_code=1,
                                         manager_name=self.user.first_name,
                                         manager_surname=self.user.
                                         last_name,
                                         manager_email=self.user.email)
        task_start_date = datetime.now() + timedelta(days=2)
        task_end_date = datetime.now() + timedelta(days=3)

        depart_date = task_start_date - timedelta(days=1)
        return_date = task_end_date + timedelta(days=1)
        city = City.objects.create(
            name='Athens', country=Country.objects.create(name='Greece'))
        base_name, petition_status = collection,\
            PETITION_COLLECTIONS[collection][0]
        data = {'project': project,
                'task_start_date': task_start_date,
                'task_end_date': task_end_date,
                'status': petition_status,
                'dse': 1,
                'user': self.user,
                'expenditure_date_protocol': datetime.now(),
                'expenditure_protocol': '1234',
                'movement_date_protocol': datetime.now(),
                'movement_protocol': '4321',
                'participation_local_currency': 'e',
                'reason': '12312321',
                'travel_report': 'sadsadsa'
                }
        petition = Petition.objects.create(**data)
        travel_info = TravelInfo.objects.create(
            arrival_point=city, departure_point=city,
            travel_petition=petition, depart_date=depart_date,
            return_date=return_date, transportation_cost=60,
            transportation_payment_description='dsadsa',
            accommodation_cost=60,
            accommodation_local_currency='e',
            accommodation_payment_description='sdsds')
        petition.travel_info.add(travel_info)
        submission_endpoint = reverse(base_name + '-list')
        submit_url = submission_endpoint + str(petition.id) + '/submit/'
        response = self.client.post(submit_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_303_SEE_OTHER)

    def test_secretary_compensation_submit(self):
        collection = 'petition/secretary/compensations'

        project = Project.objects.create(name='Test Project',
                                         accounting_code=1,
                                         manager_name=self.user.first_name,
                                         manager_surname=self.user.
                                         last_name,
                                         manager_email=self.user.email)
        task_start_date = datetime.now() + timedelta(days=2)
        task_end_date = datetime.now() + timedelta(days=3)

        depart_date = task_start_date - timedelta(days=1)
        return_date = task_end_date + timedelta(days=1)
        city = City.objects.create(
            name='Athens', country=Country.objects.create(name='Greece'))
        base_name, petition_status = collection,\
            PETITION_COLLECTIONS[collection][0]
        data = {'project': project,
                'task_start_date': task_start_date,
                'task_end_date': task_end_date,
                'status': petition_status,
                'dse': 1,
                'user': self.user,
                'expenditure_date_protocol': datetime.now(),
                'expenditure_protocol': '1234',
                'movement_date_protocol': datetime.now(),
                'movement_protocol': '4321',
                'participation_local_currency': 'e',
                'reason': '12312321',
                'travel_report': 'sadsadsa',
                'compensation_decision_date': datetime.now(),
                'compensation_decision_protocol': '5678',
                'compensation_petition_date': datetime.now(),
                'compensation_petition_protocol': '8765'
                }
        petition = Petition.objects.create(**data)
        travel_info = TravelInfo.objects.create(
            arrival_point=city, departure_point=city,
            travel_petition=petition, depart_date=depart_date,
            return_date=return_date, transportation_cost=60,
            transportation_payment_description='dsadsa',
            accommodation_cost=60,
            accommodation_local_currency='e',
            accommodation_payment_description='sdsds')
        petition.travel_info.add(travel_info)
        submission_endpoint = reverse(base_name + '-list')
        save_url = submission_endpoint + str(petition.id) + '/submit/'
        response = self.client.post(save_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_303_SEE_OTHER)

    def test_secretary_compensation_president_approval(self):
        collection = 'petition/secretary/compensations'

        project = Project.objects.create(name='Test Project',
                                         accounting_code=1,
                                         manager_name=self.user.first_name,
                                         manager_surname=self.user.
                                         last_name,
                                         manager_email=self.user.email)
        task_start_date = datetime.now() + timedelta(days=2)
        task_end_date = datetime.now() + timedelta(days=3)

        depart_date = task_start_date - timedelta(days=1)
        return_date = task_end_date + timedelta(days=1)
        city = City.objects.create(
            name='Athens', country=Country.objects.create(name='Greece'))
        base_name, petition_status = collection,\
            PETITION_COLLECTIONS[collection][0]
        data = {'project': project,
                'task_start_date': task_start_date,
                'task_end_date': task_end_date,
                'status': Petition.SECRETARY_COMPENSATION_SUBMISSION,
                'dse': 1,
                'user': self.user,
                'expenditure_date_protocol': datetime.now(),
                'expenditure_protocol': '1234',
                'movement_date_protocol': datetime.now(),
                'movement_protocol': '4321',
                'participation_local_currency': 'e',
                'reason': '12312321',
                'travel_report': 'sadsadsa',
                'compensation_decision_date': datetime.now(),
                'compensation_decision_protocol': '5678',
                'compensation_petition_date': datetime.now(),
                'compensation_petition_protocol': '8765'
                }
        petition = Petition.objects.create(**data)
        travel_info = TravelInfo.objects.create(
            arrival_point=city, departure_point=city,
            travel_petition=petition, depart_date=depart_date,
            return_date=return_date, transportation_cost=60,
            transportation_payment_description='dsadsa',
            accommodation_cost=60,
            accommodation_local_currency='e',
            accommodation_payment_description='sdsds')
        petition.travel_info.add(travel_info)
        submission_endpoint = reverse(base_name + '-list')
        approval_url = submission_endpoint + str(petition.id) +\
            '/president_approval/'
        response = self.client.post(approval_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        petition.status = 10
        petition.save()

        approval_url = submission_endpoint + str(petition.id) +\
            '/president_approval/'
        response = self.client.post(approval_url, format='json')

        self.assertEqual(response.status_code, status.HTTP_501_NOT_IMPLEMENTED)

    def _compensation_report(self, report_name):
        collection = 'petition/secretary/compensations'

        project = Project.objects.create(name='Test Project',
                                         accounting_code=1,
                                         manager_name=self.user.first_name,
                                         manager_surname=self.user.
                                         last_name,
                                         manager_email=self.user.email)
        task_start_date = datetime.now() + timedelta(days=2)
        task_end_date = datetime.now() + timedelta(days=3)

        depart_date = task_start_date - timedelta(days=1)
        return_date = task_end_date + timedelta(days=1)
        city = City.objects.create(
            name='Athens', country=Country.objects.create(name='Greece'))
        base_name, petition_status = collection,\
            PETITION_COLLECTIONS[collection][0]
        data = {'project': project,
                'task_start_date': task_start_date,
                'task_end_date': task_end_date,
                'status': Petition.SECRETARY_COMPENSATION_SUBMISSION,
                'dse': 1,
                'user': self.user,
                'expenditure_date_protocol': datetime.now(),
                'expenditure_protocol': '1234',
                'movement_date_protocol': datetime.now(),
                'movement_protocol': '4321',
                'participation_local_currency': 'e',
                'reason': '12312321',
                'travel_report': 'sadsadsa',
                'compensation_decision_date': datetime.now(),
                'compensation_decision_protocol': '5678',
                'compensation_petition_date': datetime.now(),
                'compensation_petition_protocol': '8765'
                }
        petition = Petition.objects.create(**data)
        travel_info = TravelInfo.objects.create(
            arrival_point=city, departure_point=city,
            travel_petition=petition, depart_date=depart_date,
            return_date=return_date, transportation_cost=60,
            transportation_payment_description='dsadsa',
            accommodation_cost=60,
            accommodation_local_currency='e',
            accommodation_payment_description='sdsds')
        petition.travel_info.add(travel_info)
        submission_endpoint = reverse(base_name + '-list')
        approval_url = submission_endpoint + str(petition.id) + report_name
        response = self.client.get(approval_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_secretary_compensation_application_report(self):
        self._compensation_report('/application_report/')

    def test_secretary_compensation_decision_report(self):
        self._compensation_report('/decision_report/')

    def test_secretary_compensation_cancel(self):
        collection = 'petition/secretary/compensations'

        project = Project.objects.create(name='Test Project',
                                         accounting_code=1,
                                         manager_name=self.user.first_name,
                                         manager_surname=self.user.
                                         last_name,
                                         manager_email=self.user.email)
        task_start_date = datetime.now() + timedelta(days=2)
        task_end_date = datetime.now() + timedelta(days=3)

        depart_date = task_start_date - timedelta(days=1)
        return_date = task_end_date + timedelta(days=1)
        city = City.objects.create(
            name='Athens', country=Country.objects.create(name='Greece'))
        base_name, petition_status = collection,\
            PETITION_COLLECTIONS[collection][0]
        data = {'project': project,
                'task_start_date': task_start_date,
                'task_end_date': task_end_date,
                'status': Petition.SECRETARY_COMPENSATION_SUBMISSION,
                'dse': 1,
                'user': self.user,
                'expenditure_date_protocol': datetime.now(),
                'expenditure_protocol': '1234',
                'movement_date_protocol': datetime.now(),
                'movement_protocol': '4321',
                'participation_local_currency': 'e',
                'reason': '12312321',
                'travel_report': 'sadsadsa',
                'compensation_decision_date': datetime.now(),
                'compensation_decision_protocol': '5678',
                'compensation_petition_date': datetime.now(),
                'compensation_petition_protocol': '8765'
                }
        petition = Petition.objects.create(**data)
        travel_info = TravelInfo.objects.create(
            arrival_point=city, departure_point=city,
            travel_petition=petition, depart_date=depart_date,
            return_date=return_date, transportation_cost=60,
            transportation_payment_description='dsadsa',
            accommodation_cost=60,
            accommodation_local_currency='e',
            accommodation_payment_description='sdsds')
        petition.travel_info.add(travel_info)
        submission_endpoint = reverse(base_name + '-list')
        save_url = submission_endpoint + str(petition.id) + '/cancel/'
        response = self.client.post(save_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_303_SEE_OTHER)
        response = self.client.get(dict(response.items())['Location'],
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        petition.status = petition_status + 1
        petition.save()
        petition = Petition.objects.create(**data)

        cancel_url = submission_endpoint + str(petition.id) + '/cancel/'
        response = self.client.post(cancel_url, format='json')
