from datetime import datetime
from django.core.exceptions import ValidationError, MinValueValidator
from texpenses.models.services import get_queryset_on_group
from django.db import models
from user_related import UserProfile, UserCategory, Specialty, Kind,\
    TaxOffice
from texpenses.validators import (
    afm_validator, iban_validation, required_validator, date_validator)
from django.db.models import Sum, Q
from model_utils import FieldTracker
from workdays import networkdays


class Accomondation(models.Model):

    """Docstring for Accomondation. """
    id = models.AutoField(primary_key=True)
    hotel = models.CharField(max_length=200)
    hotelPrice = models.FloatField(blank=True, null=True)
    user = models.ForeignKey(UserProfile)

    def clean(self):
        super(Accomondation, self).clean()
        advanced_petitions = AdvancedPetition.objects.filter(
            accomondation__id=self.id)
        for advanced_petition in advanced_petitions:
            petition = advanced_petition.petition
            if petition.user_category:
                max_overnight = petition.user_category.max_overnight_cost
                if self.hotelPrice > max_overnight:
                    raise ValidationError(
                        'Hotel cost %.2f exceedes the max hotel allowable'
                        ' limit' % (self.hotelPrice))

    class APITravel(object):
        fields = ('id', 'hotel', 'hotelPrice', 'url')

        @staticmethod
        def get_queryset(request_user):
            return get_queryset_on_group(request_user, Accomondation)

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

    class APITravel(object):
        fields = ('id', 'flightName', 'flightPrice', 'url')

        @staticmethod
        def get_queryset(request_user):
            return get_queryset_on_group(request_user, Flight)

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

    class APITravel(object):
        fields = ('id', 'name', 'accountingCode', 'url')

    def __unicode__(self):
        return self.name


class MovementCategories(models.Model):

    """Docstring for MovementCategories. """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)

    class APITravel(object):
        fields = ('id', 'name', 'url')

    def __unicode__(self):
        """TODO: to be defined1. """
        return self.name


class CountryCategory(models.Model):

    """Docstring for CountryCategory. """

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)

    class APITravel(object):
        fields = ('id', 'name', 'url')

    def __unicode__(self):
        """TODO: to be defined. """
        return self.name


class Country(models.Model):

    """Docstring for Countries. """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    category = models.ForeignKey(CountryCategory)

    class APITravel(object):
        fields = ('id', 'name', 'category', 'url')

    def __unicode__(self):
        """TODO: to be defined1. """
        return self.name


class City(models.Model):

    """Docstring for City. """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    country = models.ForeignKey(Country, blank=True, null=True)

    class APITravel(object):
        fields = ('id', 'name', 'country', 'url')
        filter_fields = ('country',)

    def __unicode__(self):
        """TODO: to be defined. """
        return self.name


class Transportation(models.Model):

    """Docstring for Transportation. """

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)

    class APITravel(object):
        fields = ('id', 'name', 'url')

    def __unicode__(self):
        """TODO: to be defined1. """
        return self.name


class PetitionStatus(models.Model):

    """Docstring for Petition status. """

    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)

    class APITravel(object):
        fields = ('id', 'name', 'url')

    def __unicode__(self):
        """TODO: to be defined1. """
        return self.name


class FeedingKind(models.Model):

    """Docstring for FeedindKind. """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)

    class APITravel(object):
        fields = ('id', 'name', 'url')

    def __unicode__(self):
        return self.name


class Compensation(models.Model):

    """Docstring for Compensation. """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    country_category = models.ForeignKey(CountryCategory, blank=True, null=True)
    user_category = models.ForeignKey(UserCategory, blank=True, null=True)
    compensation = models.IntegerField()

    class APITravel(object):
        fields = ('id', 'name', 'country_category', 'user_category',
                  'compensation', 'url')

    def __unicode__(self):
        """TODO: to be defined1. """
        return self.name


