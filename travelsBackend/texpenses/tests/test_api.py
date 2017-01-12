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

config = load_config(settings.APIMAS_CONFIG_PATH,
                     settings.APIMAS_CONFIG_NAME)

spec = config.get('spec')
spec['.endpoint']['permissions'] = PERMISSION_RULES

configuration = Configuration(spec)
configuration.configure_spec()


PETITION_COLLECTIONS = [
    'petition/user/saved',
]


@set_apimas_context(__name__, spec)
class TestApi(ApimasTestCase):

    def setUp_collection(self, collection, action):
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
        token = Token.objects.create(user=self.user)
        self.client.force_authenticate(user=self.user, token=token)
        collection_instances = super(
            TestApi, self).setUp_collection(collection, action)
        # if collection in PETITION_COLLECTIONS:
            # TravelInfo.objects.create(petition=collection_instances[0])

    # def request_context(collection, action, instances):
        # url, data, content_type = super(
            # TestApi, self).request_context(collection,
                                           # action,
                                           # instances)
        # if collection in C

    # def validate_response(self, collection, action, response, data,
                          # response_spec, instances):
        # if action == 'partial_update':
            # self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # else:
            # super()

   # def validate_response_partial_update_petition(self, collection,
                                                 # action, response, data,
                                                 # response_spec, instances):
       # pass
