
# -*- coding: utf-8 -*-

from datetime import timedelta
import functools
import pytz
from django.conf import settings
from django.core.exceptions import (
    ValidationError, ObjectDoesNotExist, PermissionDenied)
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import AbstractUser
from django.db import models as md
from django.db.models import Max
from django.db.models import Q
from model_utils import FieldTracker
from rest_framework import serializers
from texpenses.models import common
from texpenses.validators import (
    afm_validator, iban_validation, date_validator,
    start_end_date_validator)
from decimal import Decimal


def update_instance(instance, updated_fields):
    for field, value in updated_fields.iteritems():
        setattr(instance, field, value)


def get_model_missing_fields(instance, excluded=()):
    missing_fields = []

    for field in instance._meta.fields:
        if field.name not in excluded:
            if not bool(getattr(instance, field.name)):
                missing_fields.append(field.name)
    return missing_fields


def _construct_validation_message(fields):
    response = {}
    message = ['This field is required']

    for field in fields:
        response[field] = message
    return response


class TaxOffice(md.Model):

    """ Model which contains all tax offices of Greece. """
    id = md.AutoField(primary_key=True)
    name = md.CharField(max_length=200, blank=False, unique=True)
    description = md.CharField(max_length=300, blank=True)
    address = md.CharField(max_length=20, blank=True)
    email = md.EmailField(blank=True)
    phone = md.CharField(max_length=20, blank=True)

    def __unicode__(self):
        return self.name


class TravelUserProfile(md.Model):

    """
    An abstract model class which include all fields which describe the user
    of `Travel Expenses Application`.

    These fields actually are associated with personal info such as IBAN
    number, Tax Office, etc. as well as, with the kind and specialty of user at
    GRNET.
    """
    iban = md.CharField(max_length=27, blank=False, null=True,
                        validators=[iban_validation])
    specialty = md.CharField(
        max_length=100, choices=common.SPECIALTY, blank=False, null=True)
    tax_reg_num = md.CharField(max_length=9, blank=False, null=True,
                               unique=True, validators=[afm_validator])
    tax_office = md.ForeignKey(
        TaxOffice, blank=False, null=True, on_delete=md.SET_NULL)
    kind = md.CharField(max_length=100, choices=common.KIND, blank=False,
                        null=True)
    user_category = md.CharField(
        max_length=1, choices=common.USER_CATEGORIES,
        blank=False, default='B')

    class Meta:
        abstract = True


class UserProfile(AbstractUser, TravelUserProfile):

    """
    Model for users of `Travel Expenses Application`.

    It actually inherits from `AbstractUser` class of
    `django.contib.auth.models` which define common fields such as first name,
    last name, email, etc and from `TravelUserProfile` which define specific
    fields for the user of `Travel Expenses Application`.
    """

    trip_days_left = md.IntegerField(
        blank=False, default=settings.MAX_HOLIDAY_DAYS,
        validators=[MaxValueValidator(settings.MAX_HOLIDAY_DAYS),
                    MinValueValidator(0)])

    @property
    def apimas_roles(self):
        return [self.user_group()]

    @classmethod
    def check_resource_state_isme(cls, obj, row, request, view):
        return request.user == obj

    def user_group(self):
        groups = self.groups.all()
        # TODO fix this hack.
        if not groups:
            return "Unknown"
        return groups[0].name

    def __unicode__(self):
        return self.first_name + " " + self.last_name + " (username:"\
            + self.username + ")"


def is_manager(manager_id):
    # DRF API creates and updates call the validator with the object
    # instead of the id for some reason
    if isinstance(manager_id, UserProfile):
        manager = manager_id
    else:
        manager = UserProfile.objects.get(id=manager_id)
    manager_group = manager.user_group()
    if manager_group != "MANAGER":
        raise ValidationError('The chosen user must be a MANAGER')


class UserDaysLeft(md.Model):
    """
    A model to store remaining trip days before resetting user's
    trip_days_left field every new year.
    """
    user = md.ForeignKey(UserProfile)
    created_at = md.DateField()
    days_left = md.IntegerField()


class Project(md.Model):

    """
    Model which describes a project which GRNET has assumed.

    A project is described by its name, accounting code and the GRNET member
    who managed it.
    """
    id = md.AutoField(primary_key=True)
    name = md.CharField(max_length=500, blank=False, unique=True)
    accounting_code = md.CharField(max_length=20, blank=False)
    active = md.BooleanField(default=True)
    manager = md.ForeignKey(
        UserProfile, null=True, blank=True, validators=[is_manager],
        on_delete=md.SET_NULL)

    def __unicode__(self):
        return self.name


class Country(md.Model):

    """
    Model for countries.

    A country is descibed by its category which define the amount of
    compensation combined with the user category.
    """

    id = md.AutoField(primary_key=True)
    name = md.CharField(max_length=100, blank=False, unique=True)
    category = md.CharField(
        choices=common.CATEGORIES, max_length=1, default='A')
    currency = md.CharField(
        max_length=3, choices=common.CURRENCIES, blank=False,
        default=settings.DEFAULT_CURRENCY)

    def __unicode__(self):
        """TODO: to be defined1. """
        return self.name


class City(md.Model):

    """Model for cities. """
    id = md.AutoField(primary_key=True)
    name = md.CharField(max_length=100, blank=False)
    country = md.ForeignKey(Country, blank=False, on_delete=md.PROTECT)
    timezone = md.CharField(max_length=100)

    def __unicode__(self):
        """TODO: to be defined. """
        return self.name


class CityDistances(md.Model):

    """ Model which holds the distance between various Greek Cities"""
    id = md.AutoField(primary_key=True)
    from_city = md.ForeignKey(City, related_name='from_city')
    to_city = md.ForeignKey(City, related_name='to_city')
    distance = md.FloatField()

    def __unicode__(self):
        return str(self.id) + '-' + self.from_city.name + ' to ' + \
            self.to_city.name