class AdvancedPetition(models.Model):

    """Docstring for AdvancedPetition. """
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserProfile)

    dse = models.IntegerField(blank=True, null=True)

    accomondation = models.ForeignKey(Accomondation, blank=True, null=True)
    flight = models.ForeignKey(Flight, blank=True, null=True)
    feeding = models.ForeignKey(FeedingKind, blank=True, null=True)
    non_grnet_quota = models.FloatField(blank=True, null=True, default=0.0)

    def grnet_quota(self):
        if self.non_grnet_quota is None:
            return 100
        return 100 - self.non_grnet_quota
    movement_num = models.CharField(max_length=200, null=True, blank=True)
    compensation = models.ForeignKey(Compensation, blank=True, null=True)

    transport_days_manual = models.IntegerField(blank=True, null=True)

    overnights_num_manual = models.IntegerField(blank=True, null=True)

    compensation_days_manual = models.IntegerField(blank=True, null=True)

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

    required_fields = ('movement_num', 'dse', 'accomondation',
                       'flight', 'feeding', 'non_grnet_quota',
                       'grnet_quota', 'compensation',
                       'expenditure_protocol', 'expenditure_date_protocol',
                       'movement_protocol', 'movement_date_protocol',
                       'transport_days_manual', 'overnights_num_manual',
                       'compensation_days_manual'
                       )

    class APITravel(object):
        fields = ('id', 'petition', 'movement_num', 'dse', 'accomondation',
                  'flight', 'feeding', 'non_grnet_quota', 'grnet_quota',
                  'compensation', 'expenditure_protocol',
                  'expenditure_date_protocol', 'movement_protocol',
                  'movement_date_protocol', 'compensation_petition_protocol',
                  'compensation_petition_date',
                  'compensation_decision_protocol',
                  'compensation_decision_date', 'url',
                  'transport_days_manual', 'overnights_num_manual',
                  'compensation_days_manual'
                  )
        read_only_fields = ('id', 'url', 'petition')

    def clean(self):
        super(AdvancedPetition, self).clean()
        if self.petition.status.id == 4:
            required_validator(self, AdvancedPetition.required_fields)

    def delete(self):
        super(AdvancedPetition, self).delete()
        self.flight.delete()
        self.accomondation.delete()

    def __unicode__(self):
        return str(self.id)


class UserSnapshot(models.Model):
    """
    Abstract model class which gets the information about a user profile at
    the moment he is making a new petition.
    """
    first_name = models.CharField(max_length=200, blank=False, null=False)
    last_name = models.CharField(max_length=200, blank=False, null=False)
    iban = models.CharField(max_length=200, blank=False, null=False,
                            validators=[iban_validation])
    specialtyID = models.ForeignKey(Specialty, blank=False, null=False)
    taxRegNum = models.CharField(max_length=9, blank=False, null=False,
                                 validators=[afm_validator])
    taxOffice = models.ForeignKey(TaxOffice, blank=False, null=False)
    kind = models.ForeignKey(Kind, blank=False, null=False)
    trip_days_before = models.IntegerField(blank=False, null=False,
                                           validators=[MinValueValidator(0)])
    category = models.ForeignKey(UserCategory, blank=False, null=False)

    class Meta:
        abstract = True


class TravelInfo(models.Model):
    """
    An abstract model class that represents travel information.

    Travel information are associated with the duration, departure and arrival
    point, transportation, accomondation, etc.
    """
    taskStartDate = models.DateTimeField(blank=False, null=False)
    taskEndDate = models.DateTimeField(blank=False, null=False)
    depart_date = models.DateTimeField(blank=True, null=True)
    return_date = models.DateTimeField(blank=True, null=True)

    movementCategory = models.ForeignKey(
        MovementCategories, blank=False, null=False)
    departurePoint = models.ForeignKey(
        City, blank=False, null=False, related_name='travel_departure_point')
    arrivalPoint = models.ForeignKey(City, blank=False, null=False,
                                     related_name='travel_arrival_point')
    transportation = models.ForeignKey(Transportation, blank=True, null=True)
    recTransport = models.CharField(max_length=200, blank=True, null=True)
    recAccomondation = models.CharField(max_length=200, blank=True, null=True)
    recCostParticipation = models.FloatField(blank=True, null=True)

    class Meta:
        abstract = True


