import sys
from django.core.management.base import BaseCommand
from optparse import make_option

from django.conf import settings
from texpenses.models import (City, Country)

CURRENCY = settings.DEFAULT_CURRENCY

reload(sys)
sys.setdefaultencoding('utf8')


class Command(BaseCommand):
    help = "Loads location info (Countries,Cities etc) from a .csv file"
    args = '<locations>'
    option_list = BaseCommand.option_list + (
        make_option('--delete',
                    action='store_true',
                    dest='delete',
                    default=False,
                    help="Delete all inserted locations prior to loading the"
                    " data from CSV"),
    )

    def preprocess(self, input):
        return input.strip().split(',')

    def get_or_create_extended(self, model, **kwargs):
        try:
            name = kwargs['name']
            obj = model.objects.get(name=name)
            created = False
        except model.DoesNotExist:
            obj = model(**kwargs)
            obj.clean_fields()
            obj.save()
            created = True
        return (obj, created)

    def handle(self, *args, **options):
        location_file_path = args[0]
        with open(location_file_path) as countries_csv_file:

            if options['delete']:
                Country.objects.all().delete()

            for country_record in countries_csv_file:
                country_name, city_name, category_name = self.\
                    preprocess(country_record)

                country_data = {'name': country_name, 'category': category_name,
                                'currency': CURRENCY}
                country_obj, country_created = self.\
                    get_or_create_extended(Country, **country_data)

                if country_created:
                    self.stdout.write("Country:{0} is created.".
                                      format(country_name))

                city_data = {'name': city_name, 'country': country_obj}
                city_obj, city_created = self.\
                    get_or_create_extended(City, **city_data)

                if city_created:
                    self.stdout.write("\tCity:{0} is created.".
                                      format(city_name))