class Accommodation(md.Model):

    """
    An abstract model that represents the accommodation related info
    """

    accommodation_cost = md.DecimalField(max_digits=settings.DECIMAL_MAX_DIGITS,
                                         decimal_places=settings.DECIMAL_PLACES,
                                         blank=False, default=0.0,
                                         validators=[MinValueValidator(0.0)])
    accommodation_default_currency = md.CharField(
        max_length=3, blank=False, default=settings.DEFAULT_CURRENCY)
    accommodation_local_cost = md.DecimalField(
        max_digits=settings.DECIMAL_MAX_DIGITS,
        decimal_places=settings.DECIMAL_PLACES, blank=False, default=0.0,
        validators=[MinValueValidator(0.0)])
    accommodation_local_currency = md.CharField(
        max_length=3, blank=True, choices=common.CURRENCIES)
    accommodation_payment_way = md.CharField(
        max_length=5, choices=common.WAYS_OF_PAYMENT, blank=False,
        default='NON')
    accommodation_payment_description = md.CharField(
        max_length=200, null=True)

    accommodation_total_cost = md.DecimalField(
            max_digits=settings.DECIMAL_MAX_DIGITS,
            decimal_places=settings.DECIMAL_PLACES,
            blank=False, default=0.0,
            validators=[MinValueValidator(0.0)])
    accommodation_total_local_cost = md.DecimalField(
        max_digits=settings.DECIMAL_MAX_DIGITS,
        decimal_places=settings.DECIMAL_PLACES, blank=False, default=0.0,
        validators=[MinValueValidator(0.0)])

    class Meta:
        abstract = True


class Transportation(md.Model):

    """
    An abstract model that represents the transportation related info
    """
    transportation_cost = md.DecimalField(
        max_digits=settings.DECIMAL_MAX_DIGITS,
        decimal_places=settings.DECIMAL_PLACES,
        blank=False, default=0.0, validators=[MinValueValidator(0.0)])
    transportation_default_currency = md.CharField(
        max_length=3, blank=False, default=settings.DEFAULT_CURRENCY)
    transportation_payment_way = md.CharField(
        max_length=5, choices=common.WAYS_OF_PAYMENT,
        blank=False, default='NON')
    transportation_payment_description = md.CharField(
        max_length=200, null=True)

    class Meta:
        abstract = True


