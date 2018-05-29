from texpenses.api_conf.spec.petitions.applications import spec as applications

from texpenses.api_conf.spec.travel_info.travel_info import (
    spec as travel_info)

spec = {'api': {'.endpoint': {},
                'city': {},
                'countries': {},
                'applications': {},
                'project': {},
                'tax-office': {},
                'users': {},
                'city-distances': {}}}

tax_office_conf = {'*': {'address': {'.cli_option': {},
                                     '.drf_field': {},
                                     '.field': {},
                                     '.string': {}},
                         'description': {'.cli_option': {},
                                         '.drf_field': {},
                                         '.field': {},
                                         '.string': {'max_length': 300}},
                         'email': {'.cli_option': {},
                                   '.drf_field': {},
                                   '.field': {},
                                   '.string': {}},
                         'id': {'.cli_option': {},
                                '.drf_field': {},
                                '.field': {},
                                '.readonly': {},
                                '.serial': {}},
                         'name': {'.cli_option': {},
                                  '.drf_field': {},
                                  '.field': {},
                                  '.string': {}},
                         'phone': {'.cli_option': {},
                                   '.drf_field': {},
                                   '.field': {},
                                   '.string': {}},
                         'url': {'.drf_field': {}, '.identity': {},
                                 '.readonly': {}}},
                   '.cli_commands': {},
                   '.collection': {},
                   '.drf_collection': {'mixins':
                                       ["rest_framework_extensions.cache."
                                        "mixins.CacheResponseMixin"],
                                       'model': 'texpenses.models.TaxOffice'},
                   '.actions': {'.list': {}, '.retrieve': {}}}

project_conf = {'*': {'accounting_code': {'.cli_option': {},
                                          '.drf_field': {},
                                          '.field': {},
                                          '.string': {}},
                      'id': {'.cli_option': {},
                             '.drf_field': {},
                             '.field': {},
                             '.readonly': {},
                             '.serial': {}},

                      'manager': {'.cli_option': {},
                                  '.drf_field': {},
                                  '.field': {},
                                  '.readonly': {},
                                  '.ref': {'to': 'api/users'}},
                      'name': {'.cli_option': {},
                               '.drf_field': {},
                               '.field': {},
                               '.string': {'max_length': 500}},
                      'url': {'.drf_field': {}, '.identity': {},
                              '.readonly': {}}},
                '.cli_commands': {},
                '.collection': {},
                '.drf_collection':
                {'authentication_classes':
                 ['rest_framework.authentication.SessionAuthentication',
                  'rest_framework.authentication.BasicAuthentication',
                  'rest_framework.authentication.TokenAuthentication'],
                 'mixins':
                 ["rest_framework_extensions."
                  "cache.mixins.CacheResponseMixin",
                  'texpenses.views.mixins.ProjectMixin'],
                 'model': 'texpenses.models.Project'},
                '.actions': {'.list': {}, '.retrieve': {}}}

user_conf = {'*': {'email': {'.cli_option': {},
                             '.drf_field': {},
                             '.field': {},
                             '.string': {}},
                   'first_name': {'.cli_option': {},
                                  '.drf_field': {},
                                  '.field': {},
                                  '.string': {}},
                   'iban': {'.cli_option': {},
                            '.drf_field': {},
                            '.field': {},
                            '.string': {}},
                   'kind': {'.choices': {},
                            '.cli_option': {},
                            '.drf_field': {},
                            '.field': {}},
                   'last_name': {'.cli_option': {},
                                 '.drf_field': {},
                                 '.field': {},
                                 '.string': {}},
                   'specialty': {'.choices': {},
                                 '.cli_option': {},
                                 '.drf_field': {},
                                 '.field': {}},
                   'tax_office': {'.cli_option': {},
                                  '.drf_field': {},
                                  '.field': {},
                                  '.readonly': {},
                                  '.ref': {'to': 'api/tax-office'}},
                   'tax_reg_num': {'.cli_option': {},
                                   '.drf_field': {},
                                   '.field': {},
                                   '.string': {}},
                   'trip_days_left': {'.cli_option': {},
                                      '.drf_field': {},
                                      '.field': {},
                                      '.integer': {},
                                      '.readonly': {}},
                   'user_category': {'.choices': {},
                                     '.cli_option': {},
                                     '.drf_field': {},
                                     '.field': {},
                                     '.readonly': {}},
                   'user_group': {'.cli_option': {},
                                  '.drf_field': {},
                                  '.field': {},
                                  '.nullable': {},
                                  '.readonly': {},
                                  '.string': {}},
                   'username': {'.cli_option': {},
                                '.drf_field': {},
                                '.field': {},
                                '.readonly': {},
                                '.string': {}}},
             '.cli_auth': {'format': 'yaml', 'schema': {'token': ['token']}},
             '.cli_commands': {},
             '.collection': {},
             '.drf_collection':
             {'authentication_classes':
              ['rest_framework.authentication.SessionAuthentication',
               'rest_framework.authentication.TokenAuthentication'],
              'model': 'texpenses.models.UserProfile',
              'permission_classes':
                  ['rest_framework.permissions.IsAuthenticated',
                   'rest_framework.permissions.DjangoModelPermissions']},
             '.actions': {'.list': {}, '.retrieve': {}}}

