from datetime import timedelta
import functools
from django.conf import settings
from django.core.exceptions import (
    ValidationError, ObjectDoesNotExist, PermissionDenied)
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Max
from django.db.models import Q
from model_utils import FieldTracker
from rest_framework import serializers
from texpenses.models import common
from texpenses.validators import (
    afm_validator, required_validator, iban_validation, date_validator,
    start_end_date_validator)


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


class TaxOffice(models.Model):

    """ Model which contains all tax offices of Greece. """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, blank=False, unique=True)
    description = models.CharField(max_length=300, blank=True)
    address = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)

    class Api(object):
        fields = ('id', 'url', 'name', 'description', 'address',
                  'email', 'phone')
        read_only_fields = ('id', 'url')
        allowable_operations = ('list', 'retrieve')
        caching = True
        resource_name = 'resources/tax-office'

    def __unicode__(self):
        return self.name


class TravelUserProfile(models.Model):

    """
    An abstract model class which include all fields which describe the user
    of `Travel Expenses Application`.

    These fields actually are associated with personal info such as IBAN
    number, Tax Office, etc. as well as, with the kind and specialty of user at
    GRNET.
    """
    iban = models.CharField(max_length=27, blank=False, null=True,
                            validators=[iban_validation])
    specialty = models.CharField(
        max_length=5, choices=common.SPECIALTY, blank=False, null=True)
    tax_reg_num = models.CharField(max_length=9, blank=False, null=True,
                                   unique=True, validators=[afm_validator])
    tax_office = models.ForeignKey(TaxOffice, blank=False, null=True)
    kind = models.CharField(max_length=5, choices=common.KIND, blank=False,
                            null=True)
    user_category = models.CharField(
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

    trip_days_left = models.IntegerField(
        blank=False, default=settings.MAX_HOLIDAY_DAYS,
        validators=[MaxValueValidator(settings.MAX_HOLIDAY_DAYS),
                    MinValueValidator(0)])

    class Api(object):
        fields = ('username', 'first_name', 'last_name', 'email',
                  'iban', 'specialty', 'kind', 'tax_reg_num', 'tax_office',
                  'user_category', 'user_group', 'trip_days_left')
        read_only_fields = ('username', 'trip_days_left', 'user_category')
        allowable_operations = ('list', 'retrieve')
        caching = True

    def user_group(self):
        groups = self.groups.all()
        # TODO fix this hack.
        if not groups:
            return "Unknown"
        return groups[0].name


class Project(models.Model):

    """
    Model which describes a project which GRNET has assumed.

    A project is described by its name, accounting code and the GRNET member
    who managed it.
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=500, blank=False, unique=True)
    accounting_code = models.CharField(max_length=20, blank=False)
    manager_name = models.CharField(max_length=40, blank=False)
    manager_surname = models.CharField(max_length=40, blank=False)
    manager_email = models.EmailField(max_length=256, blank=False, null=True)

    class Api(object):
        fields = ('id', 'url', 'name', 'accounting_code',
                  'manager_name', 'manager_surname', 'manager_email')
        read_only_fields = ('id', 'url')
        allowable_operations = ('list', 'retrieve')
        caching = True
        resource_name = 'resources/project'

    def __unicode__(self):
        return self.name


class Country(models.Model):

    """
    Model for countries.

    A country is descibed by its category which define the amount of
    compensation combined with the user category.
    """
    CATEGORIES = (
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C')
    )

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20, blank=False, unique=True)
    category = models.CharField(choices=CATEGORIES, max_length=1, default='A')
    currency = models.CharField(
        max_length=3, choices=common.CURRENCIES, blank=False,
        default=settings.DEFAULT_CURRENCY)

    class Api(object):
        fields = ('id', 'url', 'name', 'category', 'currency')
        read_only_fields = ('id', 'url', 'category', 'currency')
        allowable_operations = ('list', 'retrieve')
        caching = True

    def __unicode__(self):
        """TODO: to be defined1. """
        return self.name


class City(models.Model):

    """Model for cities. """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=False)
    country = models.ForeignKey(Country, blank=False)

    class Api(object):
        fields = ('id', 'url', 'name', 'country')
        read_only_fields = ('id', 'url', 'country')
        nested_relations = [('country', 'country')]
        allowable_operations = ('list', 'retrieve')
        caching = True
        viewset_code = 'texpenses.views'
        viewset_module_name = 'city'
        resource_name = 'resources/city'

    def __unicode__(self):
        """TODO: to be defined. """
        return self.name


class Accommodation(models.Model):

    """
    An abstract model that represents the accommodation related info
    """

    accommodation_cost = models.FloatField(
        blank=False, default=0.0, validators=[MinValueValidator(0.0)])
    accommodation_default_currency = models.CharField(
        max_length=3, blank=False, default=settings.DEFAULT_CURRENCY)
    accommodation_local_cost = models.FloatField(
        blank=False, default=0.0, validators=[MinValueValidator(0.0)])
    accommodation_local_currency = models.CharField(
        max_length=3, blank=True, choices=common.CURRENCIES)
    accommodation_payment_way = models.CharField(
        max_length=5, choices=common.WAYS_OF_PAYMENT, blank=False,
        default='NON')
    accommodation_payment_description = models.CharField(
        max_length=200, null=True)

    class Meta:
        abstract = True


class Transportation(models.Model):

    """
    An abstract model that represents the transportation related info
    """
    transportation_cost = models.FloatField(
        blank=False, default=0.0, validators=[MinValueValidator(0.0)])
    transportation_default_currency = models.CharField(
        max_length=3, blank=False, default=settings.DEFAULT_CURRENCY)
    transportation_payment_way = models.CharField(
        max_length=5, choices=common.WAYS_OF_PAYMENT,
        blank=False, default='NON')
    transportation_payment_description = models.CharField(
        max_length=200, null=True)

    class Meta:
        abstract = True


class TravelInfo(Accommodation, Transportation):

    """
    An abstract model class that represents travel information.

    Travel information are associated with the duration, departure and arrival
    point, transportation, accommodation, etc.
    """
    depart_date = models.DateTimeField(null=True, validators=[date_validator])
    return_date = models.DateTimeField(null=True, validators=[date_validator])
    departure_point = models.ForeignKey(
        City, blank=True, null=True, related_name='travel_departure_point')
    arrival_point = models.ForeignKey(City, blank=True, null=True,
                                      related_name='travel_arrival_point')
    means_of_transport = models.CharField(
        choices=common.TRANSPORTATION, max_length=10, blank=False,
        default='AIR')
    transport_days_manual = models.PositiveSmallIntegerField(
        blank=False, default=0)
    overnights_num_manual = models.PositiveSmallIntegerField(
        blank=False, default=0)
    compensation_days_manual = models.PositiveSmallIntegerField(
        blank=False, default=0)
    meals = models.CharField(max_length=10, choices=common.MEALS,
                             blank=False, default='NON')
    travel_petition = models.ForeignKey('Petition')

    tracked_fields = ['depart_date', 'return_date']
    tracker = FieldTracker(fields=tracked_fields)

    class Api:
        expose = False
        fields = ('id', 'arrival_point', 'departure_point',
                  'means_of_transport',
                  'accommodation_cost', 'accommodation_default_currency',
                  'accommodation_local_cost', 'accommodation_local_currency',
                  'accommodation_payment_way',
                  'accommodation_payment_description',
                  'return_date', 'depart_date',
                  'transportation_cost', 'transportation_default_currency',
                  'transportation_payment_way',
                  'transportation_payment_description',
                  'transport_days_proposed',
                  'overnight_cost',
                  'compensation_level',
                  'same_day_return_task', 'compensation_cost',
                  'compensation_days_proposed',
                  'overnights_num_manual', 'transport_days_manual',
                  'compensation_days_manual', 'meals')
        read_only_fields = ('id', 'transportation_default_currency',
                            'accommodation_default_currency')
        allowable_operations = ('list', 'retrieve', 'delete')

    def clean(self):
        if self.depart_date and self.return_date \
                and self.travel_petition.task_end_date:
            dates = ((self.depart_date, self.return_date),
                     (self.depart_date, self.travel_petition.task_end_date))
            labels = (('depart', 'return'), ('depart', 'task end'))
            start_end_date_validator(dates, labels)
        self.validate_overnight_cost()
        super(TravelInfo, self).clean()

    def save(self, *args, **kwargs):
        changed = any(self.tracker.has_changed(field)
                      for field in self.tracked_fields)
        petition_dates_changed = any(
            self.travel_petition.tracker.has_changed(field)
            for field in self.travel_petition.tracked_fields)
        if changed or petition_dates_changed:
            overnight_days = self.overnights_num_proposed(
                self.travel_petition.task_start_date,
                self.travel_petition.task_end_date)
            self.transport_days_manual = self.transport_days_proposed()
            self.overnights_num_manual = overnight_days
            self.compensation_days_manual = overnight_days

        super(TravelInfo, self).save(*args, **kwargs)

    def validate_overnight_cost(self):
        """
        Checks that the accommodation_cost does not surpass the maximum
        overnight limit based on the category of user.

        :raises: ValidationError if accommodation cost exceeds the allowable
        limit.
        """
        EXTRA_COST = 100
        max_overnight_cost = common.MAX_OVERNIGHT_COST[
            self.travel_petition.user_category]
        max_overnight_cost += EXTRA_COST if self.is_city_ny() else 0
        if self.accommodation_cost > max_overnight_cost:
            raise ValidationError('Accomondation cost %.2f for petition with'
                                  ' DSE %s exceeds the max overnight cost.' % (
                                      self.accommodation_cost,
                                      str(self.travel_petition.dse)))

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
        time_period = (self.depart_date + timedelta(x + 1)
                       for x in xrange((
                           self.return_date - self.depart_date).days))
        return sum(1 for day in time_period if day.weekday() not in WEEKENDS)

    def overnights_num_proposed(self, task_start_date, task_end_date):
        """
        Method which calculates the proposed number of days that traveller
        should overnight.

        The number of days is calculated by return and departure dates.
        There are two possible scenarios:
            1) One more day is added to the total overnight days if the
               departure date is one day before from the date when task starts.
            2) One more day is added to the total overnight days if the
               return date is one day after from the date when task ends.

        :param task_start_date: Date when task starts.
        :param task_end_date: Date when task ends.
        :returns: The proposed overinight days.
        """
        if not (self.return_date and self.depart_date and task_start_date
                and task_end_date):
            return 0
        first_day = task_start_date - timedelta(days=1)\
            if (task_start_date - self.depart_date).days >= 1\
            else self.depart_date
        last_day = task_end_date + timedelta(days=1) if (
            self.return_date - task_end_date).days >= 1 else self.return_date
        return (last_day.date() - first_day.date()).days

    def overnight_cost(self):
        """ Returns total overnight cost. """
        return self.accommodation_cost * self.overnights_num_manual

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

    def same_day_return_task(self):
        """
        This method checks that the t
        """
        task_start_date = self.travel_petition.task_start_date
        task_end_date = self.travel_petition.task_end_date
        if task_end_date is None or \
                self.return_date is None\
                or task_start_date is None\
                or self.depart_date is None:
            return False
        return task_end_date.date() == self.return_date.date()\
            == task_start_date.date() == self.depart_date.date()

    def compensation_days_proposed(self):
        return self.overnights_num_proposed(self.travel_petition.
                                            task_start_date,
                                            self.travel_petition.task_end_date)

    def compensation_cost(self):
        """Calculates the compensation based on compensation days,
        compensation level and additional expenses
        :returns: The maximum possible compensation

        """
        percentage = 100
        max_compensation = self.compensation_days_manual * \
            self.compensation_level()
        if self.same_day_return_task():
            max_compensation *= 0.5
        compensation_proportion = common.COMPENSATION_PROPORTION[self.meals]\
            if self.meals else 1
        return max_compensation * compensation_proportion * (
            self.travel_petition.grnet_quota() / percentage)


class TravelInfoUserSubmission(TravelInfo):

    class Meta:
        proxy = True

    class Api:
        expose = False
        fields = TravelInfo.Api.fields
        read_only_fields = TravelInfo.Api.read_only_fields
        allowable_operations = TravelInfo.Api.allowable_operations
        extra_kwargs = {
            'arrival_point': {
                'required': True, 'allow_null': False
            },
            'departure_point': {
                'required': True, 'allow_null': False
            }

        }


class TravelInfoCompensation(TravelInfo):

    class Meta:
        proxy = True

    class Api:
        expose = False
        fields = TravelInfo.Api.fields
        read_only_fields = (
            'id', 'arrival_point', 'departure_point',
            'means_of_transport',
            'accommodation_default_currency',
            'accommodation_local_cost', 'accommodation_local_currency',
            'accommodation_payment_way',
            'accommodation_payment_description',
            'return_date', 'depart_date',
            'transportation_default_currency',
            'transportation_payment_way',
            'transportation_payment_description',
            'transport_days_proposed',
            'overnight_cost',
            'compensation_level',
            'same_day_return_task', 'compensation_cost',
            'compensation_days_proposed',
            'transport_days_manual')


class TravelInfoSecretarySubmission(TravelInfo):

    class Meta:
        proxy = True

    class Api:
        expose = False
        fields = TravelInfo.Api.fields
        read_only_fields = TravelInfo.Api.read_only_fields
        allowable_operations = TravelInfo.Api.allowable_operations
        extra_kwargs = {
            'arrival_point': {
                'required': True, 'allow_null': False
            },
            'departure_point': {
                'required': True, 'allow_null': False
            },
            'means_of_transport': {
                'required': True, 'allow_blank': False, 'allow_null': False
            },
            'accommodation_cost': {
                'required': True, 'allow_null': False
            },
            'accommodation_default_currency': {
                'required': True, 'allow_blank': False, 'allow_null': False
            },
            'accommodation_payment_way': {
                'required': True, 'allow_blank': False, 'allow_null': False
            },
            'accommodation_payment_description': {
                'required': True, 'allow_blank': False, 'allow_null': False
            },
            'return_date': {
                'required': True, 'allow_null': False
            },
            'depart_date': {
                'required': True, 'allow_null': False
            },
            'transportation_cost': {
                'required': True, 'allow_null': False
            },
            'transportation_default_currency': {
                'required': True, 'allow_blank': False, 'allow_null': False
            },
            'transportation_payment_way': {
                'required': True, 'allow_blank': False, 'allow_null': False
            },
            'transportation_payment_description': {
                'required': True, 'allow_blank': False, 'allow_null': False
            },

        }


class SecretarialInfo(models.Model):

    """
    Abstract model which includes information that secretary fills.
    """
    non_grnet_quota = models.FloatField(
        blank=False, default=0.0, validators=[MinValueValidator(0.0)])

    movement_id = models.CharField(max_length=200, null=True, blank=True)
    expenditure_protocol = models.CharField(
        max_length=30, null=True, blank=True)
    expenditure_date_protocol = models.DateField(
        blank=True, null=True, validators=[date_validator])
    movement_protocol = models.CharField(
        max_length=30, null=True, blank=True)
    movement_date_protocol = models.DateField(
        blank=True, null=True, validators=[date_validator])
    compensation_petition_protocol = models.CharField(
        max_length=30, null=True, blank=True)
    compensation_petition_date = models.DateField(
        blank=True, null=True, validators=[date_validator])
    compensation_decision_protocol = models.CharField(
        max_length=30, null=True, blank=True)
    compensation_decision_date = models.DateField(
        blank=True, null=True, validators=[date_validator])
    manager_travel_approval = models.CharField(max_length=200, null=True,
                                               blank=True)

    manager_final_approval = models.CharField(max_length=200, null=True,
                                              blank=True)
    MAX_GRNET_QUOTA = 100

    def grnet_quota(self):
        if self.non_grnet_quota is None:
            return self.MAX_GRNET_QUOTA
        return self.MAX_GRNET_QUOTA - self.non_grnet_quota

    class Meta:
        abstract = True


class ParticipationInfo(models.Model):

    """
    An abstract model that represents the participation cost related info
    """
    participation_cost = models.FloatField(
        blank=False, default=0.0, validators=[MinValueValidator(0.0)])

    participation_default_currency = models.CharField(
        max_length=3, blank=False, default=settings.DEFAULT_CURRENCY)
    participation_local_cost = models.FloatField(
        blank=True, default=0.0, validators=[MinValueValidator(0.0)])
    participation_local_currency = models.CharField(
        max_length=3, blank=True, choices=common.CURRENCIES)
    participation_payment_way = models.CharField(
        max_length=10, choices=common.WAYS_OF_PAYMENT, blank=False,
        default='NON')
    participation_payment_description = models.CharField(
        max_length=200, blank=True, null=True)

    class Meta:
        abstract = True


class AdditionalCosts(models.Model):

    """
    An abstract model that represents the additional costs related info
    """
    additional_expenses_initial = models.FloatField(
        blank=False, default=0.0, validators=[MinValueValidator(0.0)])
    additional_expenses_default_currency = models.CharField(
        max_length=3, blank=False, default=settings.DEFAULT_CURRENCY)
    additional_expenses_initial_description = models.CharField(
        max_length=400, blank=True, null=True)

    additional_expenses = models.FloatField(
        blank=False, default=0.0, validators=[MinValueValidator(0.0)])
    additional_expenses_local_currency = models.CharField(
        max_length=3, blank=False, default=settings.DEFAULT_CURRENCY)
    additional_expenses_description = models.CharField(
        max_length=400, blank=True, null=True)

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

    id = models.AutoField(primary_key=True)

    # travel user profile fields
    iban = models.CharField(max_length=27, blank=False,
                            validators=[iban_validation])
    specialty = models.CharField(
        max_length=5, choices=common.SPECIALTY, blank=False)
    tax_reg_num = models.CharField(max_length=9, blank=False,
                                   validators=[afm_validator])
    tax_office = models.ForeignKey(TaxOffice, blank=False)
    kind = models.CharField(max_length=5, choices=common.KIND, blank=False)
    user_category = models.CharField(
        max_length=1, choices=common.USER_CATEGORIES,
        blank=False, default='B')
    #

    dse = models.IntegerField(blank=False, validators=[MinValueValidator(1)])
    travel_info = models.ManyToManyField(TravelInfo, blank=True)

    user = models.ForeignKey(UserProfile, blank=False)
    task_start_date = models.DateTimeField(
        blank=True, null=True, validators=[date_validator])
    task_end_date = models.DateTimeField(
        blank=True, null=True, validators=[date_validator])
    created = models.DateTimeField(blank=False, default=timezone.now())
    updated = models.DateTimeField(blank=False, default=timezone.now())
    deleted = models.BooleanField(default=False)
    project = models.ForeignKey(Project, blank=False)
    reason = models.CharField(max_length=500, blank=True, null=True)
    user_recommendation = models.CharField(
        max_length=500, blank=True, null=True)
    secretary_recommendation = models.CharField(
        max_length=500, blank=True, null=True)

    status = models.IntegerField(blank=False)

    first_name = models.CharField(max_length=200, blank=False, null=True)
    last_name = models.CharField(max_length=200, blank=False, null=True)

    travel_report = models.CharField(max_length=1000, blank=True, null=True)

    travel_files = models.FileField(upload_to=common.user_directory_path,
                                    null=True, blank=True)

    tracked_fields = ['task_start_date', 'task_end_date']
    tracker = FieldTracker()

    class Api:
        expose = False
        fields = ('id', 'dse', 'first_name', 'last_name', 'kind',
                  'specialty', 'tax_office', 'tax_reg_num', 'user_category',
                  'user', 'iban',
                  'task_start_date', 'task_end_date', 'created', 'updated',
                  'travel_info', 'project', 'reason',
                  'secretary_recommendation', 'user_recommendation',
                  'trip_days_before', 'trip_days_after', 'status',
                  'participation_cost', 'participation_default_currency',
                  'participation_local_cost', 'participation_local_currency',
                  'participation_payment_way',
                  'participation_payment_description', 'url',
                  'additional_expenses_initial',
                  'additional_expenses_initial_description',
                  'additional_expenses_default_currency',
                  'overnights_sum_cost',
                  'overnights_proposed', 'transport_days', 'trip_days_before',
                  'trip_days_after', 'overnights_num', 'overnights_proposed',
                  'overnights_sum_cost', 'task_duration', 'compensation_final',
                  'total_cost')
        read_only_fields = ('id', 'url', 'first_name', 'last_name',
                            'kind', 'specialty', 'tax_office', 'tax_reg_num',
                            'user_category', 'iban', 'status', 'created',
                            'updated', 'participation_default_currency')
        filter_fields = ('first_name', 'last_name', 'project',
                         'task_start_date', 'task_end_date', 'created',
                         'updated', 'project', 'travel_info__depart_date',
                         'travel_info__return_date')

        search_fields = ('first_name', 'last_name', 'project',
                         'task_start_date', 'task_end_date', 'created',
                         'updated')
        nested_relations = [('travel_info', 'travel_info')]

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

    def save(self, *args, **kwargs):
        self.updated = timezone.now()
        super(Petition, self).save(*args, **kwargs)

    def delete(self):
        """
        Overrides the `delete` method of model.

        It doesn't actually delete the object, but it sets its status as
        `DELETED`.
        """
        self.deleted = True
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
        self.user.trip_days_left -= self.transport_days()
        self.user.save()

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
            self.delete()
        petition_modifications = kwargs.pop('petition_data', {})
        travel_info_modifications = kwargs.pop(
            'travel_info_data', [{}] * len(travel_info))
        self.id = None
        self.status = new_status
        self.deleted = False
        update_instance(self, petition_modifications)
        self.save()
        for i, travel_obj in enumerate(travel_info):
            travel_obj.id = None
            update_instance(travel_obj, travel_info_modifications[i])
            travel_obj.travel_petition = self
            travel_obj.save()
        self.travel_info.add(*travel_info)
        return self.id

    def _construct_validation_message(self, fields):
        response = {}
        message = ['This field is required']

        for field in fields:
            response[field] = message
        return response

    def proceed(self, **kwargs):
        """
        Proceed petition to the next status.


        If next status is one of the submission statuses, then a checker
        is triggered and tests if the petition is completed.
        """
        next_status = self.status + 1
        submit = next_status in Petition.SUBMISSION_STATUSES or\
            kwargs.pop('delete', False)
        missing_fields = self.get_missing_fields()
        if next_status in Petition.SUBMISSION_STATUSES \
                and missing_fields:
            raise serializers.ValidationError(
                self._construct_validation_message(missing_fields))
        return self.status_transition(self.status + 1, delete=submit, **kwargs)

    def get_missing_fields(self):
        """

        Check if all fields of petition along with the fields of many to many
        related objects have been initialized.
        """
        missing_fields = []
        petition_missing_fields = get_model_missing_fields(
            self, excluded=getattr(self, 'excluded', []))
        missing_fields.extend(petition_missing_fields)

        travel_info = self.travel_info.all()

        if travel_info:
            for travel_obj in travel_info:
                travel_info_missing_fields = []
                travel_info_missing_fields.extend(get_model_missing_fields(
                    travel_obj,
                    excluded=getattr(self, 'excluded_travel_info', [])))
                missing_fields.extend(travel_info_missing_fields)

        return missing_fields

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

    def transport_days(self):
        """ Gets the total number of transport days for all destinations. """
        return sum(travel.transport_days_manual
                   for travel in self.travel_info.all())

    def trip_days_before(self):
        """ Gets the number of trip days of user before petition. """
        return self.user.trip_days_left

    def trip_days_after(self):
        """ Gets the number of trip days of user after petition. """
        return self.user.trip_days_left - self.transport_days()

    def overnights_num(self):
        """ Gets the number of total overnight days for all destinations. """
        return sum(travel.overnights_num_manual
                   for travel in self.travel_info.all())

    def overnights_proposed(self):
        return sum(travel.overnights_num_proposed(
            self.task_start_date, self.task_end_date)
            for travel in self.travel_info.all())

    def overnights_sum_cost(self):
        """ Total accommodation for all destinations. """
        return sum(travel.overnight_cost()
                   for travel in self.travel_info.all())

    def task_duration(self):
        """ Gets the duration of task. """
        if not (self.task_start_date and self.task_end_date):
            return 0
        return (self.task_end_date - self.task_start_date).days

    def compensation_final(self):
        """TODO: Docstring for compensation_final.
        :returns: TODO

        """
        return sum(travel_obj.compensation_cost()
                   for travel_obj in self.travel_info.all()) + \
            (self.additional_expenses or self.additional_expenses_initial)

    def total_cost(self):
        """
        Gets the total expenses of trip.

        This value is calculated by adding the transportation,
        compensation, partication and accommodation costs.
        """
        transportation_cost = sum(travel.transportation_cost
                                  for travel in self.travel_info.all())
        return sum([transportation_cost, self.participation_cost,
                    self.compensation_final(), self.overnights_sum_cost()])

    def __unicode__(self):
        return str(self.id) + "-" + self.project.name


class PetitionManager(models.Manager):

    def __init__(self, status_list, *args, **kwargs):
        self.status_list = status_list
        super(PetitionManager, self).__init__(*args, **kwargs)

    def get_queryset(self):
        """
        Filters Petition objects by the status specified by this manager.
        """
        base_queryset = super(PetitionManager, self).get_queryset()
        status_dse_map = base_queryset.filter(
            status__in=self.status_list, deleted=False).values('dse').\
            annotate(Max('status'))
        q = Q()
        for status_dse in status_dse_map:
            q |= Q(status=status_dse['status__max'],
                   dse=status_dse['dse'], deleted=False)
        return base_queryset.filter(q) if status_dse_map else \
            base_queryset.filter(status__in=self.status_list, deleted=False)


class UserPetition(Petition):

    """ A proxy model for the temporary saved petition by user. """
    objects = PetitionManager([Petition.SAVED_BY_USER])

    class Meta:
        proxy = True

    class Api:
        fields = Petition.Api.fields
        read_only_fields = Petition.Api.read_only_fields + (
            'dse', 'user')
        filter_fields = Petition.Api.filter_fields
        nested_relations = [('travel_info', 'travel_info')]
        extra_kwargs = {
            'dse': {'required': False, 'allow_null': True},
            'status': {'default': Petition.SAVED_BY_USER},
            'task_start_date': {'required': False},
            'task_end_date': {'required': False},
            'travel_info': {'required': False},
            'user': {'default': serializers.CurrentUserDefault(),
                     'validators': [functools.partial(
                         required_validator, fields=Petition.USER_FIELDS)]}
        }
        serializer_code = 'texpenses.serializers'
        serializer_module_name = 'petition'
        viewset_code = 'texpenses.views'
        resource_name = 'petition/user/saved'


class UserPetitionSubmission(Petition):

    """ A proxy model for the temporary submitted petitions by user. """
    objects = PetitionManager([Petition.SUBMITTED_BY_USER])

    class Meta:
        proxy = True

    class Api:
        fields = Petition.Api.fields
        filter_fields = Petition.Api.filter_fields
        read_only_fields = Petition.Api.read_only_fields + ('user',)
        nested_relations = [
            ('travel_info', 'travel_info', TravelInfoUserSubmission)]
        extra_kwargs = {
            'reason': {
                'required': True, 'allow_blank': False, 'allow_null': False
            },
            'dse': {
                'required': False, 'allow_null': True
            },
            'status': {
                'default': Petition.SUBMITTED_BY_USER
            },
            'task_start_date': {
                'required': True, 'allow_null': False
            },
            'task_end_date': {
                'required': True, 'allow_null': False
            },
            'user': {
                'default': serializers.CurrentUserDefault(),
                'validators': [functools.partial(
                    required_validator, fields=Petition.USER_FIELDS)]
            }
        }
        serializer_code = 'texpenses.serializers'
        serializer_module_name = 'petition'
        viewset_code = 'texpenses.views'
        resource_name = 'petition/user/submitted'

    def save(self, **kwargs):
        # Remove temporary saved petition with the corresponding dse.
        try:
            UserPetition.objects.select_for_update(nowait=True).\
                get(dse=self.dse).delete()
        except ObjectDoesNotExist:
            pass
        super(UserPetitionSubmission, self).save(**kwargs)

    def status_rollback(self):
        """
        Changes status of the petition to the previous one by marking current
        as deleted and creating new one to the corresponding status.
        """
        return self.status_transition(self.SAVED_BY_USER)


class SecretaryPetition(Petition):

    """ A proxy model for the temporary saved petitions by secretary. """
    objects = PetitionManager([Petition.SUBMITTED_BY_USER,
                               Petition.SAVED_BY_SECRETARY])

    class Meta:
        proxy = True

    class Api:
        fields = Petition.Api.fields + (
            'non_grnet_quota', 'grnet_quota', 'user',
            'expenditure_protocol',
            'expenditure_date_protocol', 'movement_protocol',
            'movement_date_protocol',  'movement_id',
            'manager_travel_approval', 'manager_final_approval')
        read_only_fields = Petition.Api.read_only_fields
        filter_fields = Petition.Api.filter_fields
        nested_relations = [('travel_info', 'travel_info')]
        extra_kwargs = {
            'dse': {'required': False, 'allow_null': True},
            'task_start_date': {'required': False},
            'task_end_date': {'required': False},
            'travel_info': {'required': False},
            'status': {'default': Petition.SAVED_BY_SECRETARY},
            'user': {
                'validators': [functools.partial(
                    required_validator, fields=Petition.USER_FIELDS)]
            },
        }
        serializer_code = 'texpenses.serializers'
        serializer_module_name = 'petition'
        viewset_code = 'texpenses.views'
        resource_name = 'petition/secretary/saved'


class SecretaryPetitionSubmission(Petition):

    """ A proxy model for the temporary submitted petitions by secretary. """
    objects = PetitionManager([Petition.SUBMITTED_BY_SECRETARY,
                               Petition.APPROVED_BY_PRESIDENT])

    class Meta:
        proxy = True

    class Api:
        fields = Petition.Api.fields + (
            'non_grnet_quota', 'grnet_quota', 'user', 'movement_id',
            'expenditure_protocol',
            'expenditure_date_protocol',
            'movement_protocol', 'movement_date_protocol',
            'manager_travel_approval',
            'manager_final_approval')
        filter_fields = Petition.Api.filter_fields
        read_only_fields = Petition.Api.read_only_fields
        nested_relations = [
            ('travel_info', 'travel_info', TravelInfoSecretarySubmission)]
        extra_kwargs = {
            'movement_id': {
                'required': True, 'allow_blank': False, 'allow_null': False
            },
            'expenditure_protocol': {
                'required': True, 'allow_blank': False, 'allow_null': False
            },
            'expenditure_date_protocol': {
                'required': True, 'allow_null': False
            },
            'movement_protocol': {
                'required': True, 'allow_blank': False, 'allow_null': False
            },
            "movement_date_protocol": {
                'required': True, 'allow_null': False
            },

            'additional_expenses_initial': {
                'required': True, 'allow_null': False
            },
            'additional_expenses_default_currency': {
                'required': True, 'allow_blank': False, 'allow_null': False,
            },

            'additional_expenses_initial': {
                'required': True, 'allow_null': False
            },
            'additional_expenses_default_currency': {
                'required': True, 'allow_null': False, 'allow_blank': False
            },

            'dse': {
                'required': False, 'allow_null': True
            },
            'status': {
                'default': Petition.SUBMITTED_BY_SECRETARY
            },
            'user': {
                'validators': [functools.partial(
                    required_validator, fields=Petition.USER_FIELDS)]
            },
        }
        serializer_code = 'texpenses.serializers'
        serializer_module_name = 'petition'
        viewset_code = 'texpenses.views'
        resource_name = 'petition/secretary/submitted'

    def save(self, **kwargs):
        # Remove temporary saved petition with the corresponding dse.
        try:
            SecretaryPetition.objects.select_for_update(nowait=True).\
                get(dse=self.dse).delete()
        except ObjectDoesNotExist:
            pass
        super(SecretaryPetitionSubmission, self).save(**kwargs)

    def status_rollback(self):
        """
        Changes status of the petition to the previous one by marking current
        as deleted and creating new one to the corresponding status.
        """
        return self.status_transition(self.SAVED_BY_SECRETARY)


class UserCompensation(Petition):

    """ A proxy model for the user petitions to be compensated. """
    objects = PetitionManager([
        Petition.APPROVED_BY_PRESIDENT, Petition.USER_COMPENSATION,
        Petition.USER_COMPENSATION_SUBMISSION])
    excluded = ['non_grnet_quota', 'participation_cost',
                'compensation_petition_protocol', 'user_recommendation',
                'secretary_recommendation', 'compensation_petition_date',
                'compensation_decision_protocol', 'compensation_decision_date',
                'participation_payment_description', 'deleted', 'travel_files',
                'participation_local_cost', 'additional_expenses_initial',
                'additional_expenses_initial_description',
                'additional_expenses', 'additional_expenses_description']
    excluded_travel_info = ['accommodation_local_cost', ]

    class Meta:
        proxy = True

    class Api:
        fields = Petition.Api.\
            fields + ('additional_expenses_initial',
                      'additional_expenses_default_currency',
                      'additional_expenses_initial_description',
                      'additional_expenses',
                      'additional_expenses_local_currency',
                      'additional_expenses_description',
                      'travel_report', 'travel_files',
                      'non_grnet_quota',
                      'movement_protocol', 'movement_date_protocol',
                      'expenditure_protocol', 'expenditure_date_protocol',
                      'movement_id', 'manager_final_approval',
                      'manager_travel_approval',
                      )
        filter_fields = Petition.Api.filter_fields
        search_fields = Petition.Api.search_fields
        read_only_fields = Petition.Api.read_only_fields +\
            ('user', 'task_start_date',
             'task_end_date', 'travel_info', 'reason',
             'secretary_recommendation', 'user_recommendation',
             'status', 'dse', 'project', 'additional_expenses_initial',
             'additional_expenses_default_currency',
             'additional_expenses_initial_description',
             'participation_cost', 'participation_default_currency',
             'participation_local_cost',
             'participation_local_currency',
             'participation_payment_way',
             'non_grnet_quota',
             'participation_payment_description', 'url',
             'movement_protocol', 'movement_date_protocol',
             'expenditure_protocol', 'expenditure_date_protocol',
             'movement_id', 'manager_final_approval',
             'manager_travel_approval',
             )

        nested_relations = [
            ('travel_info', 'travel_info', TravelInfoUserSubmission)]
        extra_kwargs = {
            'status': {'default': Petition.USER_COMPENSATION},

            'user': {
                'default': serializers.CurrentUserDefault(),
                'validators': [functools.partial(
                    required_validator, fields=Petition.USER_FIELDS)]
            },
            'travel_info': {
                'read_only': True
            },
        }
        serializer_code = 'texpenses.serializers'
        serializer_module_name = 'petition'
        viewset_code = 'texpenses.views'
        viewset_module_name = 'user_compensation'
        resource_name = 'petition/user/compensations'


class SecretaryCompensation(Petition):

    """ A proxy model for the secretary petitions to be compensated. """
    objects = PetitionManager([
        Petition.USER_COMPENSATION_SUBMISSION,
        Petition.SECRETARY_COMPENSATION,
        Petition.SECRETARY_COMPENSATION_SUBMISSION,
        Petition.PETITION_FINAL_APPOVAL])

    excluded = ['non_grnet_quota', 'participation_cost',
                'participation_payment_description', 'deleted', 'travel_files',
                'participation_local_cost', 'additional_expenses_initial',
                'additional_expenses_initial_description',
                'additional_expenses', 'additional_expenses_description',
                'user_recommendation', 'secretary_recommendation']
    excluded_travel_info = ['accommodation_local_cost', ]

    class Meta:
        proxy = True

    class Api:
        fields = Petition.Api.\
            fields + ('additional_expenses_initial',
                      'additional_expenses_default_currency',
                      'additional_expenses_initial_description',
                      'additional_expenses',
                      'non_grnet_quota',
                      'additional_expenses_local_currency',
                      'additional_expenses_description',
                      'travel_report', 'travel_files',
                      'compensation_petition_protocol',
                      'compensation_petition_date',
                      'compensation_decision_protocol',
                      'compensation_decision_date',
                      'manager_travel_approval',
                      'manager_final_approval',
                      'movement_id', 'expenditure_protocol',
                      'expenditure_date_protocol', 'movement_date_protocol',
                      'movement_protocol',
                      )
        filter_fields = Petition.Api.filter_fields
        search_fields = Petition.Api.search_fields
        read_only_fields = Petition.Api.read_only_fields +\
            ('user', 'task_start_date',
             'task_end_date', 'dse', 'project', 'travel_files', 'reason',
             'secretary_recommendation', 'user_recommendation',
             'status', 'additional_expenses_initial',
             'additional_expenses_default_currency',
             'additional_expenses_initial_description'
             'participation_cost', 'participation_default_currency',
             'participation_local_cost',
             'participation_local_currency',
             'participation_payment_way',
             'participation_payment_description', 'url',
             'manager_final_approval',
             'manager_travel_approval',
             'movement_id', 'expenditure_protocol',
             'expenditure_date_protocol', 'movement_protocol',
             'movement_date_protocol',
             )

        nested_relations = [
            ('travel_info', 'travel_info', TravelInfoCompensation)]
        extra_kwargs = {
            'dse': {
                'required': False, 'allow_null': True
            },
            'status': {'default': Petition.SECRETARY_COMPENSATION},
        }
        serializer_code = 'texpenses.serializers'
        serializer_module_name = 'petition'
        viewset_code = 'texpenses.views'
        viewset_module_name = 'secretary_compensation'
        resource_name = 'petition/secretary/compensations'
