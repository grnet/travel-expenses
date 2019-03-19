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
        parser.add_argument('locations_csv')

        parser.add_argument('--delete',
            action='store_true',
            dest='delete',
            default=False,
            help="Delete all inserted locations prior to loading the"
            " data from CSV")

        parser.add_argument('--update',
            action='store_true',
            dest='update',
            default=False,
            help="Update all existing locations")

    def preprocess(self, input):
        return input.strip().split(',')

    def get_or_create_country(self, model, **kwargs):
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

    def get_or_create_city(self, model, update=False, **kwargs):
        obj = model.objects.filter(name=kwargs['name'],
                                   country=kwargs['country'])
        if obj:
            if update:
                obj.update(**kwargs)
                updated = True
                created = False
            else:
                created = False
                updated = False
        else:
            obj = model(**kwargs)
            obj.clean_fields()
            obj.save()
            created = True
            updated = False
        return (obj, created, updated)

    def handle(self, *args, **options):
        location_file_path = options['locations_csv']
        with open(location_file_path) as countries_csv_file:

            if options['delete']:
                Country.objects.all().delete()

            number_of_cities_updated = 0
            number_of_cities_created = 0
            number_of_cities_intact = 0
            number_of_countries_created = 0

            for country_record in countries_csv_file:
                country_name, city_name, category_name, timezone = self.\
                    preprocess(country_record)

                country_data = {'name': country_name, 'category': category_name,
                                'currency': CURRENCY}
                country_obj, country_created = self.\
                    get_or_create_country(Country, **country_data)

                if country_created:
                    number_of_countries_created += 1
                    self.stdout.write("Country:{0} is created.".
                                      format(country_name))

                city_data = {'name': city_name, 'country': country_obj,
                             'timezone': timezone
                             }
                city_obj, city_created, city_updated = self.\
                    get_or_create_city(City, update=True if options['update']
                                       else False,
                                       **city_data)
                if city_updated:
                    self.stdout.write("\tCity:{0} is updated.".
                                      format(city_name))
                    number_of_cities_updated += 1

                if city_created:
                    self.stdout.write("\tCity:{0} is created.".
                                      format(city_name))
                    number_of_cities_created += 1

                if not city_created and not city_updated:
                    number_of_cities_intact += 1
            print "========Stats========"
            print "Countries created:{0}".format(number_of_countries_created)
            print "Cities created:{0}".format(number_of_cities_created)
            print "Cities updated:{0}".format(number_of_cities_updated)
            print "Cities left intact:{0}".format(number_of_cities_intact)
            print "====================="
