import sys
from django.core.management.base import BaseCommand
from django.conf import settings

from texpenses.models import UserProfile

reload(sys)
sys.setdefaultencoding('utf8')


class Command(BaseCommand):
    help = "Reset travel days for all users."

    def handle(self, *args, **options):
        # Update all user records in bulk. We don't need to call save here.
        number_of_updated_users = UserProfile.objects.all().update(
            trip_days_left=settings.MAX_HOLIDAY_DAYS)
        self.stdout.write("Number of updated user records:{0}".format(
            number_of_updated_users))
