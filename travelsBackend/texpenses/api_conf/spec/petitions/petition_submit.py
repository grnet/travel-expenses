spec = {'*': {'additional_expenses_default_currency': {'.cli_option': {},
                                                       '.drf_field': {},
                                                       '.field': {},
                                                       '.string': {}},
              'additional_expenses_initial': {'.cli_option': {},
                                              '.drf_field': {},
                                              '.field': {},
                                              '.decimal': {'max_digits': 8,
                                                           'decimal_places':3}},
              'additional_expenses_initial_description': {'.cli_option': {},
                                                          '.drf_field': {},
                                                          '.field': {},
                                                          '.string': {}},
              'participation_cost': {'.cli_option': {},
                                     '.drf_field': {},
                                     '.field': {},
                                     '.decimal': {'max_digits': 8,
                                                  'decimal_places':3},
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
                         '.drf_field': {'allow_blank': False,
                                        'allow_null': False,
                                        'required': True},
                         '.field': {},
                         '.required': {},
                         '.string': {}},
              'secretary_recommendation': {'.cli_option': {},
                                           '.drf_field': {},
                                           '.field': {},
                                           '.string': {}},
              'task_end_date': {'.cli_option': {},
                                '.datetime': {'format': ['%Y-%m-%dT%H:%M']},
                                '.drf_field': {'allow_null': False,
                                               'required': True},
                                '.field': {},
                                '.required': {}},
              'task_start_date': {'.cli_option': {},
                                  '.datetime': {'format': ['%Y-%m-%dT%H:%M']},
                                  '.drf_field': {'allow_null': False,
                                                 'required': True},
                                  '.field': {},
                                  '.required': {}},
              'user_recommendation': {'.cli_option': {},
                                      '.drf_field': {},
                                      '.field': {},
                                      '.string': {}}},
        '.drf_collection': {'authentication_classes':
                            ["rest_framework.authentication."
                             "SessionAuthentication",
                             "rest_framework.authentication."
                             "TokenAuthentication"],
                            'mixins':
                            ["texpenses.views.mixins."
                             "UserPetitionSubmissionMixin"],
                            'model': 'texpenses.models.UserPetitionSubmission',
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
                                              'updated']}}
