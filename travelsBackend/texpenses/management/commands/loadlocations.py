import sys
from django.core.management.base import BaseCommand
from django.conf import settings
from texpenses.models import (City, Country)

CURRENCY = settings.DEFAULT_CURRENCY

reload(sys)
sys.setdefaultencoding('utf8')


class Command(BaseCommand):
    help = "Loads location info (Countries,Cities etc) from a .csv file"

    def add_arguments(self, parser):
        parser.add_argument('locations')
        parser.add_argument(
            '--delete',
            action='store_true',
            dest='delete',
            default=False,
            help="Delete all inserted locations prior to loading the data "
            "from CSV",
        )

    def preprocess(self, input):
        return input.strip().split(';')

    def handle(self, *args, **options):
        location_file_path = options['locations']
        with open(location_file_path) as countries_csv_file:

            if options['delete']:
                Country.objects.all().delete()

            for country_record in countries_csv_file:
                country_name, city_name, category_name = self.\
                    preprocess(country_record)

                country_obj, country_created = Country.objects.\
                    get_or_create(name=country_name,
                                  category=category_name,
                                  currency=CURRENCY)
                if country_created:
                    self.stdout.write("Country:{0} is created.".
                                      format(country_name))

                city_obj, city_created = City.objects.\
                    get_or_create(name=city_name,
                                  country=country_obj)
                if city_created:
                    self.stdout.write("\tCity:{0}, is created.".
                                      format(city_name))