class TravelInfo(Accommodation, Transportation):

    """
    An abstract model class that represents travel information.

    Travel information are associated with the duration, departure and arrival
    point, transportation, accommodation, etc.
    """
    depart_date = md.DateTimeField(null=True)
    return_date = md.DateTimeField(null=True)
    departure_point = md.ForeignKey(
        City, blank=True, null=True, related_name='travel_departure_point',
        on_delete=md.PROTECT)
    arrival_point = md.ForeignKey(
        City, blank=True, null=True, related_name='travel_arrival_point',
        on_delete=md.PROTECT)
    means_of_transport = md.CharField(
        choices=common.TRANSPORTATION, max_length=10, blank=False,
        default='AIR')
    transport_days_manual = md.PositiveSmallIntegerField(
        blank=False, default=0)
    overnights_num_manual = md.PositiveSmallIntegerField(
        blank=False, default=0)
    compensation_days_manual = md.PositiveSmallIntegerField(
        blank=False, default=0)
    meals = md.CharField(max_length=10, choices=common.MEALS,
                         blank=False, default='NON')
    travel_petition = md.ForeignKey(
        'Petition', related_name='travel_info', on_delete=md.PROTECT)
    distance = md.FloatField(blank=False, default=0.0,
                             validators=[MinValueValidator(0.0)])
    no_transportation_calculation = md.BooleanField(default=False)

    tracked_date_fields = ['depart_date', 'return_date']
    tracker = FieldTracker(fields=tracked_date_fields)
    tracked_location_fields = ['departure_point', 'arrival_point']
    location_tracker = FieldTracker(fields=tracked_location_fields)

    tracked_means_of_tranport_fields = ['means_of_transport']
    means_of_transport_tracker = FieldTracker(
        fields=tracked_means_of_tranport_fields)
    travel_petition_buffer = None

    class Meta:
        ordering = ['depart_date',]

    def clean(self, petition):
        extended_validation_statuses = [Petition.SUBMITTED_BY_USER,
                                        Petition.USER_COMPENSATION_SUBMISSION,
                                        Petition.
                                        SECRETARY_COMPENSATION_SUBMISSION]
        self._validate_depart_arrival_points()
        self._validate_city_distance_exists()

        if self.depart_date and self.return_date \
                and petition.task_end_date:
            dates = ((self.depart_date, self.return_date),
                     (self.depart_date, petition.task_end_date))
            labels = (('depart', 'return'), ('depart', 'task end'))
            if petition.status in extended_validation_statuses:
                date_validator('depart_date', self.depart_date)
                date_validator('return_date', self.return_date)

            start_end_date_validator(dates, labels)

        # T2860: Remove validation
        #self.validate_overnight_cost(petition)

        super(TravelInfo, self).clean()

    def _endpoints_are_set(self):
        return None not in (self.departure_point, self.arrival_point)

    def _validate_depart_arrival_points(self):

        if self._endpoints_are_set():
            base_country_name = settings.BASE_COUNTRY
            departure_country_name = self.departure_point.country.name

            arrival_point_name = self.arrival_point.name
            departure_point_name = self.departure_point.name
            if departure_point_name == arrival_point_name:
                raise ValidationError(u"Departure city and arrival city should"
                                      " not be the same.")

    def _validate_city_distance_exists(self):
        if self.is_abroad() or not self.means_of_transport_is_car_or_bike():
            return
        if not CityDistances.objects.filter(from_city=self.departure_point,
                                        to_city=self.arrival_point).exists():
            raise ValidationError(u'No distance found for these cities.')

    def _set_travel_manual_field_defaults(self):
        self.transport_days_manual = self.transport_days_proposed()
        self.compensation_days_manual = self.compensation_days_proposed()

    def is_abroad(self):
        if not self._endpoints_are_set():
            return True
        base_country_name = settings.BASE_COUNTRY
        arrival_country_name = self.arrival_point.country.name
        return arrival_country_name != base_country_name

    def is_athens_or_thesniki(self):
        if not self._endpoints_are_set():
            return False
        return self.arrival_point.name in (u'Αθήνα', u'Θεσσαλονίκη')

    def locations_have_changed(self):
        return any(self.location_tracker.has_changed(field)
                   for field in self.tracked_location_fields)

    def means_of_transport_have_changed(self):
        return any(self.means_of_transport_tracker.has_changed(field)
                   for field in self.tracked_means_of_tranport_fields)

    def means_of_transport_is_car_or_bike(self):
        return self.means_of_transport in ('BIKE', 'CAR')

    def means_of_transport_is_train_ship_bus(self):
        return self.means_of_transport in ('TRAIN', 'SHIP', 'BUS')

    def transportation_should_be_compensated(self):
        return self.means_of_transport_is_car_or_bike() or\
               (self.means_of_transport_is_train_ship_bus() and
                self.transportation_payment_way == u'VISA')

    def transportation_cost_should_be_calculated(self):
        if self.no_transportation_calculation:
            return False
        return self.means_of_transport_is_car_or_bike()

    @property
    def local_depart_date(self):
        city = self.departure_point
        city_timezone = pytz.timezone(city.timezone)
        return self.depart_date.astimezone(city_timezone)

    @property
    def local_return_date(self):
        city = self.arrival_point
        city_timezone = pytz.timezone(city.timezone)
        return self.return_date.astimezone(city_timezone)

    def calculate_transportation_cost(self):
        # we cannot use location tracker as it's not guaranteed
        # there will be a calculation on every save
        try:
            self.distance = CityDistances.objects.get(
                from_city=self.departure_point,
                to_city=self.arrival_point).distance
        except CityDistances.DoesNotExist:
            self.distance = 0.0

        distance_factor = common.\
            MEANS_OF_TRANSPORT_DISTANCE_FACTOR[self.means_of_transport]
        self.transportation_cost = 2 * distance_factor * self.distance

    def save(self, *args, **kwargs):
        new_object = kwargs.pop('new_object', False)
        if self.transportation_cost_should_be_calculated():
            self.calculate_transportation_cost()
        super(TravelInfo, self).save(*args, **kwargs)

    def validate_overnight_cost(self, petition):
        """
        Checks that the accommodation_cost does not surpass the maximum
        overnight limit based on the category of user.

        :raises: ValidationError if accommodation cost exceeds the allowable
        limit.
        """

        EXTRA_COST = 100

        max_overnight_cost = common.MAX_OVERNIGHT_COST[
            petition.user_category][0] if self.is_abroad() else \
            common.MAX_OVERNIGHT_COST[petition.user_category][1]

        max_overnight_cost += EXTRA_COST if self.is_city_ny() else 0
        max_overnight_cost += max_overnight_cost * 0.2\
            if self.is_athens_or_thesniki() else 0

        if self.same_day_return_task(petition=petition) and \
                self.accommodation_cost:
            raise ValidationError('This is a same day return travel,'
                                  ' overnight cost is not acceptable.')


    def transport_days_proposed(self):
        """
        Method which calculates the number of transport days based on the
        return and departure dates specified on petition.

        Weekends are ignored.

        :returns: Proposed transport_days.
        """

        WEEKENDS = [5, 6]
        if self.depart_date is None or self.return_date is None:
            return 0
        time_period = (self.depart_date + timedelta(x) for x in xrange(
            (self.return_date.date() - self.depart_date.date()).days + 1))

        return sum(1 for day in time_period if day.weekday() not in WEEKENDS)

    def overnights_num_proposed(self, task_start_date=None, task_end_date=None):
        """
        Method which calculates the proposed number of days that traveller
        should overnight.

        The number of days is calculated by return and departure dates.
        There are two possible scenarios:
            1) One more day is added to the total overnight days if the
               departure date is one day before from the date when task starts.
            2) One more day is added to the total overnight days if the
               return date is one day after from the date when task ends.

        :param task_start_date: Date when, transportation_cost task starts.
        :param task_end_date: Date when task ends.
        :returns: The proposed overinight days.
        """

        task_start_date = (task_start_date or
                           self.travel_petition.task_start_date)
        task_end_date = task_end_date or self.travel_petition.task_end_date

        if not (self.return_date and self.depart_date and
                task_start_date and task_end_date):
            return 0

        first_day = task_start_date - timedelta(days=1) if (
            task_start_date - self.depart_date).days >= 1 else self.depart_date
        last_day = task_end_date + timedelta(days=1) if (
            self.return_date - task_end_date).days >= 1 else self.return_date
        return ((last_day.date() - first_day.date()).days
                if first_day < last_day else 0)

    def overnight_cost(self):
        """ Returns total overnight cost. """
        #return self.accommodation_cost * self.overnights_num_manual
        return self.accommodation_total_cost

    def is_city_ny(self):
        """
        Checks if city is `New YORK` and returns True if this is the case;
        False otherwise.
        """
        if self.arrival_point:
            return self.arrival_point.name.lower() == "new york"
        else:
            return False

    def compensation_level(self):
        """Calculates the compensation level based on country and user category
        :returns:compensation level

        """

        if not self.arrival_point:
            return 0.0
        return common.COMPENSATION_CATEGORIES[(
            self.travel_petition.user_category,
            self.arrival_point.country.category)]

    def same_day_return_task(self, petition=None):
        """
        This method checks that the t
        """
        task_start_date, task_end_date = None, None
        if petition is None:
            task_start_date = self.travel_petition.task_start_date
            task_end_date = self.travel_petition.task_end_date
        else:
            task_start_date = petition.task_start_date
            task_end_date = petition.task_end_date

        if task_end_date is None or \
                self.return_date is None \
                or task_start_date is None \
                or self.depart_date is None:
            return False
        return task_end_date.date() == self.return_date.date() \
            == task_start_date.date() == self.depart_date.date()

    def compensation_days_proposed(self):
        """
        A method that calculates compensation days in case no related value is
        inserted by secretary

        Algorithm description:

            [task_end_date] - [task_start_date] + 1
            +1 if { [depart_date] < [task_start_date] }
        """
        task_start_date = self.travel_petition.task_start_date.replace(
            hour=0, minute=0) if self.travel_petition.task_start_date else (
                self.travel_petition.task_start_date)
        task_end_date = self.travel_petition.task_end_date.replace(
            hour=0, minute=0) if self.travel_petition.task_end_date else (
            self.travel_petition.task_end_date)

        depart_date = self.depart_date.replace(
            hour=0, minute=0) if self.depart_date else self.depart_date
        return_date = self.return_date.replace(
            hour=0, minute=0) if self.return_date else self.return_date

        if not (depart_date and return_date and task_start_date and
                task_end_date):
            return 0

        if self.same_day_return_task():
            return 1

        compensation_days = 0

        start_date_delta = (task_start_date - depart_date).days


        if return_date <= task_end_date:
            if start_date_delta == 0:
                compensation_days = (
                    return_date - task_start_date).days + 1
            if start_date_delta > 0:
                compensation_days = (
                    return_date - task_start_date).days + 1 if (
                    self.travel_petition.has_multiple_destinations()) else (
                        return_date - task_start_date).days + 2

            if start_date_delta < 0:
                compensation_days = (
                    return_date - depart_date).days + 1 if (
                        return_date == task_end_date) else (
                            (return_date - depart_date).days if (
                            self.travel_petition.has_multiple_destinations())\
                            else (
                                (return_date - depart_date).days + 1)
                        )
        else:
            if start_date_delta > 0:
                compensation_days = (task_end_date - task_start_date).days + 2
            if start_date_delta == 0:
                compensation_days = (task_end_date - task_start_date).days + 1
            if start_date_delta < 0:
                compensation_days = (
                    task_end_date - depart_date).days + 1

        if compensation_days < 0:
            return 0
        return compensation_days

    def compensation_cost_single_day(self):
        """
        Calculates the single day compensation
        :returns: The maximum possible compensation per day

        """
        percentage = 100
        max_compensation = self.compensation_level()

        if self.is_abroad() and self.same_day_return_task():
            max_compensation *= 0.5

        compensation_proportion = common.COMPENSATION_PROPORTION[self.meals] \
            if self.meals else 1

        if not self.is_abroad():
            if self.meals not in ('SEMI', 'FULL'):
                if self.same_day_return_task() and (
                    self.distance >= (
                        common.TRANSPORTATION_MODE_MIN_DISTANCE[
                            self.means_of_transport])):
                    compensation_proportion = 0.5

                if self.same_day_return_task() and (
                    self.distance <= (
                        common.TRANSPORTATION_MODE_MIN_DISTANCE[
                            self.means_of_transport])):
                    if self.means_of_transport == 'AIR':
                        compensation_proportion = 0.5
                    else:
                        compensation_proportion = 0.25

            if self.meals == 'FULL':
                compensation_proportion = 0

        return max_compensation * compensation_proportion * (
            self.travel_petition.grnet_quota() / percentage) if not (
                self.travel_petition.withdrawn) else 0

    def compensation_cost(self):
        """Calculates the compensation for all compensation days,
        :returns: The maximum possible compensation

        """
        return self.compensation_cost_single_day() * (
            self.compensation_days_manual) if not (
                self.travel_petition.withdrawn) else 0

    def __unicode__(self):
        return str(self.travel_petition.dse) + "-" + \
            self.travel_petition.project.name +\
            '-' + str(self.travel_petition.id)


