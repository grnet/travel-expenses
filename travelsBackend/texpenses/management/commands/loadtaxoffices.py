import sys
from django.core.management.base import BaseCommand

from texpenses.models import TaxOffice


reload(sys)
sys.setdefaultencoding('utf8')


class Command(BaseCommand):
    help = "Loads tax office info from a .csv file"
    args = '<taxoffices>'

    def preprocess(self, input):
        data = input.strip().split(',')

        data = [item.replace('"', '') for item in data]

        return data

    def get_or_create_extended(self, model, **kwargs):
        try:
            obj = model.objects.get(**kwargs)
            created = False
        except model.DoesNotExist:
            obj = model(**kwargs)
            obj.clean_fields()
            try:
                obj.save()
            except Exception:
                print "Record for tax office:" + str(kwargs['name']) + \
                " will be updated."
                model.objects.get(name=kwargs['name']).delete()
                obj.save()
            created = True
        return (obj, created)

    def handle(self, *args, **options):
        location_file_path = args[0]
        with open(location_file_path) as taxoffices_csv_file:

            for taxoffice_record in taxoffices_csv_file:
                name, description, address, email, phone = self.\
                    preprocess(taxoffice_record)

                taxoffice_data = {'name': name, 'description': description,
                                  'address': address, 'email': email,
                                  'phone': phone}
                taxoffice_obj, taxoffice_created = self.\
                    get_or_create_extended(TaxOffice, **taxoffice_data)

                if taxoffice_created:
                    self.stdout.write("Tax-Office:{0} is created.".
                                      format(name))
