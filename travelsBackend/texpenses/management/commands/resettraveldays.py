import datetime
import logging
from django.core.management.base import BaseCommand
from django.conf import settings

from texpenses.models import UserProfile, UserDaysLeft

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Reset travel days for all users."

    def handle(self, *args, **options):
        users = UserProfile.objects.all()
        now = datetime.datetime.utcnow()

        for u in users:
            if UserDaysLeft.objects.filter(user=u, created_at__year=now.year).exists():
                logger.info('Already reset days for user %s' % u.username)
                continue

            UserDaysLeft.objects.create(
                    user=u,
                    created_at=now,
                    days_left=u.trip_days_left)
            u.trip_days_left = settings.MAX_HOLIDAY_DAYS
            u.save()
