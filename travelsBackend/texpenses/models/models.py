from datetime import timedelta
from django.conf import settings
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.utils import timezone
from django.core.validators import MinValueValidator
from django.contrib.auth.models import AbstractUser
from django.db import models
from model_utils import FieldTracker
from texpenses.models import common
from texpenses.validators import (
    afm_validator, iban_validation, required_validator, date_validator)


class TaxOffice(models.Model):

    """ Model which contains all tax offices of Greece. """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=300, blank=True)
    address = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20)

    class APITravel(object):
        fields = ('id', 'url', 'name', 'description', 'address',
                  'email', 'phone')
        read_only_fields = ('id', 'url')
        allowed_operations = ('list', 'retrieve')

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
    iban = models.CharField(max_length=200,
                            validators=[iban_validation])
    specialty = models.CharField(
        max_length=5, choices=common.SPECIALTY)
    tax_reg_num = models.CharField(max_length=9,
                                   validators=[afm_validator])
    tax_office = models.ForeignKey(TaxOffice)
    kind = models.CharField(max_length=5, choices=common.KIND)
    category = models.CharField(max_length=1, choices=common.USER_CATEGORIES,
                                blank=False, null=False, default='B')

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

    trip_days_left = models.IntegerField(default=settings.MAX_HOLIDAY_DAYS)

    class APITravel(object):
        fields = ('username', 'first_name', 'last_name', 'email',
                  'iban', 'specialty', 'kind', 'tax_reg_num', 'tax_office',
                  'category', 'user_group', 'trip_days_left')
        read_only_fields = ('username', 'trip_days_left', 'category')
        allowed_operations = ('list', 'retrieve')

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
    name = models.CharField(max_length=200, blank=True, null=True)
    accounting_code = models.CharField(max_length=20)
    manager = models.ForeignKey(UserProfile, blank=True, null=True)

    class APITravel(object):
        fields = ('id', 'url', 'name', 'accounting_code', 'manager')
        read_only_fields = ('id', 'url')
        allowed_operations = ('list', 'retrieve')

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
    name = models.CharField(max_length=20)
    category = models.CharField(choices=CATEGORIES, max_length=1, default='A')

    class APITravel(object):
        fields = ('id', 'url', 'name', 'category')
        read_only_fields = ('id', 'url', 'category')
        allowed_operations = ('list', 'retrieve')

    def __unicode__(self):
        """TODO: to be defined1. """
        return self.name


class City(models.Model):

    """Model for cities. """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    country = models.ForeignKey(Country, blank=True, null=True)

    class APITravel(object):
        fields = ('id', 'url', 'name', 'country')
        read_only_fields = ('id', 'url', 'country')
        nested_relations = [('country', 'country')]
        allowed_operations = ('list', 'retrieve')

    def __unicode__(self):
        """TODO: to be defined. """
        return self.name


class Accommodation(models.Model):

    """
    An abstract model that represents the accommodation related info
    """
    accommodation_price = models.FloatField(
        blank=False, null=False, default=0.0)
    accommodation_payment_way = models.CharField(
        max_length=30, choices=common.WAYS_OF_PAYMENT, blank=False,
        null=False, default='NON')
    accommodation_payment_description = models.CharField(
        max_length=200, blank=True, null=True)

    class Meta:
        abstract = True


class Transportation(models.Model):

    """
    An abstract model that represents the transportation related info
    """
    transportation_price = models.FloatField(
        blank=False, null=False, default=0.0)
    transportation_payment_way = models.CharField(
        max_length=5, choices=common.WAYS_OF_PAYMENT,
        blank=False, null=False, default='NON')
    transportation_payment_description = models.CharField(
        max_length=200, blank=True, null=True)

    class Meta:
        abstract = True


