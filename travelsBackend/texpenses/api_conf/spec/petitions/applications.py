from django.conf import settings

spec = {'*': {


    'compensation_decision_date': {'.cli_option': {},
                                   '.datetime': {'format': '%Y-%m-%dT%H:%M'},
                                   '.drf_field': {},
                                   '.field': {}},
    'compensation_decision_protocol': {'.cli_option': {},
                                       '.drf_field': {},
                                       '.field': {},
                                       '.string': {}},
    'compensation_petition_date': {'.cli_option': {},
                                   '.drf_field': {},
                                   '.datetime': {'format': '%Y-%m-%dT%H:%M'},
                                   '.field': {}},
    'compensation_petition_protocol': {'.cli_option': {},
                                       '.drf_field': {},
                                       '.field': {},
                                       '.string': {}},
    'timesheeted': {'.cli_option': {},
                    '.drf_field': {'required': False},
                    '.field': {},
                    '.boolean': {}},
    'withdrawn': {'.cli_option': {},
                  '.drf_field': {},
                  '.field': {},
                  '.boolean': {}},
    'compensation_cost': {'.cli_option': {},
                              '.drf_field': {},
                              '.field': {},
                              '.decimal': {
                                  'max_digits': settings.DECIMAL_MAX_DIGITS,
                                  'decimal_places':settings.DECIMAL_PLACES},
                              '.readonly': {}},
    'total_cost_calculated': {'.cli_option': {},
                              '.drf_field': {},
                              '.field': {},
                              '.decimal': {
                                  'max_digits': settings.DECIMAL_MAX_DIGITS,
                                  'decimal_places':settings.DECIMAL_PLACES},
                              '.readonly': {}},
    'additional_expenses': {'.cli_option': {},
                            '.drf_field': {},
                            '.field': {},
                            '.decimal': {
                                'max_digits': settings.DECIMAL_MAX_DIGITS,
                                'decimal_places':settings.DECIMAL_PLACES}},
    'additional_expenses_description': {'.cli_option': {},
                                        '.drf_field': {},
                                        '.field': {},
                                        '.string': {'max_length': 400}},
    'additional_expenses_local_currency': {'.cli_option': {},
                                           '.drf_field': {},
                                           '.field': {},
                                           '.string': {}},
    'travel_files': {'.cli_option': {},
                     '.drf_field': {},
                     '.field': {},
                     '.file': {}},
    'travel_report': {'.cli_option': {},
                      '.drf_field': {},
                      '.field': {},
                      '.string': {'max_length': 1000}},

    'expenditure_date_protocol': {'.cli_option': {},
                                  '.datetime': {'format': '%Y-%m-%dT%H:%M'},
                                  '.drf_field': {},
                                  '.field': {}},
    'expenditure_protocol': {'.cli_option': {},
                             '.drf_field': {},
                             '.field': {},
                             '.string': {}},
    'grnet_quota': {'.cli_option': {},
                    '.drf_field': {},
                    '.field': {},
                    '.float': {},
                    '.readonly': {}},
    'manager_cost_approval': {'.cli_option': {},
                              '.drf_field': {},
                              '.field': {},
                              '.boolean': {}},
    'manager_movement_approval': {'.cli_option': {},
                                  '.drf_field': {},
                                  '.field': {},
                                  '.boolean': {}},
    'movement_date_protocol': {'.cli_option': {},
                               '.datetime': {'format': '%Y-%m-%dT%H:%M'},
                               '.drf_field': {},
                               '.field': {}},
    'movement_id': {'.cli_option': {},
                    '.drf_field': {},
                    '.field': {},
                    '.string': {}},
    'movement_protocol': {'.cli_option': {},
                          '.drf_field': {},
                          '.field': {},
                          '.string': {}},
    'non_grnet_quota': {'.cli_option': {},
                        '.drf_field': {},
                        '.field': {},
                        '.float': {},
                        '.readonly': {}},

    'additional_expenses_initial': {'.cli_option': {},
                                    '.drf_field': {},
                                    '.field': {},
                                    '.decimal': {
                                        'max_digits': settings.DECIMAL_MAX_DIGITS,
                                        'decimal_places':settings.DECIMAL_PLACES}},
    'additional_expenses_initial_description': {'.cli_option': {},
                                                '.drf_field': {},
                                                '.field': {},
                                                '.string': {
                                                    'max_length': 400}},
    'secretary_recommendation': {'.cli_option': {},
                                 '.drf_field': {},
                                 '.field': {},
                                 '.string': {'max_length': 500}},

    'additional_expenses_default_currency': {'.cli_option': {},
                                             '.drf_field': {},
                                             '.field': {},
                                             '.string': {'max_length': 3}},
    'compensation_final': {'.cli_option': {},
                           '.drf_field': {},
                           '.field': {},
                           '.decimal': {
                                'max_digits': settings.DECIMAL_MAX_DIGITS,
                                'decimal_places':settings.DECIMAL_PLACES},
                           '.readonly':{}},
    'created': {'.cli_option': {},
                '.datetime': {},
                '.drf_field': {},
                '.field': {},
                '.readonly': {}},
    'dse': {'.cli_option': {},
            '.drf_field': {'allow_null': True, 'required': False},
            '.field': {},
            '.integer': {},
            '.nullable': {}},
    'first_name': {'.cli_option': {},
                   '.drf_field': {},
                   '.field': {},
                   '.readonly': {},
                   '.string': {}},
    'iban': {'.cli_option': {},
             '.drf_field': {},
             '.field': {},
             '.readonly': {},
             '.string': {}},
    'id': {'.cli_option': {},
           '.drf_field': {},
           '.field': {},
           '.readonly': {},
           '.serial': {}},
    'kind': {'.choices': {},
             '.cli_option': {},
             '.drf_field': {},
             '.field': {},
             '.readonly': {}},
    'last_name': {'.cli_option': {},
                  '.drf_field': {},
                  '.field': {},
                  '.readonly': {},
                  '.string': {}},
    'overnights_num': {'.cli_option': {},
                       '.drf_field': {},
                       '.field': {},
                       '.integer': {},
                       '.readonly': {}},
    'compensation_days_num': {'.cli_option': {},
                              '.drf_field': {},
                              '.field': {},
                              '.integer': {}},
    'overnights_proposed': {'.cli_option': {},
                            '.drf_field': {},
                            '.field': {},
                            '.integer': {},
                            '.readonly':{}},
    'overnights_sum_cost': {'.cli_option': {},
                            '.drf_field': {},
                            '.field': {},
                            '.decimal': {
                                'max_digits': settings.DECIMAL_MAX_DIGITS,
                                'decimal_places':settings.DECIMAL_PLACES},
                            '.readonly': {}},
    'participation_cost': {'.cli_option': {},
                           '.drf_field': {},
                           '.field': {},
                           '.decimal': {
                               'max_digits': settings.DECIMAL_MAX_DIGITS,
                               'decimal_places':settings.DECIMAL_PLACES}},
    'participation_default_currency': {'.cli_option': {},
                                       '.drf_field': {},
                                       '.field': {},
                                       '.string': {'max_length': 3}},
    'participation_local_cost': {'.cli_option': {},
                                 '.drf_field': {},
                                 '.field': {},
                                 '.decimal': {
                                     'max_digits': settings.DECIMAL_MAX_DIGITS,
                                     'decimal_places':settings.DECIMAL_PLACES}},
    'participation_local_currency': {'.choices': {},
                                     '.cli_option': {},
                                     '.drf_field': {},
                                     '.field': {}},
    'participation_payment_description': {'.cli_option': {},
                                          '.drf_field': {},
                                          '.field': {},
                                          '.string': {}},
    'participation_payment_way': {'.choices': {},
                                  '.cli_option': {},
                                  '.drf_field': {},
                                  '.field': {}},
    'project': {'.cli_option': {},
                '.drf_field': {},
                '.field': {},
                '.ref': {'to': 'api/project'},
                '.required': {}},
    'reason': {'.cli_option': {},
               '.drf_field': {},
               '.field': {},
               '.string': {'max_length': 500}},
    'specialty': {'.choices': {},
                  '.cli_option': {},
                  '.drf_field': {},
                  '.field': {},
                  '.readonly': {}},
    'status': {'.cli_option': {},
               '.drf_field': {},
               '.field': {},
               '.integer': {},
               '.readonly': {}},
    'task_duration': {'.cli_option': {},
                      '.drf_field': {},
                      '.field': {},
                      '.integer': {}},
    'task_end_date': {'.cli_option': {},
                      '.datetime': {'format': '%Y-%m-%dT%H:%M'},
                      '.drf_field': {'required': False},
                      '.field': {}},
    'task_start_date': {'.cli_option': {},
                        '.datetime': {'format': '%Y-%m-%dT%H:%M'},
                        '.drf_field': {'required': False},
                        '.field': {}},
    'tax_office': {'.cli_option': {},
                   '.drf_field': {},
                   '.field': {},
                   '.readonly': {},
                   '.ref': {'to': 'api/tax-office'}},
    'tax_reg_num': {'.cli_option': {},
                    '.drf_field': {},
                    '.field': {},
                    '.readonly': {},
                    '.string': {}},
    'transport_days': {'.cli_option': {},
                       '.drf_field': {},
                       '.field': {},
                       '.integer': {}},
    'travel_info': {},
    'trip_days_after': {'.cli_option': {},
                        '.drf_field': {},
                        '.field': {},
                        '.integer': {},
                        '.readonly': {}},
    'trip_days_before': {'.cli_option': {},
                         '.drf_field': {},
                         '.field': {},
                         '.integer': {},
                         '.readonly': {}},
    'updated': {'.cli_option': {},
                '.datetime': {},
                '.drf_field': {},
                '.field': {},
                '.readonly': {}},
    'url': {'.drf_field': {}, '.identity': {}, '.readonly': {}},
    'user': {'.cli_option': {},
             '.drf_field': {},
             '.field': {},
             '.readonly': {},
             '.ref': {'to': 'api/users'}},
    'user_category': {'.choices': {},
                      '.cli_option': {},
                      '.drf_field': {},
                      '.field': {},
                      '.readonly': {}},
    'user_recommendation': {'.cli_option': {},
                            '.drf_field': {},
                            '.field': {},
                            '.string': {'max_length': 500}}},
        '.cli_auth': {'format': 'yaml', 'schema': {'token': ['token']}},
        '.cli_commands': {},
        '.collection': {},
        '.drf_collection': {'authentication_classes':
                            ["rest_framework.authentication."
                             "SessionAuthentication",
                             "rest_framework.authentication."
                             "TokenAuthentication"],
                            'mixins':
                            ['texpenses.views.mixins.ApplicationMixin'],
                            'model': 'texpenses.models.Applications',
                            'model_serializers':
                            ['texpenses.serializers.mixins.PetitionMixin'],
                            'ordering_fields': ['id', 'dse'],
                            'apimas_permission_class':
                             'texpenses.serializers.permissions.NestedPermissions',
                            'permission_classes':
                            ['rest_framework.permissions.IsAuthenticated',
                             "rest_framework.permissions."
                             "DjangoModelPermissions",
                            ],
                            'search_fields': ['first_name',
                                              'last_name',
                                              'dse'
                                              ]},
        '.actions': {'.create': {},
                     '.delete': {},
                     '.list': {},
                     '.retrieve': {},
                     '.update': {}}}