class SecretarialInfo(md.Model):

    """
    Abstract model which includes information that secretary fills.
    """
    non_grnet_quota = md.FloatField(
        blank=False, default=0.0, validators=[MinValueValidator(0.0)])

    movement_id = md.CharField(max_length=200, null=True, blank=True)
    expenditure_protocol = md.CharField(
        max_length=256, null=True, blank=True)
    expenditure_date_protocol = md.DateTimeField(
        blank=True, null=True)
    movement_protocol = md.CharField(
        max_length=256, null=True, blank=True)
    movement_date_protocol = md.DateTimeField(
        blank=True, null=True)
    compensation_petition_protocol = md.CharField(
        max_length=256, null=True, blank=True)
    compensation_petition_date = md.DateTimeField(
        blank=True, null=True)
    compensation_decision_protocol = md.CharField(
        max_length=256, null=True, blank=True)
    compensation_decision_date = md.DateTimeField(
        blank=True, null=True)
    manager_movement_approval = md.BooleanField(default=False,
                                                db_index=True)
    manager_cost_approval = md.BooleanField(default=False, db_index=True)
    timesheeted = md.BooleanField(default=False, db_index=True)

    MAX_GRNET_QUOTA = 100

    def grnet_quota(self):
        if self.non_grnet_quota is None:
            return self.MAX_GRNET_QUOTA
        return self.MAX_GRNET_QUOTA - self.non_grnet_quota

    class Meta:
        abstract = True


class ParticipationInfo(md.Model):

    """
    An abstract model that represents the participation cost related info
    """
    participation_cost = md.DecimalField(
        max_digits=settings.DECIMAL_MAX_DIGITS,
        decimal_places=settings.DECIMAL_PLACES,
        blank=False, default=0.0, validators=[MinValueValidator(0.0)])

    participation_default_currency = md.CharField(
        max_length=3, blank=False, default=settings.DEFAULT_CURRENCY)
    participation_local_cost = md.DecimalField(
        max_digits=settings.DECIMAL_MAX_DIGITS,
        decimal_places=settings.DECIMAL_PLACES,
        blank=True, default=0.0, validators=[MinValueValidator(0.0)])
    participation_local_currency = md.CharField(
        max_length=3, blank=True, choices=common.CURRENCIES)
    participation_payment_way = md.CharField(
        max_length=10, choices=common.WAYS_OF_PAYMENT, blank=False,
        default='NON')
    participation_payment_description = md.CharField(
        max_length=200, blank=True, null=True)

    class Meta:
        abstract = True


class AdditionalCosts(md.Model):

    """
    An abstract model that represents the additional costs related info
    """
    additional_expenses_initial = md.DecimalField(
        max_digits=settings.DECIMAL_MAX_DIGITS,
        decimal_places=settings.DECIMAL_PLACES, blank=False, default=0.0,
        validators=[MinValueValidator(0.0)])
    additional_expenses_default_currency = md.CharField(
        max_length=3, blank=False, default=settings.DEFAULT_CURRENCY)
    additional_expenses_initial_description = md.CharField(
        max_length=400, blank=True, null=True)

    additional_expenses = md.DecimalField(
        max_digits=settings.DECIMAL_MAX_DIGITS,
        decimal_places=settings.DECIMAL_PLACES,
        blank=False, default=0.0, validators=[MinValueValidator(0.0)])
    additional_expenses_local_currency = md.CharField(
        max_length=3, blank=False, default=settings.DEFAULT_CURRENCY)
    additional_expenses_description = md.CharField(
        max_length=400, blank=True, null=True)
    additional_expenses_grnet = md.DecimalField(
        max_digits=settings.DECIMAL_MAX_DIGITS,
        decimal_places=settings.DECIMAL_PLACES,
        blank=False, default=0.0, validators=[MinValueValidator(0.0)])

    class Meta:
        abstract = True