class TravelInfo(Accommodation, Transportation):

    """
    An abstract model class that represents travel information.

    Travel information are associated with the duration, departure and arrival
    point, transportation, accommodation, etc.
    """
    depart_date = models.DateTimeField(blank=True, null=True)
    return_date = models.DateTimeField(blank=True, null=True)
    departure_point = models.ForeignKey(
        City, blank=False, null=False, related_name='travel_departure_point')
    arrival_point = models.ForeignKey(City, blank=False, null=False,
                                      related_name='travel_arrival_point')
    mean_of_transport = models.CharField(choices=common.TRANSPORTATION,
                                         max_length=10, blank=False, null=False,
                                         default='AIR')
    transport_days_manual = models.IntegerField(blank=False, null=False,
                                                default=0)
    overnights_num_manual = models.IntegerField(blank=False, null=False,
                                                default=0)
    compensation_days_manual = models.IntegerField(blank=False, null=False,
                                                   default=0)
    meal = models.CharField(max_length=10, choices=common.MEALS,
                            blank=False, null=False, default='NON')
    travel_petition = models.ForeignKey('Petition')

    tracked_fields = ['depart_date', 'return_date']
    tracker = FieldTracker(fields=tracked_fields)

    class APITravel:
        fields = ('id', 'url', 'arrival_point', 'departure_point',
                  'mean_of_transport'
                  'accommodation_price', 'accommodation_payment_way',
                  'accommodation_payment_description',
                  'return_date', 'depart_date',
                  'transportation_price', 'transportation_payment_way',
                  'transportation_payment_description',
                  'transport_days_proposed', 'overnights_num_proposed',
                  'overnight_cost', 'compensation_level',
                  'same_day_return_task', 'get_compensation',
                  'overnights_num_manual', 'transport_days_manual',
                  'compensation_days_manual', 'meal')
        read_only_fields = ('id', 'url')
        allowed_operations = ('list', 'retrieve', 'delete')

    def clean(self):
        if self.depart_date and self.return_date \
                and self.travel_petition.task_end_date:
            date_validator(self.depart_date, self.return_date,
                           ('depart', 'return'))
            date_validator(self.depart_date,
                           self.travel_petition.task_end_date,
                           ('depart', 'task end'))
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
        Checks that the accommodation_price does not surpass the maximum
        overnight limit based on the category of user.

        :raises: ValidationError if accommodation price exceeds the allowable
        limit.
        """
        EXTRA_COST = 100
        max_overnight_cost = common.MAX_OVERNIGHT_COST[
            self.travel_petition.category]
        max_overnight_cost += EXTRA_COST if self.is_city_ny() else 0
        if self.accommodation_price > max_overnight_cost:
            raise ValidationError('Accomondation price %.2f for petition with'
                                  ' DSE %s exceeds the max overnight cost.' % (
                                      self.accommodation_price,
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
        if not (self.return_date and self.depart_date):
            return 0
        first_day = task_start_date - timedelta(days=1)\
            if (task_start_date - self.depart_date).days >= 1\
            else self.depart_date
        last_day = task_end_date + timedelta(days=1) if (
            self.return_date - task_end_date).days >= 1 else self.return_date
        return (last_day.date() - first_day.date()).days

    def overnight_cost(self):
        """ Returns total overnight cost. """
        return self.accommodation_price * self.overnights_num_manual

    def is_city_ny(self):
        """
        Checks if city is `New YORK` and returns True if this is the case;
        False otherwise.
        """
        try:
            return self.arrival_point.name.lower() == "new york"
        except City.DoesNotExist:
            return False

    def compensation_level(self):
        """Calculates the compensation level based on country and user category
        :returns:compensation level

        """
        return common.COMPENSATION_CATEGORIES[(
            self.travel_petition.category,
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

    def get_compensation(self):
        """Calculates the compensation based on compensation days,
        compensation level and additional expenses
        :returns: The maximum possible compensation

        """
        percentage = 100
        max_compensation = self.compensation_days_manual * \
            self.compensation_level()
        if self.same_day_return_task():
            max_compensation *= 0.5
        compensation_proportion = common.COMPENSATION_PROPORTION[self.meal]\
            if self.meal else 1
        return max_compensation * compensation_proportion * (
            self.travel_petition.grnet_quota() / percentage)


class SecretarialInfo(models.Model):

    """
    Abstract model which includes information that secretary fills.
    """
    non_grnet_quota = models.FloatField(blank=True, null=True, default=0.0)

    movement_num = models.CharField(max_length=200, null=True, blank=True)
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
        blank=False, null=False, default=0.0,
        validators=[MinValueValidator(0.0)])

    participation_payment_way = models.CharField(
        max_length=10, choices=common.WAYS_OF_PAYMENT, blank=False,
        null=False, default='NON')
    participation_payment_description = models.CharField(
        max_length=200, blank=True, null=True)

    class Meta:
        abstract = True


class Petition(TravelUserProfile, SecretarialInfo, ParticipationInfo):
    SAVED_BY_USER = 1
    SUBMITTED_BY_USER = 2
    SAVED_BY_SECRETARY = 3
    SUBMITTED_BY_SECRETARY = 4
    CANCELLED = 10
    DELETED = 100

    # Fields that are copied from user object.
    USER_FIELDS = ['first_name', 'last_name', 'iban', 'specialty', 'kind',
                   'tax_office', 'tax_reg_num', 'category']

    id = models.AutoField(primary_key=True)
    dse = models.IntegerField(blank=False, null=False)
    travel_info = models.ManyToManyField(TravelInfo, blank=False)
    user = models.ForeignKey(UserProfile, blank=False, null=False)
    task_start_date = models.DateTimeField(blank=True, null=True)
    task_end_date = models.DateTimeField(blank=True, null=True)
    created = models.DateTimeField(blank=False, null=False,
                                   default=timezone.now())
    updated = models.DateTimeField(blank=True, null=True)
    project = models.ForeignKey(Project, blank=False, null=False)
    reason = models.CharField(max_length=500, blank=False, null=False)
    status = models.IntegerField(blank=True, null=True)

    additional_expenses_initial = models.FloatField(
        blank=False, null=False, default=0.0,
        validators=[MinValueValidator(0.0)])
    additional_expenses_initial_description = models.CharField(
        max_length=400, blank=True, null=True)
    first_name = models.CharField(max_length=200, blank=False, null=False)
    last_name = models.CharField(max_length=200, blank=False, null=False)

    tracked_fields = ['task_start_date', 'task_end_date']
    tracker = FieldTracker()

    class APITravel:
        fields = ('id', 'dse', 'first_name', 'last_name', 'kind',
                  'specialty', 'tax_office', 'tax_reg_num', 'category', 'user',
                  'task_start_date', 'task_end_date', 'created', 'updated',
                  'travel_info', 'project', 'reason',
                  'additional_expenses_initial',
                  'additional_expenses_initial_description',
                  'trip_days_before', 'trip_days_after', 'status',
                  'participation_cost', 'participation_payment_way',
                  'participation_payment_description', 'url',
                  'overnights_sum_cost',
                  'overnights_proposed', 'transport_days', 'trip_days_before',
                  'trip_days_after', 'overnights_num', 'overnights_proposed',
                  'overnights_sum_cost', 'task_duration', 'compensation_final',
                  'total_cost')
        read_only_fields = ('id', 'user', 'url', 'first_name', 'last_name',
                            'kind', 'specialty', 'tax_office', 'tax_reg_num',
                            'category', 'iban', 'status', 'dse')
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
            self.validate_dates()

    def delete(self):
        """
        Overrides the `delete` method of model.

        It doesn't actually delete the object, but it sets its status as
        `DELETED`.
        """
        self.status = self.DELETED
        self.save()

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

    def validate_dates(self):
        """
        Validates that the given date when task starts is before from
        the date when task ends.
        """
        date_validator(self.task_start_date, self.task_end_date,
                       ('task start', 'task end'))

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
        return sum(travel_obj.get_compensation()
                   for travel_obj in self.travel_info.all())

    def total_cost(self):
        """
        Gets the total expenses of trip.

        This value is calculated by adding the transportation,
        compensation, partication and accommodation costs.
        """
        transportation_cost = sum(travel.transportation_price
                                  for travel in self.travel_info.all())
        return sum([transportation_cost, self.participation_cost,
                    self.compensation_final(), self.overnights_sum_cost()])

    def __unicode__(self):
        return str(self.id) + "-" + self.project.name


class PetitionManager(models.Manager):

    def __init__(self, status, *args, **kwargs):
        self.status = status
        super(PetitionManager, self).__init__(*args, **kwargs)

    def create(self, *args, **kwargs):
        """
        Add status argument for creating model based on the status specified
        by this manager.
        """
        kwargs['status'] = self.status
        return super(PetitionManager, self).create(
            *args, **kwargs)

    def get_queryset(self):
        """
        Filters Petition objects by the status specified by this manager.
        """
        return super(PetitionManager, self).get_queryset()\
            .filter(status=self.status)


class UserPetition(Petition):

    """ A proxy model for the temporary saved petition by user. """
    objects = PetitionManager(Petition.SAVED_BY_USER)

    class Meta:
        proxy = True

    class APITravel:
        fields = Petition.APITravel.fields
        read_only_fields = Petition.APITravel.read_only_fields
        nested_relations = [('travel_info', 'travel_info')]


class UserPetitionSubmission(Petition):

    """ A proxy model for the temporary submitted petitions by user. """
    objects = PetitionManager(Petition.SUBMITTED_BY_USER)
    required_fields = (
        'first_name', 'last_name', 'specialty', 'task_start_date',
        'task_end_date', 'kind', 'tax_reg_num', 'tax_office', 'iban',
        'project', 'reason', 'departure_point',
        'arrival_point', 'depart_date', 'return_date', 'mean_of_transport')

    class Meta:
        proxy = True

    class APITravel:
        fields = Petition.APITravel.fields
        read_only_fields = Petition.APITravel.read_only_fields
        nested_relations = [('travel_info', 'travel_info')]

    def clean(self):
        required_validator(self, self.required_fields)
        super(UserPetitionSubmission, self).clean()

    def save(self, **kwargs):
        # Remove temporary saved petition with the corresponding dse.
        try:
            UserPetition.objects.get(dse=self.dse).delete()
        except ObjectDoesNotExist:
            pass
        super(UserPetitionSubmission, self).save(**kwargs)


class SecretaryPetition(Petition):

    """ A proxy model for the temporary saved petitions by secretary. """
    objects = PetitionManager(Petition.SAVED_BY_SECRETARY)

    class Meta:
        proxy = True

    class APITravel:
        fields = Petition.APITravel.fields + (
            'non_grnet_quota', 'grnet_quota', 'user',
            'expenditure_protocol',
            'expenditure_date_protocol', 'movement_protocol',
            'movement_date_protocol', 'compensation_petition_protocol',
            'compensation_petition_date',
            'compensation_decision_protocol',
            'compensation_decision_date')
        read_only_fields = ('id', 'url', 'first_name', 'last_name',
                            'kind', 'specialty', 'tax_office', 'tax_reg_num',
                            'category', 'status', 'dse', 'travel_info')
        nested_relations = [('travel_info', 'travel_info')]

    def save(self, *args, **kwargs):
        self.updated = timezone.now()
        super(SecretaryPetition, self).save(*args, **kwargs)


class SecretaryPetitionSubmission(Petition):

    """ A proxy model for the temporary submitted petitions by secretary. """
    objects = PetitionManager(Petition.SUBMITTED_BY_SECRETARY)
    required_fields = ('name', 'surname', 'iban', 'specialty', 'kind',
                       'tax_reg_num', 'tax_office',
                       'task_start_date', 'task_end_date',
                       'project', 'reason',
                       'status', 'user_category',
                       'additional_expenses_initial_description',
                       'additional_expenses_initial', 'non_grnet_quota',
                       'grnet_quota',
                       'expenditure_protocol', 'expenditure_date_protocol',
                       'movement_protocol', 'movement_date_protocol')

    class Meta:
        proxy = True

    class APITravel:
        fields = Petition.APITravel.fields + (
            'non_grnet_quota', 'grnet_quota', 'user',
            'expenditure_protocol',
            'expenditure_date_protocol', 'movement_protocol',
            'movement_date_protocol', 'compensation_petition_protocol',
            'compensation_petition_date',
            'compensation_decision_protocol',
            'compensation_decision_date')
        read_only_fields = Petition.APITravel.read_only_fields
        nested_relations = [('travel_info', 'travel_info')]

    def clean(self):
        required_validator(self, self.required_fields)
        super(SecretaryPetitionSubmission, self).clean()

    def save(self, **kwargs):
        # Remove temporary saved petition with the corresponding dse.
        try:
            SecretaryPetition.objects.get(dse=self.dse).delete()
        except ObjectDoesNotExist:
            pass
        super(SecretaryPetitionSubmission, self).save(**kwargs)
