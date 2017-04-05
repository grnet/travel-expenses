from texpenses.api_conf.spec.petitions.petition_compensations \
    import spec as petition_user_compensation
from texpenses.api_conf.spec.petitions.petition_save \
    import spec as petition_save
from texpenses.api_conf.spec.petitions.petition_secretary_compensations \
    import spec as petition_secretary_compensation
from texpenses.api_conf.spec.petitions.petition_secretary_save \
    import spec as petition_secretary_save
from texpenses.api_conf.spec.petitions.petition_secretary_submit \
    import spec as petition_secretary_submit
from texpenses.api_conf.spec.petitions.petition_submit \
    import spec as petition_submit

from texpenses.api_conf.spec.travel_info.travel_info_compensations\
    import spec as travel_info_compensations
from texpenses.api_conf.spec.travel_info.travel_info_save\
    import spec as travel_info_save
from texpenses.api_conf.spec.travel_info.travel_info_submit\
    import spec as travel_info_submit
from texpenses.api_conf.spec.travel_info.travel_info_secretary_save\
    import spec as travel_info_secretary_save
from texpenses.api_conf.spec.travel_info.travel_info_secretary_submit\
    import spec as travel_info_secretary_submit
from texpenses.api_conf.spec.travel_info.travel_info_secretary_compensations\
    import spec as travel_info_secretary_compensations

spec = {'api': {'.endpoint': {},
                'city': {},
                'countries': {},
                'petition-secretary-compensations': {},
                'petition-secretary-saved': {},
                'petition-secretary-submitted': {},
                'petition-user-compensations': {},
                'petition-user-saved': {},
                'petition-user-submitted': {},
                'project': {},
                'tax-office': {},
                'users': {}}}

tax_office_conf = {'*': {'address': {'.cli_option': {},
                                     '.drf_field': {},
                                     '.field': {},
                                     '.string': {}},
                         'description': {'.cli_option': {},
                                         '.drf_field': {},
                                         '.field': {},
                                         '.string': {}},
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
                               '.string': {}},
                      'url': {'.drf_field': {}, '.identity': {},
                              '.readonly': {}}},
                '.cli_commands': {},
                '.collection': {},
                '.drf_collection': {'mixins':
                                    ["rest_framework_extensions."
                                     "cache.mixins.CacheResponseMixin"],
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
                   'rest_framework.permissions.DjangoModelPermissions',
                   'texpenses.permissions.custom_permissions.IsOwner']},
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
                               '.readonly': {},
                               '.struct': {'category': {'.choices': {},
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
                                           'url': {'.drf_field': {},
                                                   '.identity': {},
                                                   '.readonly': {}}}},
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

                   'timezone': {'.cli_option': {},
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
              ['rest_framework_extensions.cache.mixins.CacheResponseMixin',
               'texpenses.views.mixins.CityMixin'],
              'model': 'texpenses.models.City'},
             '.actions': {'.list': {}, '.retrieve': {}}}
