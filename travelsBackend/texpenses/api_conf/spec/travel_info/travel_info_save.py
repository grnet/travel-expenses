from django.conf import settings

spec = {'.cli_option': {},
        '.drf_field': {'required': False},
        '.field': {},
        '.structarray': {'accommodation_cost': {'.cli_option': {},
                                                '.drf_field': {},
                                                '.field': {},
                                                '.decimal': {'max_digits': settings.DECIMAL_MAX_DIGITS,
                                                             'decimal_places':settings.DECIMAL_PLACES}},
                        'accommodation_total_cost': {
                            '.cli_option': {},
                            '.drf_field': {},
                            '.field': {},
                            '.decimal': {
                                'max_digits': settings.DECIMAL_MAX_DIGITS,
                                'decimal_places':settings.DECIMAL_PLACES
                            }
                        },
                         'accommodation_default_currency': {'.cli_option': {},
                                                            '.drf_field': {},
                                                            '.field': {},
                                                            '.readonly': {},
                                                            '.string': {}},
                         'accommodation_local_cost': {'.cli_option': {},
                                                      '.drf_field': {},
                                                      '.field': {},
                                                      '.decimal': {'max_digits': settings.DECIMAL_MAX_DIGITS,
                                                                   'decimal_places':settings.DECIMAL_PLACES}},
                         'accommodation_local_currency': {'.choices': {},
                                                          '.cli_option': {},
                                                          '.drf_field': {},
                                                          '.field': {}},
                         'accommodation_payment_description': {'.cli_option':
                                                               {},
                                                               '.drf_field':
                                                               {},
                                                               '.field': {},
                                                               '.string': {}},
                         'accommodation_payment_way': {'.choices': {},
                                                       '.cli_option': {},
                                                       '.drf_field': {},
                                                       '.field': {}},
                         'arrival_point': {'.cli_option': {},
                                           '.drf_field': {},
                                           '.field': {},
                                           '.ref': {'to': 'api/city'}},
                         'compensation_cost': {'.cli_option': {},
                                               '.drf_field': {},
                                               '.field': {},
                                               '.decimal': {'max_digits': settings.DECIMAL_MAX_DIGITS,
                                                            'decimal_places':settings.DECIMAL_PLACES}},
                         'compensation_days_manual': {'.cli_option': {},
                                                      '.drf_field': {},
                                                      '.field': {},
                                                      '.integer': {}},
                         'compensation_days_proposed': {'.cli_option': {},
                                                        '.drf_field': {},
                                                        '.field': {},
                                                        '.integer': {}},
                         'compensation_level': {'.cli_option': {},
                                                '.drf_field': {},
                                                '.field': {},
                                                '.decimal': {'max_digits': settings.DECIMAL_MAX_DIGITS,
                                                             'decimal_places':settings.DECIMAL_PLACES}},
                         'depart_date': {'.cli_option': {},
                                        '.datetime': {
                                            'input_formats': ['%Y-%m-%dT%H:%M']
                                        },
                                         '.drf_field': {},
                                         '.field': {}},
                         'departure_point': {'.cli_option': {},
                                             '.drf_field': {},
                                             '.field': {},
                                             '.ref': {'to': 'api/city'}},
                         'id': {'.cli_option': {},
                                '.drf_field': {},
                                '.field': {},
                                '.readonly': {},
                                '.serial': {}},
                         'meals': {'.choices': {},
                                   '.cli_option': {},
                                   '.drf_field': {},
                                   '.field': {}},
                         'means_of_transport': {'.choices': {},
                                                '.cli_option': {},
                                                '.drf_field': {},
                                                '.field': {}},
                         'overnight_cost': {'.cli_option': {},
                                            '.drf_field': {},
                                            '.field': {},
                                            '.decimal': {'max_digits': settings.DECIMAL_MAX_DIGITS,
                                                         'decimal_places':settings.DECIMAL_PLACES}},
                         'overnights_num_manual': {'.cli_option': {},
                                                   '.drf_field': {},
                                                   '.field': {},
                                                   '.integer': {}},
                         'return_date': {'.cli_option': {},
                                        '.datetime': {
                                            'input_formats': ['%Y-%m-%dT%H:%M']
                                        },
                                         '.drf_field': {},
                                         '.field': {}},
                         'same_day_return_task': {'.boolean': {},
                                                  '.cli_option': {},
                                                  '.drf_field': {},
                                                  '.field': {}},
                         'transport_days_manual': {'.cli_option': {},
                                                   '.drf_field': {},
                                                   '.field': {},
                                                   '.integer': {}},
                         'transport_days_proposed': {'.cli_option': {},
                                                     '.drf_field': {},
                                                     '.field': {},
                                                     '.integer': {}},
                         'transportation_cost': {'.cli_option': {},
                                                 '.drf_field': {},
                                                 '.field': {},
                                                 '.decimal': {'max_digits': settings.DECIMAL_MAX_DIGITS,
                                                              'decimal_places':settings.DECIMAL_PLACES}},
                         'transportation_default_currency': {'.cli_option': {},
                                                             '.drf_field': {},
                                                             '.field': {},
                                                             '.readonly': {},
                                                             '.string':
                                                             {'max_length': 3}
                                                             },
                         'transportation_payment_description': {'.cli_option':
                                                                {},
                                                                '.drf_field':
                                                                {},
                                                                '.field': {},
                                                                '.string': {}
                                                                },
                         'transportation_payment_way': {'.choices': {},
                                                        '.cli_option': {},
                                                        '.drf_field': {},
                                                        '.field': {}},
                         'is_abroad': {'.cli_option': {},
                                       '.drf_field': {},
                                       '.field': {},
                                       '.boolean': {}},
                         'distance': {'.cli_option': {},
                                      '.drf_field': {},
                                      '.field': {},
                                      '.float': {}},
                         'overnights_num_proposed': {'.cli_option': {},
                                                     '.drf_field': {},
                                                     '.field': {},
                                                     '.integer': {},
                                                     '.readonly': {}},

                         }}
