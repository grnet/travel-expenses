from apimas.modeling.core import documents as doc
from texpenses.models import Petition
from rest_framework import serializers
from texpenses.validators import required_validator
import functools


class Configuration(object):

    def __init__(self, spec):
        self.spec = spec

    def UserPetitionConfig(self):
        endpoint = self.spec['api']['petition/user/saved']
        doc.doc_set(endpoint, ['*', 'dse', '.drf_field', 'required'], False)
        doc.doc_set(endpoint, ['*', 'dse', '.drf_field', 'allow_null'], True)
        doc.doc_set(endpoint, ['*', 'status', '.drf_field', 'default'],
                    Petition.SAVED_BY_USER)
        doc.doc_set(
            endpoint, ['*', 'task_start_date', '.drf_field', 'required'],
            False)
        doc.doc_set(endpoint, ['*', 'task_end_date', '.drf_field', 'required'],
                    False)
        doc.doc_set(endpoint, ['*', 'travel_info', '.drf_field', 'required'],
                    False)
        doc.doc_set(endpoint, ['*', 'user', '.drf_field', 'default'],
                    serializers.CurrentUserDefault())
        doc.doc_set(endpoint, ['*', 'user', '.drf_field', 'validators'],
                    [functools.partial(required_validator,
                                       fields=Petition.USER_FIELDS)])

    def UserPetitionSubmitConfig(self):
        endpoint = self.spec['api']['petition/user/submitted']
        doc.doc_set(endpoint, ['*', 'reason', '.drf_field', 'required'], True)
        doc.doc_set(endpoint, ['*', 'reason', '.drf_field', 'allow_blank'],
                    False)
        doc.doc_set(endpoint, ['*', 'reason', '.drf_field', 'allow_null'],
                    False)

        doc.doc_set(endpoint, ['*', 'dse', '.drf_field', 'required'], False)
        doc.doc_set(endpoint, ['*', 'dse', '.drf_field', 'allow_null'], True)

        doc.doc_set(endpoint, ['*', 'status', '.drf_field', 'default'],
                    Petition.SUBMITTED_BY_USER)
        doc.doc_set(
            endpoint, ['*', 'task_start_date', '.drf_field', 'required'],
            True)

        doc.doc_set(
            endpoint, ['*', 'task_start_date', '.drf_field', 'allow_null'],
            False)
        doc.doc_set(endpoint, ['*', 'task_end_date', '.drf_field', 'required'],
                    True)
        doc.doc_set(endpoint, ['*', 'task_end_date', '.drf_field',
                               'allow_null'], False)
        doc.doc_set(endpoint, ['*', 'travel_info', '.drf_field', 'required'],
                    False)
        doc.doc_set(endpoint, ['*', 'user', '.drf_field', 'default'],
                    serializers.CurrentUserDefault())
        doc.doc_set(endpoint, ['*', 'user', '.drf_field', 'validators'],
                    [functools.partial(required_validator,
                                       fields=Petition.USER_FIELDS)])
        doc.doc_set(endpoint, ['*', 'travel_info', '.structarray',
                               'arrival_point', '.drf_field', 'required'],
                    True)
        doc.doc_set(endpoint, ['*', 'travel_info', '.structarray',
                               'arrival_point', '.drf_field', 'allow_null'],
                    False)

        doc.doc_set(endpoint, ['*', 'travel_info', '.structarray',
                               'departure_point', '.drf_field', 'required'],
                    True)
        doc.doc_set(endpoint, ['*', 'travel_info', '.structarray',
                               'departure_point', '.drf_field', 'allow_null'],
                    False)

    def configure_spec(self):
        self.UserPetitionConfig()
        self.UserPetitionSubmitConfig()
