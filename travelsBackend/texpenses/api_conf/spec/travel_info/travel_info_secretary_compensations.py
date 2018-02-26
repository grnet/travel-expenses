from django.conf import settings

spec = {
    '.structarray': {
        'accommodation_local_cost': {
            '.cli_option': {},
            '.drf_field': {},
            '.field': {},
            '.decimal': {
                'max_digits': settings.DECIMAL_MAX_DIGITS,
                'decimal_places':settings.DECIMAL_PLACES
            },
            '.readonly': {}
        },
        'accommodation_total_local_cost': {
            '.cli_option': {},
            '.drf_field': {},
            '.field': {},
            '.decimal': {
                'max_digits': settings.DECIMAL_MAX_DIGITS,
                'decimal_places':settings.DECIMAL_PLACES
            },
            '.readonly': {}
        },
        'accommodation_local_currency': {
            '.choices': {},
            '.cli_option': {},
            '.drf_field': {},
            '.field': {},
            '.readonly': {}
        },
        'accommodation_payment_description': {
            '.cli_option': {},
            '.drf_field': {},
            '.field': {},
            '.readonly': {},
            '.string': {}
        },
        'accommodation_payment_way': {
            '.choices': {},
            '.cli_option': {},
            '.drf_field': {},
            '.field': {}
        },
        'arrival_point': {
            '.cli_option': {},
            '.drf_field': {},
            '.field': {},
            '.readonly': {},
            '.ref': {'to': 'api/city'}
        },
        'compensation_cost': {
            '.cli_option': {},
            '.drf_field': {},
            '.field': {},
            '.decimal': {
                'max_digits': settings.DECIMAL_MAX_DIGITS,
                'decimal_places':settings.DECIMAL_PLACES
            },
            '.readonly': {}
        },
        'compensation_days_proposed': {
            '.cli_option': {},
            '.drf_field': {},
            '.field': {},
            '.integer': {},
            '.readonly': {}
        },
        'compensation_level': {
            '.cli_option': {},
            '.drf_field': {},
            '.field': {},
            '.decimal': {
                'max_digits': settings.DECIMAL_MAX_DIGITS,
                'decimal_places':settings.DECIMAL_PLACES
            },
            '.readonly': {}
        },
        'overnights_num_proposed': {
            '.cli_option': {},
            '.drf_field': {},
            '.field': {},
            '.integer': {},
            '.readonly': {}
        },
        'depart_date': {
            '.cli_option': {},
            '.datetime': {
                'input_formats': ['%Y-%m-%dT%H:%M']
            },
            '.drf_field': {},
            '.field': {},
            '.readonly': {}
        },
        'departure_point': {
            '.cli_option': {},
            '.drf_field': {},
            '.field': {},
            '.readonly': {},
            '.ref': {'to': 'api/city'}
        },
        'means_of_transport': {
            '.choices': {},
            '.cli_option': {},
            '.drf_field': {},
            '.field': {},
            '.readonly': {}
        },
        'overnight_cost': {
            '.cli_option': {},
            '.drf_field': {},
            '.field': {},
            '.decimal': {
                'max_digits': settings.DECIMAL_MAX_DIGITS,
                'decimal_places':settings.DECIMAL_PLACES
            },
            '.readonly': {}
        },
        'return_date': {
            '.cli_option': {},
            '.datetime': {
                'input_formats': ['%Y-%m-%dT%H:%M']
            },
            '.drf_field': {},
            '.field': {},
            '.readonly': {}
        },
        'same_day_return_task': {
            '.boolean': {},
            '.cli_option': {},
            '.drf_field': {},
            '.field': {},
            '.readonly': {}
        },
        'transport_days_manual': {
            '.cli_option': {},
            '.drf_field': {},
            '.field': {},
            '.integer': {},
            '.readonly': {}
        },
        'transport_days_proposed': {
            '.cli_option': {},
            '.drf_field': {},
            '.field': {},
            '.integer': {},
            '.readonly': {}
        },
        'transportation_payment_description': {
            '.cli_option': {},
            '.drf_field': {},
            '.field': {},
            '.readonly': {},
            '.string': {}
        },
        'transportation_payment_way': {
            '.choices': {},
            '.cli_option': {},
            '.drf_field': {},
            '.field': {}
        }
    }
}