class Petition(SecretarialInfo, ParticipationInfo, AdditionalCosts):
    SAVED_BY_USER = 1
    SUBMITTED_BY_USER = 2
    SAVED_BY_SECRETARY = 3
    SUBMITTED_BY_SECRETARY = 4
    APPROVED_BY_PRESIDENT = 5
    USER_COMPENSATION = 6
    USER_COMPENSATION_SUBMISSION = 7
    SECRETARY_COMPENSATION = 8
    SECRETARY_COMPENSATION_SUBMISSION = 9
    PETITION_FINAL_APPOVAL = 10

    SUBMISSION_STATUSES = [SUBMITTED_BY_USER, SUBMITTED_BY_SECRETARY,
                           USER_COMPENSATION_SUBMISSION,
                           SECRETARY_COMPENSATION_SUBMISSION]

    # Fields that are copied from user object.
    USER_FIELDS = ['first_name', 'last_name', 'iban', 'specialty', 'kind',
                   'tax_office', 'tax_reg_num', 'user_category']

    id = md.AutoField(primary_key=True)

    # travel user profile fields
    iban = md.CharField(max_length=27, blank=False,
                        validators=[iban_validation])
    specialty = md.CharField(
        max_length=100, choices=common.SPECIALTY, blank=False)
    tax_reg_num = md.CharField(max_length=9, blank=False,
                               validators=[afm_validator])
    tax_office = md.ForeignKey(TaxOffice, blank=False, on_delete=md.PROTECT)
    kind = md.CharField(max_length=100, choices=common.KIND, blank=False)
    user_category = md.CharField(
        max_length=1, choices=common.USER_CATEGORIES,
        blank=False, default='B')

    dse = md.IntegerField(
        blank=False, validators=[MinValueValidator(1)])

    user = md.ForeignKey(UserProfile, blank=False, on_delete=md.PROTECT)
    task_start_date = md.DateTimeField(
        blank=True, null=True)
    task_end_date = md.DateTimeField(
        blank=True, null=True)
    created = md.DateTimeField(blank=False, default=timezone.now)
    updated = md.DateTimeField(blank=False, default=timezone.now)
    deleted = md.BooleanField(default=False, db_index=True)
    project = md.ForeignKey(Project, blank=False, on_delete=md.PROTECT)
    reason = md.CharField(max_length=500, blank=True, null=True)
    user_recommendation = md.CharField(
        max_length=500, blank=True, null=True)
    secretary_recommendation = md.CharField(
        max_length=500, blank=True, null=True)

    status = md.IntegerField(blank=False, db_index=True)

    first_name = md.CharField(max_length=200, blank=False, null=True)
    last_name = md.CharField(max_length=200, blank=False, null=True)

    travel_report = md.CharField(max_length=1000, blank=True, null=True)

    compensation_alert = md.BooleanField(default=False, db_index=True)
    withdrawn = md.BooleanField(default=False, db_index=True)

    travel_files = md.FileField(upload_to=common.user_directory_path,
                                null=True, blank=True)

    total_cost_manual = md.DecimalField(
        max_digits=settings.DECIMAL_MAX_DIGITS,
        decimal_places=settings.DECIMAL_PLACES,
        blank=False, default=0.0, validators=[MinValueValidator(0.0)])
    total_cost_change_reason = md.CharField(max_length=1000, blank=True,
                                            null=True)

    tracked_cost_field = ['total_cost_manual']
    cost_tracker = FieldTracker(fields=tracked_cost_field)
    is_total_manual_cost_set = md.BooleanField(default=False, db_index=True)
    initial_user_days_left = md.IntegerField(default=0)
    transport_days_total = md.IntegerField(default=0)

    tracked_fields = ['task_start_date', 'task_end_date']
    tracker = FieldTracker()


    @classmethod
    def check_resource_state_usersaved(cls, obj, row, request, view):
        return obj.status == cls.SAVED_BY_USER

    @classmethod
    def check_resource_state_ownedusersaved(cls, obj, row, request, view):
        return request.user == obj.user and obj.status == cls.SAVED_BY_USER

    @classmethod
    def check_resource_state_usersubmitted(cls, obj, row, request, view):
        return obj.status == cls.SUBMITTED_BY_USER

    @classmethod
    def check_resource_state_ownedusersubmitted(cls, obj, row, request, view):
        return request.user == obj.user and obj.status == cls.SUBMITTED_BY_USER

    @classmethod
    def check_resource_state_secretarysaved(cls, obj, row, request, view):
        return obj.status == cls.SUBMITTED_BY_USER or \
            obj.status == cls.SAVED_BY_SECRETARY

    @classmethod
    def check_resource_state_secretarysubmitted(cls, obj, row, request, view):
        return obj.status == cls.SUBMITTED_BY_SECRETARY

    @classmethod
    def check_resource_state_presidentapproved(cls, obj, row, request, view):
        return obj.status == cls.APPROVED_BY_PRESIDENT

    @classmethod
    def check_resource_state_ownedpresidentapproved(cls, obj, row, request, view):
        return request.user == obj.user and obj.status == cls.APPROVED_BY_PRESIDENT

    @classmethod
    def check_resource_state_usercompensationsaved(cls, obj, row, request,
                                                   view):
        return obj.status == cls.USER_COMPENSATION

    @classmethod
    def check_resource_state_ownedusercompensationsaved(cls, obj, row, request,
                                                   view):
        return request.user == obj.user and obj.status == cls.USER_COMPENSATION

    @classmethod
    def check_resource_state_usercompensationsubmitted(cls, obj, row, request,
                                                       view):
        return obj.status == cls.USER_COMPENSATION_SUBMISSION

    @classmethod
    def check_resource_state_ownedusercompensationsubmitted(cls, obj, row, request,
                                                       view):
        return request.user == obj.user and obj.status == cls.USER_COMPENSATION_SUBMISSION

    @classmethod
    def check_resource_state_secretarycompensationsaved(cls, obj, row,
                                                        request, view):
        return obj.status == cls.SECRETARY_COMPENSATION

    @classmethod
    def check_resource_state_secretarycompensationsubmitted(cls, obj, row,
                                                            request, view):
        return obj.status == cls.SECRETARY_COMPENSATION_SUBMISSION

    @classmethod
    def check_resource_state_presidentcompensationapproved(cls, obj, row,
                                                           request, view):
        return obj.status == cls.PETITION_FINAL_APPOVAL

    @classmethod
    def check_resource_state_presidentcompensationapproved(cls, obj, row,
                                                           request, view):
        return obj.status == cls.PETITION_FINAL_APPOVAL

    @classmethod
    def check_resource_state_belongs(cls, obj, row, request, view):
        return request.user == obj.user

    def __init__(self, *args, **kwargs):
        super(Petition, self).__init__(*args, **kwargs)
        user = kwargs.get('user', None)
        if not self.dse:
            self.set_next_dse()

        if user:
            for field in self.USER_FIELDS:
                setattr(self, field, getattr(user, field))



    def clean(self):
        """
        Overrides `clean` method and checks if specified dates are valid.
        """
        super(Petition, self).clean()
        if self.task_start_date and self.task_end_date:
            start_end_date_validator(
                ((self.task_start_date, self.task_end_date),),
                (('task start', 'task end'),))

    def total_cost_manual_haschanged(self):
        return self.cost_tracker.has_changed('total_cost_manual')

    def _set_manual_total_cost(self):

        if self.total_cost_manual_haschanged() and (
            self.cost_tracker.previous('total_cost_manual')):
            self.is_total_manual_cost_set = True
        if not self.is_total_manual_cost_set:
            self.total_cost_manual = self.total_cost_calculated()

    def save(self, *args, **kwargs):
        self.updated = timezone.now()
        self._set_movement_id()
        # self._set_manual_total_cost()
        super(Petition, self).save(*args, **kwargs)

    def mark_as_deleted(self):
        """
        Sets petition's status as `DELETED`.
        """
        self.deleted = True
        self.save()

    def unmark_deleted(self):
        """
        Restore a previously "deleted" petition.
        """
        self.deleted = False
        self.save()

    def transition_is_allowed(self, new_status):
        """
        Check if the transition of a petition is  allowed.

        Transition is allowed only if there is not another petition with the
        same dse but on greater status. Moreover, new status must not be
        equal with the current status.

        :param new_status: New status to transit petition.
        """
        return not Petition.objects.filter(
            dse=self.dse, status__gt=self.status,
            deleted=False).exists() and not new_status == self.status

    def set_trip_days_left(self):
        if self.transport_days() and \
                self.transport_days_total != self.transport_days():
            self.user.trip_days_left -= self.transport_days()
            self.user.trip_days_left += self.transport_days_total
            self.user.save()
            self.transport_days_total = self.transport_days()
            self.save()

    def status_transition(self, new_status, delete=True, **kwargs):
        """
        This method transits a petition to a new status.

        Actually, this method marks current petition as deleted (only if it
        specified by `delete` parameter) and creates
        a copied petition that is not marked as deleted and it points to the
        new status.

        However, a transition is not allowed if another petition with the
        corresponding dse is on greater status than the current one.

        :param new_status: New status to transit petition.
        :param delete: If true then deletes the petition which is transitted to
        a new status.
        :returns: Id of the created petition.
        """
        if not self.transition_is_allowed(new_status):
            raise PermissionDenied('Petition transition is not allowed.')
        travel_info = self.travel_info.all()
        if delete:
            self.mark_as_deleted()
        petition_modifications = kwargs.pop('petition_data', {})
        travel_info_modifications = kwargs.pop(
            'travel_info_data', [{}] * len(travel_info))
        self.id = None
        self.status = new_status
        self.deleted = False
        update_instance(self, petition_modifications)

        # withdrawn = kwargs.pop('withdrawn', False)
        # if withdrawn:
            # self.withdrawn = False

        self.save()
        for i, travel_obj in enumerate(travel_info):
            travel_obj.id = None
            update_instance(travel_obj, travel_info_modifications[i])
            travel_obj.travel_petition = self
            travel_obj.save()
        self.travel_info.add(*travel_info)
        return self.id

    def has_multiple_destinations(self):
        if self.travel_info.count() > 1:
            return True
        return False

    def withdraw(self, **kwargs):
        """
        Withdraw a petition.

        """
        proceed = kwargs.pop('proceed', False)
        if proceed:
            if self.status == self.SUBMITTED_BY_SECRETARY:
                self.proceed(status=self.SECRETARY_COMPENSATION)
            else:
                self.proceed()
        self.withdrawn = True
        self.user.trip_days_left += self.transport_days()
        self.user.save()
        self.save()

    def cancel_withdrawal(self, **kwargs):
        """
        Cancels petition withdrawal.

        """

        roll_back = kwargs.pop('roll_back',False)
        if roll_back:
            self.status_transition(self.SAVED_BY_SECRETARY)

        self.withdrawn = False
        self.user.trip_days_left -= self.transport_days()
        self.user.save()
        self.save()

    def proceed(self, **kwargs):
        """
        Proceed petition to the next status.


        If next status is one of the submission statuses, then a checker
        is triggered and tests if the petition is completed.
        """
        next_status = kwargs.pop('status', 0)
        if next_status == 0:
            next_status = self.status + 1

        #submit = next_status in Petition.SUBMISSION_STATUSES or\
        #    kwargs.pop('delete', False)
        # Always mark previous instances as deleted
        submit = True
        missing_fields = self.get_missing_fields()
        if next_status in Petition.SUBMISSION_STATUSES \
                and missing_fields:
            raise serializers.ValidationError(
                _construct_validation_message(missing_fields))
        return self.status_transition(next_status, delete=submit, **kwargs)

    def get_missing_fields(self):
        """

        Check if all fields of petition along with the fields of many to many
        related objects have been initialized.
        """
        missing_fields = []
        excluded = self.excluded_per_status.get(self.status, [])
        petition_missing_fields = get_model_missing_fields(self, excluded)
        missing_fields.extend(petition_missing_fields)

        travel_info = self.travel_info.all()

        if travel_info:
            for travel_obj in travel_info:
                travel_info_missing_fields = []
                travel_info_excluded = \
                    self.excluded_ti_per_status.get(self.status,[])
                travel_info_missing_fields.extend(get_model_missing_fields(
                    travel_obj,travel_info_excluded))
                missing_fields.extend(travel_info_missing_fields)

        return missing_fields

    @property
    def local_task_start_date(self):
        task_start = self.task_start_date
        travel_infos = list(self.travel_info.all())

        # If task starts before, take first city's timezone
        city = travel_infos[0].arrival_point

        for travel in travel_infos:
            if task_start >= travel.depart_date and task_start <= travel.return_date:
                city = travel.arrival_point
                break

        city_timezone = pytz.timezone(city.timezone)
        return self.task_start_date.astimezone(city_timezone)

    @property
    def local_task_end_date(self):
        task_end = self.task_end_date
        travel_infos = list(self.travel_info.all())

        # If task starts after, take last city's timezone
        city = travel_infos[-1].arrival_point

        for travel in travel_infos:
            if task_end >= travel.depart_date and task_end <= travel.return_date:
                city = travel.arrival_point
                break

        city_timezone = pytz.timezone(city.timezone)
        return self.task_end_date.astimezone(city_timezone)

    def compensation_cost(self):
        return sum([travel_obj.compensation_cost()
                    for travel_obj in self.travel_info.all()])

    def revoke(self, **kwargs):
        """ Revoke a petition the previous status. """
        return self.status_transition(self.status - 1, **kwargs)

    def set_next_dse(self):
        """
        This method sets the default value for DSE field.

        This value is serial number according to the existing petitions.
        If there is no any petition, then `DSE` is set to `1`.
        """
        try:
            self.dse = Petition.objects.latest('dse').dse + 1
        except ObjectDoesNotExist:
            self.dse = 1

    def _set_movement_id(self):
        """
        This method sets the movement_id value to be equal to dse's one
        """
        self.movement_id = str(self.dse)

    def transport_days(self):
        """ Gets the total number of transport days for all destinations. """
        return sum(travel.transport_days_manual
                   for travel in self.travel_info.all())

    def trip_days_before(self):
        return self.initial_user_days_left if self.initial_user_days_left \
            else self.user.trip_days_left

    def trip_days_after(self):
        days_before = self.initial_user_days_left \
            if self.initial_user_days_left else self.user.trip_days_left
        return days_before - self.transport_days() \
            if not self.withdrawn else days_before

    def overnights_num(self):
        """ Gets the number of total overnight days for all destinations. """
        return sum(travel.overnights_num_manual
                   for travel in self.travel_info.all())

    def compensation_days_num(self):
        """ Gets the number of total compensation days for all destinations. """
        return sum(travel.compensation_days_manual
                   for travel in self.travel_info.all())

    def overnights_proposed(self):
        return sum(travel.overnights_num_proposed(
            self.task_start_date, self.task_end_date)
            for travel in self.travel_info.all())

    def overnights_sum_cost(self):
        """ Total accommodation for all destinations. """
        return sum(travel.overnight_cost()
                   for travel in self.travel_info.all())

    def overnights_not_to_be_compensated(self):
        overnights_compensation = 0
        for travel in self.travel_info.all():
            overnights_compensation += travel.overnight_cost()

        return overnights_compensation

    def task_duration(self):
        """ Gets the duration of task. """
        if not (self.task_start_date and self.task_end_date):
            return 0
        return (self.task_end_date - self.task_start_date).days

    def transportation_cost_to_be_compensated(self):

        transportation_compensation = 0

        for travel_obj in self.travel_info.all():
            if travel_obj.transportation_should_be_compensated():
                transportation_compensation += travel_obj.transportation_cost

        return transportation_compensation

    def transportation_cost_not_to_be_compensated(self):

        transportation_compensation = 0

        for travel_obj in self.travel_info.all():
            if not travel_obj.transportation_should_be_compensated():
                transportation_compensation += travel_obj.transportation_cost

        return transportation_compensation

    def compensation_final(self):
        """TODO: Docstring for compensation_final.
        :returns: TODO

        """
        compensation_cost_sum = Decimal(sum(travel_obj.compensation_cost()
                                            for travel_obj in
                                            self.travel_info.all()))
        additional_expenses = 0
        if not self.withdrawn:
            additional_expenses = self.additional_expenses_initial if (
                self.status <= self.APPROVED_BY_PRESIDENT) else (
                    self.additional_expenses)

        return sum([Decimal(compensation_cost_sum), Decimal(additional_expenses),
                    Decimal(self.transportation_cost_to_be_compensated())])



    def total_cost_calculated(self):
        """
        Gets the total expenses of trip.

        This value is calculated by adding the transportation,
        compensation, partication and accommodation costs.
        """

        return sum([Decimal(self.transportation_cost_not_to_be_compensated()),
                    Decimal(self.additional_expenses_grnet),
                    Decimal(self.participation_cost),
                    Decimal(self.compensation_final()),
                    Decimal(self.overnights_not_to_be_compensated())])

    def __unicode__(self):
        return str(self.dse) + "-" + self.project.name + '-' + str(self.id)


