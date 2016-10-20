import sys
from django.core.management.base import BaseCommand
from optparse import make_option

from texpenses.models import Project

reload(sys)
sys.setdefaultencoding('utf8')


class Command(BaseCommand):
    help = "Loads project info from a .csv file"
    args = '<projects>'
    option_list = BaseCommand.option_list + (
        make_option('--delete',
                    action='store_true',
                    dest='delete',
                    default=False,
                    help="Delete all inserted projects prior to loading the"
                    " data from CSV"),
    )

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
            obj.save()
            created = True
        return (obj, created)

    def handle(self, *args, **options):
        location_file_path = args[0]
        with open(location_file_path) as projects_csv_file:

            load_in_bulk = False
            bulk_data = []

            if options['delete']:
                self.stdout.write("Data insertion in bulk is activated...")
                load_in_bulk = True
                Project.objects.all().delete()

            for project_record in projects_csv_file:
                name, accounting_code, manager_surname, manager_name,\
                    manager_email = self.preprocess(project_record)

                project_data = {'name': name,
                                'accounting_code': accounting_code,
                                'manager_surname': manager_surname,
                                'manager_name': manager_name,
                                'manager_email': manager_email
                                }
                if not load_in_bulk:
                    project_obj, project_created = self.\
                        get_or_create_extended(Project, **project_data)

                    if project_created:
                        self.stdout.write("Project:{0} is created.".
                                          format(name))
                else:
                    self.stdout.write("Appending new project:{0}"
                                      "to project list.".
                                      format(name))
                    bulk_data.append(Project(**project_data))

            if load_in_bulk:
                self.stdout.write("Inserting data in bulk.")
                Project.objects.bulk_create(bulk_data)