countries_conf = {'*': {'category': {'.choices': {},
                                     '.cli_option': {},
                                     '.drf_field': {},
                                     '.field': {},
                                     '.readonly': {}},
                        'currency': {'.choices': {},
                                     '.cli_option': {},
                                     '.drf_field': {},
                                     '.field': {},
                                     '.readonly': {}},
                        'id': {'.cli_option': {},
                               '.drf_field': {},
                               '.field': {},
                               '.readonly': {},
                               '.serial': {}},
                        'name': {'.cli_option': {},
                                 '.drf_field': {},
                                 '.field': {},
                                 '.readonly': {},
                                 '.string': {}},
                        'url': {'.drf_field': {}, '.identity': {},
                                '.readonly': {}}},
                  '.cli_commands': {},
                  '.collection': {},
                  '.drf_collection':
                  {'mixins':
                   ["rest_framework_extensions.cache.mixins."
                    "CacheResponseMixin"],
                   'model': 'texpenses.models.Country'},
                  '.actions': {'.list': {}, '.retrieve': {}}}

city_conf = {'*': {'country': {'.cli_option': {},
                               '.drf_field': {},
                               '.field': {},
                               '.ref': {
                                   'to': 'api/countries'
                               }},
                   'id': {'.cli_option': {},
                          '.drf_field': {},
                          '.field': {},
                          '.readonly': {},
                          '.serial': {}},
                   'name': {'.cli_option': {},
                            '.drf_field': {},
                            '.field': {},
                            '.string': {}},
                   'timezone': {'.cli_option': {},
                                '.drf_field': {},
                                '.field': {},
                                '.string': {}},
                   'url': {'.drf_field': {}, '.identity': {},
                           '.readonly': {}}},
             '.cli_commands': {},
             '.collection': {},
             '.drf_collection':
             {'mixins':
              ['rest_framework_extensions.cache.mixins.CacheResponseMixin',
               'texpenses.views.mixins.CityMixin'],
              'model': 'texpenses.models.City',
              'authentication_classes':
              ['rest_framework.authentication.SessionAuthentication',
               'rest_framework.authentication.TokenAuthentication'],
             },
             '.actions': {'.list': {},
                          '.retrieve': {},
                          '.create': {},
                          '.update': {}}}

city_distances_conf = {
    '.cli_commands': {},
    '.collection': {},
    '.drf_collection': {
        'mixins': [
            'rest_framework_extensions.cache.mixins.CacheResponseMixin'],
        'model': 'texpenses.models.CityDistances'
    },
    '.actions': {
        '.list': {},
        '.retrieve': {}
    },
    '*': {
        'id': {
            '.cli_option': {},
            '.drf_field': {},
            '.field': {},
            '.readonly': {},
            '.serial': {}
        },
       'url': {
            '.drf_field': {},
            '.identity': {},
            '.readonly': {}
        },
        'distance': {
            '.cli_option': {},
            '.drf_field': {},
            '.field': {},
            '.float': {}
        },
        'from_city': {
            '.cli_option': {},
            '.drf_field': {},
            '.field': {},
            '.readonly': {},
            '.ref': {
                'to': 'api/city'
            }
        },
        'to_city': {
            '.cli_option': {},
            '.drf_field': {},
            '.field': {},
            '.readonly': {},
            '.ref': {
                'to': 'api/city'
            }
        },
    }
}