class PetitionManager(md.Manager):

    def __init__(self, status_list, *args, **kwargs):
        self.status_list = status_list
        super(PetitionManager, self).__init__(*args, **kwargs)

    def get_queryset(self):
        """
        Filters Petition objects by the status specified by this manager.
        """
        base_queryset = super(PetitionManager, self).get_queryset()
        status_dse_map = base_queryset.filter(
            status__in=self.status_list,
            deleted=False).values('dse').annotate(Max('status'))
        q = Q()
        for status_dse in status_dse_map:
            q |= Q(status=status_dse['status__max'],
                   dse=status_dse['dse'], deleted=False)
        return base_queryset.filter(q) if status_dse_map else \
            base_queryset.filter(status__in=self.status_list, deleted=False)

class Applications(Petition):
    objects = PetitionManager([Petition.SAVED_BY_USER,
                               Petition.SUBMITTED_BY_USER,
                               Petition.SAVED_BY_SECRETARY,
                               Petition.SUBMITTED_BY_SECRETARY,
                               Petition.APPROVED_BY_PRESIDENT,
                               Petition.USER_COMPENSATION,
                               Petition.USER_COMPENSATION_SUBMISSION,
                               Petition.SECRETARY_COMPENSATION,
                               Petition.SECRETARY_COMPENSATION_SUBMISSION,
                               Petition.PETITION_FINAL_APPOVAL])

    excluded_ucompensation = ['non_grnet_quota', 'participation_cost',
                'compensation_petition_protocol', 'user_recommendation',
                'secretary_recommendation', 'compensation_petition_date',
                'compensation_decision_protocol', 'compensation_decision_date',
                'participation_payment_description', 'deleted',
                'participation_local_cost', 'compensation_alert',
                'additional_expenses_initial',
                'additional_expenses_initial_description',
                'additional_expenses', 'additional_expenses_description',
                'additional_expenses_grnet',
                'manager_cost_approval', 'manager_movement_approval',
                'compensation_alert','timesheeted',
                              'participation_local_currency',
                              'expenditure_date_protocol',
                              'expenditure_protocol','travel_report',
                              'withdrawn', 'total_cost_change_reason',
                              'is_total_manual_cost_set', 'total_cost_manual',
                              'transport_days_total']
    excluded_uc_travel_info = ['accommodation_local_cost',
                               'accommodation_cost',
                               'accommodation_total_cost',
                               'accommodation_total_local_cost',
                               'accommodation_payment_description',
                               'accommodation_local_currency',
                               'overnights_num_manual',
                               'transport_days_manual',
                               'compensation_days_manual',
                               'distance',
                               'transportation_cost',
                               'no_transportation_calculation',
                               'transportation_payment_description']

    excluded_scompensation = ['non_grnet_quota', 'participation_cost',
                'participation_payment_description', 'deleted', 'travel_files',
                'participation_local_cost', 'additional_expenses_initial',
                'additional_expenses_initial_description',
                'additional_expenses', 'additional_expenses_description',
                'additional_expenses_grnet',
                'user_recommendation', 'compensation_alert',
                'secretary_recommendation', 'manager_cost_approval',
                'manager_movement_approval','timesheeted',
                              'participation_local_currency', 'travel_report',
                              'withdrawn', 'total_cost_change_reason',
                              'is_total_manual_cost_set', 'total_cost_manual',
                              'transport_days_total']
    excluded_sc_travel_info = ['accommodation_local_cost',
                            'accommodation_cost',
                            'accommodation_total_cost',
                            'accommodation_total_local_cost',
                            'accommodation_payment_description',
                            'accommodation_local_currency',
                            'overnights_num_manual',
                            'transport_days_manual',
                            'compensation_days_manual',
                            'distance',
                            'transportation_cost',
                            'no_transportation_calculation',
                            'transportation_payment_description']

    excluded_usubmission = ['non_grnet_quota','expenditure_protocol',
                            'expenditure_date_protocol',
                            'movement_protocol',
                            'movement_date_protocol',
                            'compensation_petition_protocol',
                            'compensation_petition_date',
                            'compensation_decision_protocol',
                            'compensation_decision_date',
                            'manager_movement_approval',
                            'manager_cost_approval',
                            'timesheeted',
                            'participation_cost',
                            'participation_local_currency',
                            'participation_local_cost',
                            'participation_payment_description',
                            'additional_expenses_initial',
                            'additional_expenses_initial_description',
                            'additional_expenses',
                            'additional_expenses_grnet',
                            'additional_expenses_description',
                            'deleted',
                            'user_recommendation',
                            'secretary_recommendation',
                            'travel_report',
                            'compensation_alert',
                            'travel_files',
                            'accommodation_cost',
                            'accommodation_local_cost',
                            'accommodation_total_cost',
                            'accommodation_total_local_cost',
                            'accommodation_payment_description',
                            'transportation_cost',
                            'no_transportation_calculation',
                            'transportation_payment_description',
                            'distance',
                            'is_total_manual_cost_set',
                            'total_cost_change_reason',
                            'withdrawn',
                            'total_cost_manual',
                            'transport_days_total']
    excluded_usubmission_ti = ['accommodation_cost',
                               'accommodation_local_cost',
                               'accommodation_total_cost',
                               'accommodation_total_local_cost',
                               'accommodation_payment_description',
                               'transportation_cost',
                               'no_transportation_calculation',
                               'transportation_payment_description',
                               'distance', 'overnights_num_manual',
                               'transport_days_manual',
                               'accommodation_local_currency',
                               'compensation_days_manual',
                               'depart_date',
                               'return_date']

    excluded_sec_submission =['non_grnet_quota',
                              'compensation_petition_protocol',
                              'compensation_petition_date',
                              'compensation_decision_protocol',
                              'compensation_decision_date',
                              'manager_cost_approval',
                              'timesheeted',
                              'participation_cost',
                              'participation_local_cost',
                              'participation_payment_description',
                              'additional_expenses_initial',
                              'additional_expenses_initial_description',
                              'additional_expenses',
                              'additional_expenses_grnet',
                              'additional_expenses_description',
                              'deleted',
                              'user_recommendation',
                              'secretary_recommendation',
                              'travel_report',
                              'compensation_alert',
                              'travel_files',
                              'manager_movement_approval',
                              'participation_local_currency',
                              'is_total_manual_cost_set',
                              'total_cost_change_reason',
                              'withdrawn',
                              'total_cost_manual',
                              'transport_days_total']

    excluded_sec_submission_ti =['accommodation_local_cost','distance',
                                 'accommodation_cost',
                                 'accommodation_total_cost',
                                 'accommodation_total_local_cost',
                                 'manager_movement_approval',
                                 'transportation_cost',
                                 'no_transportation_calculation',
                                 'accommodation_payment_description',
                                 'transportation_payment_description',
                                 'accommodation_local_currency',
                                 'overnights_num_manual',
                                 'transport_days_manual',
                                 'compensation_days_manual',
                                 ]


    excluded_per_status = {
        Petition.SAVED_BY_USER:excluded_usubmission,
        Petition.APPROVED_BY_PRESIDENT:excluded_ucompensation,
        Petition.SAVED_BY_SECRETARY:excluded_sec_submission,
        Petition.USER_COMPENSATION:excluded_ucompensation,
        Petition.USER_COMPENSATION_SUBMISSION:excluded_ucompensation,
        Petition.SECRETARY_COMPENSATION:excluded_scompensation,
        Petition.SECRETARY_COMPENSATION_SUBMISSION:excluded_scompensation,
        Petition.PETITION_FINAL_APPOVAL:excluded_scompensation
    }
    excluded_ti_per_status = {
        Petition.SAVED_BY_USER:excluded_usubmission_ti,
        Petition.SAVED_BY_SECRETARY:excluded_sec_submission_ti,
        Petition.APPROVED_BY_PRESIDENT:excluded_uc_travel_info,
        Petition.USER_COMPENSATION:excluded_uc_travel_info,
        Petition.USER_COMPENSATION_SUBMISSION:excluded_uc_travel_info,
        Petition.SECRETARY_COMPENSATION:excluded_sc_travel_info,
        Petition.SECRETARY_COMPENSATION_SUBMISSION:excluded_sc_travel_info,
        Petition.PETITION_FINAL_APPOVAL:excluded_sc_travel_info
    }

    class Meta:
        proxy = True

    def clean(self):
        """
        Overrides `clean` method and checks if specified dates are valid.
        """
        super(Applications, self).clean()
        if self.task_start_date and self.task_end_date:
            start_end_date_validator(
                ((self.task_start_date, self.task_end_date),),
                (('task start', 'task end'),))

    def save(self, **kwargs):
        # Remove temporary saved petition with the corresponding dse.
        if self.status in (Petition.SUBMITTED_BY_USER,
                           Petition.SUBMITTED_BY_SECRETARY):
            try:
                Applications.objects.get(status=self.status-1,
                                         dse=self.dse).mark_as_deleted()
            except ObjectDoesNotExist:
                pass

        super(Applications, self).save(**kwargs)

    def status_rollback(self):
        """
        Changes status of the petition to the previous one by marking current
        as deleted and creating new one to the corresponding status.
        """
        if self.status in (Petition.SECRETARY_COMPENSATION_SUBMISSION,
                           Petition.PETITION_FINAL_APPOVAL):
            return self.status_transition(self.status - 1)
        super(Applications, self).status_rollback()
