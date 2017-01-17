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
from texpenses.models import Petition

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
        super(TestApi, self).setUp()

    def setUp_collection(self, collection, action):
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
