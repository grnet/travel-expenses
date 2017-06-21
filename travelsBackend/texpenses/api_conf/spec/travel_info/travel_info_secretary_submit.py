spec = {'.structarray': {'accommodation_cost': {'.cli_option': {},
                                                '.drf_field': {'allow_null':
                                                               False,
                                                               'required':
                                                               False},
                                                '.field': {},
                                                '.float': {}},
                         'accommodation_default_currency': {'.cli_option': {},
                                                            '.drf_field':
                                                            {'allow_blank':
                                                             False,
                                                             'allow_null':
                                                             False,
                                                             'required': True},
                                                            '.field': {},
                                                            '.readonly': {},
                                                            '.string': {}},
                         'accommodation_payment_description': {'.cli_option':
                                                               {},
                                                               '.drf_field':
                                                               {'allow_blank':
                                                                False,
                                                                'allow_null':
                                                                False,
                                                                'required':
                                                                True},
                                                               '.field': {},
                                                               '.string': {}},
                         'accommodation_payment_way': {'.choices': {},
                                                       '.cli_option': {},
                                                       '.drf_field':
                                                       {'allow_blank': False,
                                                        'allow_null': False,
                                                        'required': True},
                                                       '.field': {}},
                         'arrival_point': {'.cli_option': {},
                                           '.drf_field': {'allow_null': False,
                                                          'required': True},
                                           '.field': {},
                                           '.ref': {'to': 'api/city'}},
                         'compensation_days_proposed': {'.cli_option': {},
                                                        '.drf_field': {},
                                                        '.field': {},
                                                        '.integer': {},
                                                        '.readonly': {}},
                         'compensation_level': {'.cli_option': {},
                                                '.drf_field': {},
                                                '.field': {},
                                                '.float': {},
                                                '.readonly': {}},
                         'depart_date': {'.cli_option': {},
                                         '.datetime': {'format':
                                                       ['%Y-%m-%dT%H:%M']},
                                         '.drf_field': {'allow_null': False,
                                                        'required': True},
                                         '.field': {}},
                         'departure_point': {'.cli_option': {},
                                             '.drf_field': {'allow_null':
                                                            False,
                                                            'required': True},
                                             '.field': {},
                                             '.ref': {'to': 'api/city'}},
                         'means_of_transport': {'.choices': {},
                                                '.cli_option': {},
                                                '.drf_field': {'allow_blank':
                                                               False,
                                                               'allow_null':
                                                               False,
                                                               'required':
                                                               True},
                                                '.field': {}},
                         'overnights_num_proposed': {'.cli_option': {},
                                                     '.drf_field': {},
                                                     '.field': {},
                                                     '.integer': {},
                                                     '.readonly': {}},
                         'overnight_cost': {'.cli_option': {},
                                            '.drf_field': {},
                                            '.field': {},
                                            '.float': {},
                                            '.readonly': {}},
                         'return_date': {'.cli_option': {},
                                         '.datetime': {'format':
                                                       ['%Y-%m-%dT%H:%M']},
                                         '.drf_field': {'allow_null': False,
                                                        'required': True},
                                         '.field': {}},
                         'same_day_return_task': {'.boolean': {},
                                                  '.cli_option': {},
                                                  '.drf_field': {},
                                                  '.field': {},
                                                  '.readonly': {}},
                         'transport_days_proposed': {'.cli_option': {},
                                                     '.drf_field': {},
                                                     '.field': {},
                                                     '.integer': {},
                                                     '.readonly': {}},
                         'transportation_cost': {'.cli_option': {},
                                                 '.drf_field': {'allow_null':
                                                                False,
                                                                'required':
                                                                True,
                                                                'min_value': 1,
                                                                },
                                                 '.field': {},
                                                 '.float': {}},
                         'transportation_default_currency': {'.cli_option': {},
                                                             '.drf_field':
                                                             {'allow_blank':
                                                              False,
                                                              'allow_null':
                                                              False,
                                                              'required':
                                                              True},
                                                             '.field': {},
                                                             '.readonly': {},
                                                             '.string': {}},
                         'transportation_payment_description': {'.cli_option':
                                                                {},
                                                                '.drf_field':
                                                                {'allow_blank':
                                                                 False,
                                                                 'allow_null':
                                                                 False,
                                                                 'required':
                                                                 True},
                                                                '.field': {},
                                                                '.string': {}},
                         'transportation_payment_way': {'.choices': {},
                                                        '.cli_option': {},
                                                        '.drf_field':
                                                        {'allow_blank': False,
                                                         'allow_null': False,
                                                         'required': True},
                                                        '.field': {}}}}
