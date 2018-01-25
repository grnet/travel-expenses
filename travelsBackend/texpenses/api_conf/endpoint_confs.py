from texpenses.models import Petition
from rest_framework.filters import DjangoFilterBackend, SearchFilter
from texpenses.validators import required_validator
from texpenses.pagination import TexpensesPagination
from texpenses.filters import PetitionFilter
from texpenses.models import common
from texpenses.permissions.permission_rules import PERMISSION_RULES
from texpenses.api_conf.spec.spec import (countries_conf, city_conf, user_conf,
                                          tax_office_conf, project_conf,
                                          applications,
                                          travel_info)
import functools
import copy


class Configuration(object):

    def __init__(self, spec):
        self.spec = spec
        self.currencies = map((lambda x: tuple(x)), common.CURRENCIES)
        self.categories = map((lambda x: tuple(x)), common.CATEGORIES)
        self.specialties = map((lambda x: tuple(x)), common.SPECIALTY)
        self.kinds = map((lambda x: tuple(x)), common.KIND)
        self.user_categories = map((lambda x: tuple(x)), common.USER_CATEGORIES)
        self.payment_ways = map((lambda x: tuple(x)), common.WAYS_OF_PAYMENT)
        self.transportation = map((lambda x: tuple(x)), common.TRANSPORTATION)
        self.meals = map((lambda x: tuple(x)), common.MEALS)

    def apply_permissions(self):
        self.spec['api']['.endpoint']['permissions'] = PERMISSION_RULES

    def _inject_choices_petition_fields(self, endpoint):

        values, names = zip(*self.specialties)
        endpoint['*']['specialty']['.choices']['allowed'] = values
        endpoint['*']['specialty']['.choices']['display'] = names

        values, names = zip(*self.kinds)
        endpoint['*']['kind']['.choices']['allowed'] = values
        endpoint['*']['kind']['.choices']['display'] = names

        values, names = zip(*self.user_categories)
        endpoint['*']['user_category']['.choices']['allowed'] = values
        endpoint['*']['user_category']['.choices']['display'] = names

        currency_values, currency_names = zip(*self.currencies)
        endpoint['*']['participation_local_currency']\
            ['.choices']['allowed'] = currency_values
        endpoint['*']['participation_local_currency']\
            ['.choices']['display'] = currency_names

        payment_values, payment_names = zip(*self.payment_ways)
        endpoint['*']['participation_payment_way']\
            ['.choices']['allowed'] = payment_values
        endpoint['*']['participation_payment_way']\
            ['.choices']['display'] = payment_names

        endpoint['*']['travel_info']['.structarray']\
            ['accommodation_local_currency']\
            ['.choices']['allowed'] = currency_values
        endpoint['*']['travel_info']['.structarray']\
            ['accommodation_local_currency']\
            ['.choices']['display'] = currency_names

        endpoint['*']['travel_info']['.structarray']\
            ['accommodation_payment_way']\
            ['.choices']['allowed'] = payment_values
        endpoint['*']['travel_info']['.structarray']\
            ['accommodation_payment_way']\
            ['.choices']['display'] = payment_names

        endpoint['*']['travel_info']['.structarray']\
            ['transportation_payment_way']['.choices']\
            ['allowed'] = payment_values
        endpoint['*']['travel_info']['.structarray']\
            ['transportation_payment_way']['.choices']\
            ['display'] = payment_names

        values, names = zip(*self.transportation)
        endpoint['*']['travel_info']['.structarray']\
            ['means_of_transport']['.choices']\
            ['allowed'] = values
        endpoint['*']['travel_info']['.structarray']\
            ['means_of_transport']['.choices']\
            ['display'] = names

        values, names = zip(*self.meals)
        endpoint['*']['travel_info']['.structarray']\
            ['meals']['.choices']['allowed'] = values
        endpoint['*']['travel_info']['.structarray']\
            ['meals']['.choices']['allowed'] = values

    def _inject_standard_configuration(self, endpoint):
        endpoint['.drf_collection']['pagination_class'] = TexpensesPagination
        endpoint['.drf_collection']['filter_class'] = PetitionFilter
        endpoint['.drf_collection']['filter_backends'] = (DjangoFilterBackend,
                                                          SearchFilter,)

    def CountriesConfig(self):
        endpoint = countries_conf
        endpoint['*']['currency']['.choices']['allowed'] = self.currencies
        endpoint['*']['category']['.choices']['allowed'] = self.categories
        self.spec['api']['countries'] = endpoint

    def CitiesConfig(self):
        endpoint = city_conf
        endpoint['*']['country']['.struct']['currency']\
            ['.choices']['allowed'] = self.currencies
        endpoint['*']['country']['.struct']['category']\
            ['.choices']['allowed'] = self.categories
        self.spec['api']['city'] = endpoint

    def UsersConfig(self):
        endpoint = user_conf
        endpoint['*']['specialty']['.choices']['allowed'] = self.specialties
        endpoint['*']['kind']['.choices']['allowed'] = self.kinds
        endpoint['*']['user_category']['.choices']['allowed'] = (
            self.user_categories)

        self.spec['api']['users'] = endpoint

    def TaxOfficeConfig(self):
        self.spec['api']['tax-office'] = tax_office_conf

    def ProjectConfig(self):
        self.spec['api']['project'] = project_conf

    def ApplicationConfig(self):

        applications['*']['travel_info'] = copy.deepcopy(travel_info)
        endpoint = copy.deepcopy(applications)

        validator = functools.partial(required_validator,
                                      fields=Petition.USER_FIELDS)
        endpoint['*']['user']['.drf_field']['validators'] = [validator]
        self._inject_standard_configuration(endpoint)
        self._inject_choices_petition_fields(endpoint)
        self.spec['api']['applications'] = endpoint

    def configure_spec(self):
        self.apply_permissions()
        self.TaxOfficeConfig()
        self.ProjectConfig()
        self.UsersConfig()
        self.CitiesConfig()
        self.CountriesConfig()
        self.ApplicationConfig()
