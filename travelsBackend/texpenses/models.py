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
    taxRegNum = models.IntegerField(blank=True, null=True,
                                    validators=[afm_validator])
    taxOffice = models.ForeignKey(TaxOffice, blank=True, null=True)
    kind = models.ForeignKey(Kind, blank=True, null=True)
    category = models.ForeignKey(
        UserCategory, blank=True, null=True)
    trip_days_left = models.IntegerField(default=settings.MAX_HOLIDAY_DAYS)


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

    def same_day_return(self):
        if self.return_date is None:
            return False
        if self.depart_date is None:
            return False

        delta = self.return_date - self.depart_date
        if delta.days == 0:
            return True
        return False

    accomondation = models.ForeignKey(Accomondation, blank=True, null=True)
    flight = models.ForeignKey(Flight, blank=True, null=True)
    feeding = models.ForeignKey(FeedingKind, blank=True, null=True)
    non_grnet_quota = models.FloatField(blank=True, null=True, default=0.0)

    def grnet_quota(self):
        return 100 - self.non_grnet_quota

    compensation = models.ForeignKey(Compensation, blank=True, null=True)

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

    def compensation_level(self):
        comp_object = self.advanced_info.compensation
        if comp_object is None:
            return 0

        return self.advanced_info.compensation.compensation

    def transport_days(self):
        depart_date = self.advanced_info.depart_date
        if self.taskEndDate is None or \
                self.taskStartDate is None or depart_date is None:
            return 0
        delta = self.taskEndDate - depart_date
        days = delta.days
        if days > 1:
            days = 1
        t_cycle = self.taskEndDate - self.taskStartDate

        return t_cycle.days + days

    def compensation_days(self):
        return self.transport_days()

    def max_compensation(self):
        return self.compensation_days() * self.compensation_level()

    def overnights_num(self):
        trans_days = self.transport_days()
        if trans_days == 0:
            return 0
        return trans_days - 1

    def overnight_cost(self):
        accomondation = self.advanced_info.accomondation
        if accomondation is None:
            return 0
        hotel_price = accomondation.hotelPrice
        if hotel_price is None:
            return 0
        return hotel_price

    def overnights_sum_cost(self):
        return self.overnight_cost() * self.overnights_num()

    def task_duration(self):
        if self.taskEndDate is None or self.taskStartDate is None:
            return 0

        delta = self.taskEndDate - self.taskStartDate

        return delta.days

    def is_city_ny(self):
        ap = self.arrivalPoint
        if ap is None:
            return False
        if ap.name == "NEW YORK":
            return True
        else:
            return False

    def max_overnight_cost(self):
        user_category = self.user_category
        if user_category is None:
            return 0
        default_max_overnight_cost = user_category.max_overnight_cost
        if self.is_city_ny():
            return default_max_overnight_cost + 100
        else:
            return default_max_overnight_cost

    def same_day_return_task(self):
        t_end_date = self.taskEndDate
        r_date = self.advanced_info.return_date
        if t_end_date is None or r_date is None:
            return False
        if t_end_date == r_date:
            return True

        return False

    def __unicode__(self):
        return str(self.id) + "-" + self.project.name


class AdditionalExpenses(models.Model):

    """Docstring for AdditionalWages. """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    cost = models.FloatField()
    petition = models.ForeignKey(Petition)
    user = models.ForeignKey(UserProfile)

    def __unicode__(self):
        return self.name + "-" + str(self.id)
