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

    def handle(self, *args, **options):
        location_file_path = args[0]
        with open(location_file_path) as projects_csv_file:

            for project_record in projects_csv_file:
                name, accounting_code, manager_surname, manager_name,\
                    manager_email = self.preprocess(project_record)

                try:
                    manager = UserProfile.objects.get(email=manager_email)
                except UserProfile.DoesNotExist:
                    manager = None

                try:
                    p = Project.objects.get(name=name)
                    p.accounting_code = accounting_code
                    if manager:
                        p.manager = manager
                    p.save()
                except Project.DoesNotExist:
                    Project.objects.create(
                        name=name,
                        accounting_code=accounting_code,
                        manager=manager)
                    self.stdout.write("Project:{0} is created.".
                                      format(name))
