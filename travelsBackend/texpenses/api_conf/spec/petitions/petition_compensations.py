spec = {'*': {'additional_expenses': {'.cli_option': {},
                                      '.drf_field': {},
                                      '.field': {},
                                      '.float': {}},
              'additional_expenses_description': {'.cli_option': {},
                                                  '.drf_field': {},
                                                  '.field': {},
                                                  '.string': {}},
              'additional_expenses_local_currency': {'.cli_option': {},
                                                     '.drf_field': {},
                                                     '.field': {},
                                                     '.string': {}},
              'compensation_final': {'.cli_option': {},
                                     '.drf_field': {},
                                     '.field': {},
                                     '.float': {},
                                     '.readonly': {}},
              'dse': {'.cli_option': {},
                      '.drf_field': {'allow_null': True, 'required': False},
                      '.field': {},
                      '.integer': {},
                      '.nullable': {},
                      '.readonly': {}},
              'expenditure_date_protocol': {'.cli_option': {},
                                            '.date': {},
                                            '.drf_field': {},
                                            '.field': {},
                                            '.readonly': {}},
              'expenditure_protocol': {'.cli_option': {},
                                       '.drf_field': {},
                                       '.field': {},
                                       '.readonly': {},
                                       '.string': {}},
              'manager_cost_approval': {'.cli_option': {},
                                        '.drf_field': {},
                                        '.field': {},
                                        '.readonly': {},
                                        '.boolean': {}},
              'manager_movement_approval': {'.cli_option': {},
                                            '.drf_field': {},
                                            '.field': {},
                                            '.readonly': {},
                                            '.boolean': {}},
              'movement_date_protocol': {'.cli_option': {},
                                         '.date': {},
                                         '.drf_field': {},
                                         '.field': {},
                                         '.readonly': {}},
              'movement_id': {'.cli_option': {},
                              '.drf_field': {},
                              '.field': {},
                              '.readonly': {},
                              '.string': {}},
              'movement_protocol': {'.cli_option': {},
                                    '.drf_field': {},
                                    '.field': {},
                                    '.readonly': {},
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
              'participation_cost': {'.cli_option': {},
                                     '.drf_field': {},
                                     '.field': {},
                                     '.float': {},
                                     '.readonly': {}},
              'participation_local_cost': {'.cli_option': {},
                                           '.drf_field': {},
                                           '.field': {},
                                           '.float': {},
                                           '.readonly': {}},
              'participation_local_currency': {'.choices': {},
                                               '.cli_option': {},
                                               '.drf_field': {},
                                               '.field': {},
                                               '.readonly': {}},
              'participation_payment_description': {'.cli_option': {},
                                                    '.drf_field': {},
                                                    '.field': {},
                                                    '.readonly': {},
                                                    '.string': {}},
              'participation_payment_way': {'.choices': {},
                                            '.cli_option': {},
                                            '.drf_field': {},
                                            '.field': {},
                                            '.readonly': {}},
              'reason': {'.cli_option': {},
                         '.drf_field': {},
                         '.field': {},
                         '.readonly': {},
                         '.string': {}},
              'task_end_date': {'.cli_option': {},
                                '.datetime': {'format': ['%Y-%m-%dT%H:%M']},
                                '.drf_field': {'required': False},
                                '.field': {},
                                '.readonly': {}},
              'task_start_date': {'.cli_option': {},
                                  '.datetime': {'format': ['%Y-%m-%dT%H:%M']},
                                  '.drf_field': {'required': False},
                                  '.field': {},
                                  '.readonly': {}},
              'total_cost_calculated': {'.cli_option': {},
                                        '.drf_field': {},
                                        '.field': {},
                                        '.float': {},
                                        '.readonly': {}},
              'travel_files': {'.cli_option': {},
                               '.drf_field': {},
                               '.field': {},
                               '.file': {}},
              'travel_report': {'.cli_option': {},
                                '.drf_field': {},
                                '.field': {},
                                '.string': {}},
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
                       '.required': {}}},
        '.drf_collection':
        {'authentication_classes':
         ['rest_framework.authentication.SessionAuthentication',
          'rest_framework.authentication.TokenAuthentication'],
         'mixins': ['texpenses.views.mixins.UserCompensationMixin'],
         'model': 'texpenses.models.UserCompensation',
         'model_serializers':
             ['texpenses.serializers.mixins.PetitionMixin'],
             'ordering_fields': ['id'],
             'permission_classes':
             ['rest_framework.permissions.IsAuthenticated',
              'rest_framework.permissions.DjangoModelPermissions'],
             'search_fields': ['first_name',
                               'last_name',
                               ]}}