class SecretarialInfo(models.Model):
    """
    Abstract model which includes information that secretary fills.
    """
    accomondation = models.ForeignKey(Accomondation, blank=True, null=True)
    flight = models.ForeignKey(Flight, blank=True, null=True)
    feeding = models.ForeignKey(FeedingKind, blank=True, null=True)
    non_grnet_quota = models.FloatField(blank=True, null=True, default=0.0)

    movement_num = models.CharField(max_length=200, null=True, blank=True)
    compensation = models.ForeignKey(Compensation, blank=True, null=True)
    transport_days_manual = models.IntegerField(blank=True, null=True)
    overnights_num_manual = models.IntegerField(blank=True, null=True)
    compensation_days_manual = models.IntegerField(blank=True, null=True)
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

    def grnet_quota(self):
        if self.non_grnet_quota is None:
            return 100
        return 100 - self.non_grnet_quota

    class Meta:
        abstract = True


def get_next_dse():
    try:
        return Petition.objects.latest('dse').dse + 1
    except:
        return 1


class Petition(UserSnapshot, TravelInfo, SecretarialInfo):
    SAVED_BY_USER = 1
    SUBMITTED_BY_USER = 2
    SAVED_BY_SECRETARY = 3
    SUBMITTED_BY_SECRETARY = 4
    CANCELLED = 10
    DELETED = 100

    USER_FIELDS = ['first_name', 'last_name', 'iban', 'specialtyID', 'kind',
                   'taxOffice', 'taxRegNum',
                   'category']

    id = models.AutoField(primary_key=True)
    dse = models.IntegerField(
        default=get_next_dse, blank=False, null=False)
    user = models.ForeignKey(UserProfile, blank=False, null=False)
    creationDate = models.DateTimeField(blank=False, null=False,
                                        default=datetime.now())
    updateDate = models.DateTimeField(blank=True, null=True)
    project = models.ForeignKey(Project, blank=False, null=False)
    reason = models.CharField(max_length=500, blank=True, null=True)
    status = models.IntegerField(blank=False, null=False,
                                 default=SAVED_BY_USER)
    additional_expenses_initial = models.FloatField(
        blank=False, null=False, default=0.0,
        validators=[MinValueValidator(0.0)])
    additional_expenses_initial_description = models.CharField(
        max_length=400, blank=True, null=True)

    def save(self, **kwargs):
        if not self.id:
            for field in self.USER_FIELDS:
                setattr(self, field, getattr(self.user, field))
        super(Petition, self).save(**kwargs)

    def clean(self):
        """
        Overrides `clean` method and checks if specified dates are valid.
        """
        super(Petition, self).clean()
        self.validate_dates()

    def validate_dates(self):
        date_validator(self.taskStartDate, self.taskEndDate,
                       ('task start', 'task end'))
        if self.depart_date and self.return_date:
            date_validator(self.depart_date, self.return_date,
                           ('depart', 'return'))

    def compensation_name(self):

        ap = self.arrivalPoint
        if ap is None:
            return ''

        ap_country = ap.country
        if ap_country is None:
            return ''

        ap_country_category = ap_country.category
        if ap_country_category is None:
            return ''

        ap_country_category_name = ap_country_category.name

        user_category = self.user_category

        if user_category is None:
            user_category = self.user.category

        if user_category is None:
            return ''

        user_category_name = user_category.name

        return user_category_name + ap_country_category_name

    def compensation_level(self):
        # comp_object = self.advanced_info.compensation
        # if comp_object is None:
            # return 0
        cn = self.compensation_name()
        if cn == "":
            return 0
        compensation_object = Compensation.objects.get(name=cn)
        if compensation_object:
            return compensation_object.compensation

        return 0

    def transport_days(self):
        if self.advanced_info.transport_days_manual:
            return self.advanced_info.transport_days_manual

        return 0

    def holidays(self, start_date, end_date, holidays=[]):
        """TODO: Docstring for holidays.

        :start_date: TODO
        :end_date: TODO
        :returns: TODO

        """
        workdays = networkdays(start_date, end_date, holidays=[])
        delta = end_date.date() - start_date.date()
        holidays = delta.days - workdays
        return holidays

    def transport_days_proposed(self):
        depart_date = self.depart_date
        return_date = self.return_date

        if depart_date is None or return_date is None:
            return 0
        delta = return_date.date() - depart_date.date()
        result = delta.days - self.holidays(depart_date, return_date)
        return result

    def trip_days_after(self):
        if self.trip_days_before:
            return self.trip_days_before - self.transport_days()
        return 0

    def compensation_days(self):
        if self.advanced_info.compensation_days_manual:
            return self.advanced_info.compensation_days_manual
        return 0

    def compensation_days_proposed(self):
        tsd = self.taskStartDate
        ted = self.taskEndDate

        dd = self.depart_date
        if tsd is None or ted is None or dd is None:
            return 0
        result = ted.date() - tsd.date()
        result = result.days
        delta = dd.date() - tsd.date()
        if delta.days < 0:
            result += 1
        return result

    def max_compensation(self):
        return self.compensation_days() * self.compensation_level()\
            + self.additional_expenses_sum()

    def compensation_final(self):

        comp_sum = self.max_compensation()
        if self.same_day_return_task() or self.advanced_info.feeding.id == 2:
            comp_sum = comp_sum / 2

        if self.advanced_info.feeding.id == 3:
            comp_sum = comp_sum * 25 / 100

        return comp_sum * self.advanced_info.grnet_quota() / 100

    def overnights_num(self):
        if self.advanced_info.overnights_num_manual:
            return self.advanced_info.overnights_num_manual
        return 0

    def overnights_num_proposed(self):
        tsd = self.taskStartDate
        ted = self.taskEndDate

        dd = self.depart_date
        rd = self.return_date
        if tsd is None or ted is None or dd is None or rd is None:
            return 0
        result = ted.date() - tsd.date()
        result = result.days

        delta = dd.date() - tsd.date()
        if delta.days < 0:
            result += 1

        delta = rd.date() - ted.date()

        if delta.days == 1:
            result += 1

        return result

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

        delta = self.taskEndDate.date() - self.taskStartDate.date()

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
            if self.user.category:
                return self.user.category.max_overnight_cost
            return 0

        default_max_overnight_cost = user_category.max_overnight_cost

        if self.is_city_ny():
            return default_max_overnight_cost + 100
        else:
            return default_max_overnight_cost

    def same_day_return_task(self):
        t_end_date = self.taskEndDate
        t_start_date = self.taskStartDate
        r_date = self.return_date
        d_date = self.depart_date
        if t_end_date is None or r_date is None \
                or t_start_date is None or d_date is None:
            return False
        if t_end_date.date() == r_date.date() == t_start_date.date()\
                == d_date.date():
            return True

        return False

    def additional_expenses_sum(self):
        ae = AdditionalExpenses.objects.filter(petition=self).\
            aggregate(Sum('cost'))
        if ae['cost__sum'] is None:
            return 0
        return ae['cost__sum']

    def total_cost(self):
        flight = 0
        if self.advanced_info.flight.flightPrice:
            flight = self.advanced_info.flight.flightPrice
        cost_participation = 0
        if self.recCostParticipation:
            cost_participation = self.recCostParticipation

        total = flight + \
            self.overnights_sum_cost() + \
            self.compensation_final() + cost_participation
        return total

    def __unicode__(self):
        return str(self.id) + "-" + self.project.name


class AdditionalExpenses(models.Model):

    """Docstring for AdditionalWages. """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    cost = models.FloatField()
    petition = models.ForeignKey(Petition)
    user = models.ForeignKey(UserProfile)

    class APITravel:
        fields = ('id', 'name', 'cost', 'petition', 'url')

        @staticmethod
        def get_queryset(request_user):
            return get_queryset_on_group(request_user, AdditionalExpenses)

    def __unicode__(self):
        return self.name + "-" + str(self.id)
