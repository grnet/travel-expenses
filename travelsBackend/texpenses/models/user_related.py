from django.db import models
from django.contrib.auth.models import AbstractUser
from texpenses.validators import iban_validation
from texpenses.validators import afm_validator
from django.conf import settings


class Specialty(models.Model):

    """Docstring for Specialty . """
    name = models.CharField(max_length=200)
    id = models.AutoField(primary_key=True)

    def __unicode__(self):
        return self.name


class Kind(models.Model):

    """Docstring for Kind. """

    name = models.CharField(max_length=200)
    id = models.AutoField(primary_key=True)

    def __unicode__(self):
        return self.name


class UserCategory(models.Model):

    """Docstring for User Category. """

    name = models.CharField(max_length=10)
    id = models.AutoField(primary_key=True)
    max_overnight_cost = models.FloatField(default=0.0)

    def __unicode__(self):
        return self.name


class TaxOffice(models.Model):

    """Docstring for TaxOffice. """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    kindDescription = models.CharField(max_length=300, blank=True)
    address = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20)

    def __unicode__(self):
        return self.name


class UserProfile(AbstractUser):
    iban = models.CharField(max_length=200, blank=True, null=True,
                            validators=[iban_validation])
    specialtyID = models.ForeignKey(Specialty, blank=True, null=True)
    taxRegNum = models.CharField(max_length=9, blank=True, null=True,
                                 validators=[afm_validator])
    taxOffice = models.ForeignKey(TaxOffice, blank=True, null=True)
    kind = models.ForeignKey(Kind, blank=True, null=True)
    category = models.ForeignKey(
        UserCategory, blank=True, null=True)
    trip_days_left = models.IntegerField(default=settings.MAX_HOLIDAY_DAYS)

    def user_group(self):
        groups = self.groups.all()
        print groups
        if not groups:
            return "Unknown"
        return groups[0].name
