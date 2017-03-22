spec = {'*': {'additional_expenses_default_currency': {'.cli_option': {},
                                                       '.drf_field': {},
                                                       '.field': {},
                                                       '.string': {}},
              'additional_expenses_initial': {'.cli_option': {},
                                              '.drf_field': {},
                                              '.field': {},
                                              '.float': {}},
              'additional_expenses_initial_description': {'.cli_option': {},
                                                          '.drf_field': {},
                                                          '.field': {},
                                                          '.string': {}},
              'compensation_final': {'.cli_option': {},
                                     '.drf_field': {},
                                     '.field': {},
                                     '.float': {},
                                     '.readonly': {}},
              'expenditure_date_protocol': {'.cli_option': {},
                                            '.date': {},
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
              'manager_final_approval': {'.cli_option': {},
                                         '.drf_field': {},
                                         '.field': {},
                                         '.string': {}},
              'manager_travel_approval': {'.cli_option': {},
                                          '.drf_field': {},
                                          '.field': {},
                                          '.string': {}},
              'movement_date_protocol': {'.cli_option': {},
                                         '.date': {},
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
              'overnights_num': {'.cli_option': {},
                                 '.drf_field': {},
                                 '.field': {},
                                 '.integer': {},
                                 '.readonly': {}},
              'overnights_proposed': {'.cli_option': {},
                                      '.drf_field': {},
                                      '.field': {},
                                      '.integer': {},
                                      '.readonly': {}},
              'overnights_sum_cost': {'.cli_option': {},
                                      '.drf_field': {},
                                      '.field': {},
                                      '.float': {},
                                      '.readonly': {}},
              'secretary_recommendation': {'.cli_option': {},
                                           '.drf_field': {},
                                           '.field': {},
                                           '.string': {}},
              'total_cost': {'.cli_option': {},
                             '.drf_field': {},
                             '.field': {},
                             '.float': {},
                             '.readonly': {}},
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
              'user': {'.cli_option': {},
                       '.drf_field': {},
                       '.field': {},
                       '.ref': {'to': 'api/users'},
                       '.required': {}},
              'user_recommendation': {'.cli_option': {},
                                      '.drf_field': {},
                                      '.field': {},
                                      '.string': {}}},
        '.drf_collection':
        {'authentication_classes':
         ['rest_framework.authentication.SessionAuthentication',
          'rest_framework.authentication.TokenAuthentication'],
         'mixins': ['texpenses.views.mixins.SecretaryPetitionSaveMixin'],
         'model': 'texpenses.models.SecretaryPetition',
         'model_serializers':
             ['texpenses.serializers.mixins.PetitionMixin'],
             'ordering_fields': ['id'],
             'permission_classes':
             ['rest_framework.permissions.IsAuthenticated',
              'rest_framework.permissions.DjangoModelPermissions'],
             'search_fields': ['first_name',
                               'last_name',
                               'project',
                               'task_start_date',
                               'task_end_date',
                               'created',
                               'updated']}}
