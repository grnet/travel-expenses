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
        doc.doc_set(endpoint, ['*', 'status', '.drf_field', 'default'],
                    Petition.SAVED_BY_USER)
        doc.doc_set(endpoint, ['*', 'user', '.drf_field', 'default'],
                    serializers.CurrentUserDefault())
        doc.doc_set(endpoint, ['*', 'user', '.drf_field', 'validators'],
                    [functools.partial(required_validator,
                                       fields=Petition.USER_FIELDS)])

    def UserPetitionSubmitConfig(self):
        endpoint = self.spec['api']['petition/user/submitted']
        doc.doc_set(endpoint, ['*', 'status', '.drf_field', 'default'],
                    Petition.SUBMITTED_BY_USER)
        doc.doc_set(endpoint, ['*', 'user', '.drf_field', 'default'],
                    serializers.CurrentUserDefault())
        doc.doc_set(endpoint, ['*', 'user', '.drf_field', 'validators'],
                    [functools.partial(required_validator,
                                       fields=Petition.USER_FIELDS)])

    def SecretaryPetitionSaveConfig(self):

        endpoint = self.spec['api']['petition/secretary/saved']

        doc.doc_set(endpoint, ['*', 'user', '.drf_field', 'validators'],
                    [functools.partial(required_validator,
                                       fields=Petition.USER_FIELDS)])

        doc.doc_set(endpoint, ['*', 'status', '.drf_field', 'default'],
                    Petition.SAVED_BY_SECRETARY)

    def configure_spec(self):
        self.UserPetitionConfig()
        self.UserPetitionSubmitConfig()
        self.SecretaryPetitionSaveConfig()
