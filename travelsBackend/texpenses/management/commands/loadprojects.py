import sys
from django.core.management.base import BaseCommand, CommandError
from optparse import make_option

from texpenses.models import Project, UserProfile

reload(sys)
sys.setdefaultencoding('utf8')


class Command(BaseCommand):
    help = "Loads project info from a .csv file"
    args = '<projects>'

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
                print "Record for project:" + str(kwargs['name']) + \
                    " will be updated."
                model.objects.get(name=kwargs['name']).delete()
                obj.save()
            created = True
        return (obj, created)

    def handle(self, *args, **options):
        location_file_path = args[0]
        with open(location_file_path) as projects_csv_file:

            for project_record in projects_csv_file:
                name, accounting_code, manager_surname, manager_name,\
                    manager_email = self.preprocess(project_record)

                try:
                    manager = UserProfile.objects.get(email=manager_email)
                except UserProfile.DoesNotExist:
                    raise CommandError(
                        "Manager does not exist %s" % manager_email)

                project_data = {
                    'name': name,
                    'accounting_code': accounting_code,
                    'manager': manager
                }

                project_obj, project_created = self.\
                    get_or_create_extended(Project, **project_data)

                if project_created:
                    self.stdout.write("Project:{0} is created.".
                                      format(name))
