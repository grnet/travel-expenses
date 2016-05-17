from django.db import models
from django.contrib.auth.models import AbstractUser
from validators import iban_validation
from validators import afm_validator
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
    taxRegNum = models.IntegerField(blank=True, null=True,
                                    validators=[afm_validator])
    taxOffice = models.ForeignKey(TaxOffice, blank=True, null=True)
    kind = models.ForeignKey(Kind, blank=True, null=True)
    category = models.ForeignKey(
        UserCategory, blank=True, null=True)


class Accomondation(models.Model):

    """Docstring for Accomondation. """
    id = models.AutoField(primary_key=True)
    hotel = models.CharField(max_length=200)
    hotelPrice = models.FloatField(blank=True, null=True)
    user = models.ForeignKey(UserProfile)

    def __unicode__(self):
        """TODO: Docstring for __unicode__.
        :returns: TODO

        """
        return self.hotel


class Flight(models.Model):

    """Docstring for Accomondation. """
    id = models.AutoField(primary_key=True)
    flightName = models.CharField(max_length=200)
    flightPrice = models.FloatField(blank=True, null=True)
    user = models.ForeignKey(UserProfile)

    def __unicode__(self):
        """TODO: Docstring for __unicode__.
        :returns: TODO

        """
        return self.flightName


class Project(models.Model):

    """Docstring for Project. """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    accountingCode = models.CharField(max_length=20)

    def __unicode__(self):
        return self.name


class MovementCategories(models.Model):

    """Docstring for MovementCategories. """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)

    def __unicode__(self):
        """TODO: to be defined1. """
        return self.name


class CountryCategory(models.Model):

    """Docstring for CountryCategory. """

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)

    def __unicode__(self):
        """TODO: to be defined. """
        return self.name


class Country(models.Model):

    """Docstring for Countries. """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    category = models.ForeignKey(CountryCategory)

    def __unicode__(self):
        """TODO: to be defined1. """
        return self.name


class City(models.Model):

    """Docstring for City. """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    country = models.ForeignKey(Country, blank=True, null=True)

    def __unicode__(self):
        """TODO: to be defined. """
        return self.name


class Transportation(models.Model):

    """Docstring for Transportation. """

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)

    def __unicode__(self):
        """TODO: to be defined1. """
        return self.name


class PetitionStatus(models.Model):

    """Docstring for Petition status. """

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    def __unicode__(self):
        """TODO: to be defined1. """
        return self.name


class FeedingKind(models.Model):

    """Docstring for FeedindKind. """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)

    def __unicode__(self):
        return self.name


class Compensation(models.Model):

    """Docstring for Compensation. """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    country_category = models.ForeignKey(CountryCategory, blank=True, null=True)
    user_category = models.ForeignKey(UserCategory, blank=True, null=True)
    compensation = models.IntegerField()

    def __unicode__(self):
        """TODO: to be defined1. """
        return self.name


class AdvancedPetition(models.Model):

    """Docstring for AdvancedPetition. """
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserProfile)

    dse = models.IntegerField(blank=True, null=True)
    depart_date = models.DateTimeField(blank=True, null=True)
    return_date = models.DateTimeField(blank=True, null=True)
    accomondation = models.ForeignKey(Accomondation, blank=True, null=True)
    flight = models.ForeignKey(Flight, blank=True, null=True)
    feeding = models.ForeignKey(FeedingKind, blank=True, null=True)
    non_grnet_quota = models.FloatField(blank=True, null=True, default=0.0)

    # computed model fields
    compensation = models.ForeignKey(Compensation, blank=True, null=True)
    compensation_days = models.IntegerField(default=0)

    overnights_number = models.IntegerField(default=0)

    overnights_sum_cost = models.FloatField(default=0.0)
    sum_compensation = models.FloatField(default=0.0)
    same_day_return = models.BooleanField(default=False)

    max_holiday_days = models.IntegerField(default=settings.MAX_HOLIDAY_DAYS)
    days_left_after = models.IntegerField(default=settings.MAX_HOLIDAY_DAYS)
    days_left_before = models.IntegerField(default=settings.MAX_HOLIDAY_DAYS)

    # ------------------------------------------#
    expenditure_protocol = models.CharField(
        max_length=30, null=True, blank=True)
    expenditure_date_protocol = models.DateField(blank=True, null=True)

    movement_protocol = models.CharField(
        max_length=30, null=True, blank=True)
    movement_date_protocol = models.DateField(blank=True, null=True)

    compensation_petition_protocol = models.CharField(
        max_length=30, null=True, blank=True)
    compensation_petition_date = models.DateField(blank=True, null=True)

    compensation_decision_protocol = models.CharField(
        max_length=30, null=True, blank=True)
    compensation_decision_date = models.DateField(blank=True, null=True)

    def __unicode__(self):
        return str(self.id)


class Petition(models.Model):

    """Docstring for Travel Application. """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    surname = models.CharField(max_length=200, blank=True, null=True)
    iban = models.CharField(max_length=200, blank=True, null=True,
                            validators=[iban_validation])
    specialtyID = models.ForeignKey(Specialty, blank=True, null=True)
    taxRegNum = models.IntegerField(blank=True, null=True,
                                    validators=[afm_validator])
    taxOffice = models.ForeignKey(TaxOffice, blank=True, null=True)
    kind = models.ForeignKey(Kind, blank=True, null=True)
    user_category = models.ForeignKey(UserCategory, blank=True, null=True)

    user = models.ForeignKey(UserProfile)
    taskStartDate = models.DateTimeField(blank=True, null=True)
    taskEndDate = models.DateTimeField(blank=True, null=True)
    creationDate = models.DateTimeField(blank=True, null=True)
    updateDate = models.DateTimeField(blank=True, null=True)
    project = models.ForeignKey(Project)
    reason = models.CharField(max_length=500, blank=True, null=True)
    movementCategory = models.ForeignKey(
        MovementCategories, blank=True, null=True)
    departurePoint = models.ForeignKey(
        City, blank=True, null=True, related_name='departure_point')
    arrivalPoint = models.ForeignKey(City, blank=True, null=True,
                                     related_name='arrivale_point')
    transportation = models.ForeignKey(Transportation, blank=True, null=True)
    recTransport = models.CharField(max_length=200, blank=True, null=True)
    recAccomondation = models.CharField(max_length=200, blank=True, null=True)
    recCostParticipation = models.FloatField(blank=True, null=True, default=0.0)
    status = models.ForeignKey(PetitionStatus)
    advanced_info = models.OneToOneField(
        AdvancedPetition, blank=True, null=True)

    def __unicode__(self):
        return str(self.id) + "-" + self.project.name


class AdditionalWage(models.Model):

    """Docstring for AdditionalWages. """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    cost = models.FloatField()
    petition = models.ForeignKey(Petition)
    user = models.ForeignKey(UserProfile)

    def __unicode__(self):
        return self.name + "-" + str(self.id)
