spec = {'*': {'additional_expenses_default_currency': {'.cli_option': {},
                                                       '.drf_field': {},
                                                       '.field': {},
                                                       '.readonly': {},
                                                       '.string':
                                                       {'max_length': 3}},
              'additional_expenses_initial': {'.cli_option': {},
                                              '.drf_field': {},
                                              '.field': {},
                                              '.float': {},
                                              '.readonly': {}},
              'additional_expenses_initial_description': {'.cli_option': {},
                                                          '.drf_field': {},
                                                          '.field': {},
                                                          '.readonly': {},
                                                          '.string': {}},
              'compensation_final': {'.cli_option': {},
                                     '.drf_field': {},
                                     '.field': {},
                                     '.float': {}},
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
                                 '.integer': {}},
              'compensation_days_num': {'.cli_option': {},
                                 '.drf_field': {},
                                 '.field': {},
                                 '.integer': {}},
              'overnights_proposed': {'.cli_option': {},
                                      '.drf_field': {},
                                      '.field': {},
                                      '.integer': {}},
              'overnights_sum_cost': {'.cli_option': {},
                                      '.drf_field': {},
                                      '.field': {},
                                      '.float': {}},
              'participation_cost': {'.cli_option': {},
                                     '.drf_field': {},
                                     '.field': {},
                                     '.float': {}},
              'participation_default_currency': {'.cli_option': {},
                                                 '.drf_field': {},
                                                 '.field': {},
                                                 '.readonly': {},
                                                 '.string': {'max_length': 3}},
              'participation_local_cost': {'.cli_option': {},
                                           '.drf_field': {},
                                           '.field': {},
                                           '.float': {}},
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
                         '.string': {}},
              'secretary_recommendation': {'.cli_option': {},
                                           '.drf_field': {},
                                           '.field': {},
                                           '.readonly': {},
                                           '.string': {}},
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
                                '.datetime': {'format': ['%Y-%m-%dT%H:%M']},
                                '.drf_field': {'required': False},
                                '.field': {}},
              'task_start_date': {'.cli_option': {},
                                  '.datetime': {'format': ['%Y-%m-%dT%H:%M']},
                                  '.drf_field': {'required': False},
                                  '.field': {}},
              'tax_office': {'.cli_option': {},
                             '.drf_field': {},
                             '.field': {},
                             '.readonly': {},
                             '.ref': {'to': 'api/tax-office'}},
              'total_cost': {'.cli_option': {},
                             '.drf_field': {},
                             '.field': {},
                             '.float': {}},
              'transport_days': {'.cli_option': {},
                                 '.drf_field': {},
                                 '.field': {},
                                 '.integer': {}},
              'travel_info': {},
              'trip_days_after': {'.cli_option': {},
                                  '.drf_field': {},
                                  '.field': {},
                                  '.integer': {}},
              'trip_days_before': {'.cli_option': {},
                                   '.drf_field': {},
                                   '.field': {},
                                   '.integer': {}},
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
                                      '.string': {}}},
        '.cli_auth': {'format': 'yaml', 'schema': {'token': ['token']}},
        '.cli_commands': {},
        '.collection': {},
        '.drf_collection': {'authentication_classes':
                            ["rest_framework.authentication."
                             "SessionAuthentication",
                             "rest_framework.authentication."
                             "TokenAuthentication"],
                            'mixins':
                            ['texpenses.views.mixins.UserPetitionMixin'],
                            'model': 'texpenses.models.UserPetition',
                            'model_serializers':
                            ['texpenses.serializers.mixins.PetitionMixin'],
                            'ordering_fields': ['id'],
                            'permission_classes':
                            ['rest_framework.permissions.IsAuthenticated',
                             "rest_framework.permissions."
                             "DjangoModelPermissions"],
                            'search_fields': ['first_name',
                                              'last_name',
                                              'project',
                                              'task_start_date',
                                              'task_end_date',
                                              'created',
                                              'updated']},
        '.actions': {'.create': {},
                     '.delete': {},
                     '.list': {},
                     '.retrieve': {},
                     '.update': {}}}
