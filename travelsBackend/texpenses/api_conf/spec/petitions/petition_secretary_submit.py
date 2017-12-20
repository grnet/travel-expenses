spec = {'*': {'additional_expenses_default_currency': {'.cli_option': {},
                                                       '.drf_field':
                                                       {'allow_blank': False,
                                                        'allow_null': False,
                                                        'required': True},
                                                       '.field': {},
                                                       '.required': {},
                                                       '.string':
                                                       {'max_length': 3}},
              'additional_expenses_initial': {'.cli_option': {},
                                              '.drf_field':
                                              {'allow_null': False,
                                               'required': True},
                                              '.field': {},
                                              '.float': {},
                                              '.required': {}},
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
                                            '.drf_field': {'allow_null': False,
                                                           'required': True},
                                            '.field': {},
                                            '.required': {}},
              'withdrawn': {'.cli_option': {},
                            '.drf_field': {},
                            '.field': {},
                            '.boolean': {}},
              'expenditure_protocol': {'.cli_option': {},
                                       '.drf_field': {'allow_blank': False,
                                                      'allow_null': False,
                                                      'required': True},
                                       '.field': {},
                                       '.required': {},
                                       '.string': {'max_length': 30}},
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
                                         '.date': {},
                                         '.drf_field': {'allow_null': False,
                                                        'required': True},
                                         '.field': {},
                                         '.required': {}},
              'movement_id': {'.cli_option': {},
                              '.drf_field': {'allow_blank': False,
                                             'allow_null': False,
                                             'required': True},
                              '.field': {},
                              '.required': {},
                              '.string': {}},
              'movement_protocol': {'.cli_option': {},
                                    '.drf_field': {'allow_blank': False,
                                                   'allow_null': False,
                                                   'required': True},
                                    '.field': {},
                                    '.required': {},
                                    '.string': {'max_length': 30}},
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
              'compensation_days_num': {'.cli_option': {},
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
              'total_cost_calculated': {'.cli_option': {},
                                        '.drf_field': {},
                                        '.field': {},
                                        '.float': {},
                                        '.readonly': {}},
              'total_cost_change_reason': {'.cli_option': {},
                                           '.drf_field': {},
                                           '.field': {},
                                           '.string': {},
                                           '.readonly': {}},
              'total_cost_manual': {'.cli_option': {},
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
         'mixins':
             ['texpenses.views.mixins.SecretaryPetitionSubmissionMixin'],
             'model': 'texpenses.models.SecretaryPetitionSubmission',
             'model_serializers':
             ['texpenses.serializers.mixins.PetitionMixin'],
             'ordering_fields': ['id'],
             'permission_classes':
             ['rest_framework.permissions.IsAuthenticated',
              'rest_framework.permissions.DjangoModelPermissions'],
             'search_fields': ['first_name',
                               'last_name',]}}
