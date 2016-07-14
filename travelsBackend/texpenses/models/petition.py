from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.utils import timezone
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Sum
from workdays import networkdays
from texpenses.models.user_related import UserProfile, TaxOffice
from texpenses.models.services import get_queryset_on_group
from texpenses.models import common
from texpenses.validators import (
    afm_validator, iban_validation, required_validator, date_validator)


class Project(models.Model):

    """Docstring for Project. """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    accountingCode = models.CharField(max_length=20)

    class APITravel(object):
        fields = ('id', 'name', 'accountingCode', 'url')

    def __unicode__(self):
        return self.name


class Country(models.Model):
    CATEGORIES = (
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C')
    )

    """Docstring for Countries. """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    category = models.CharField(choices=CATEGORIES, max_length=1, default='A')

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


class UserSnapshot(models.Model):
    """
    Abstract model class which gets the information about a user profile at
    the moment he is making a new petition.
    """
    first_name = models.CharField(max_length=200, blank=False, null=False)
    last_name = models.CharField(max_length=200, blank=False, null=False)
    SPECIALTIES = tuple([(k, v) for k, v in common.SPECIALTY.iteritems()])
    KINDS = tuple([(k, v) for k, v in common.KIND.iteritems()])
    USER_CATEGORIES = tuple([(category, category)
                             for category in common.USER_CATEGORIES])

    iban = models.CharField(max_length=200, blank=True, null=True,
                            validators=[iban_validation])
    specialtyID = models.CharField(max_length=10, choices=SPECIALTIES)
    taxRegNum = models.CharField(max_length=9, blank=True, null=True,
                                 validators=[afm_validator])
    taxOffice = models.ForeignKey(TaxOffice, blank=True, null=True)
    kind = models.CharField(max_length=10, choices=KINDS, blank=True,
                            null=True)
    category = models.CharField(max_length=10, choices=USER_CATEGORIES,
                                blank=True, null=True)
    trip_days_before = models.IntegerField(blank=False, null=False,
                                           validators=[MinValueValidator(0)])

    class Meta:
        abstract = True


class TravelInfo(models.Model):
    """
    An abstract model class that represents travel information.

    Travel information are associated with the duration, departure and arrival
    point, transportation, accomondation, etc.
    """
    TRANSPORTATIONS = tuple([(k, v)
                             for k, v in common.TRANSPORTATION.iteritems()])
    FEEDINGS = tuple([(k, v) for k, v in common.FEEDING.iteritems()])

    FULL_FEEDING = "1"
    SEMI_FEEDING = "2"
    NON_FEEDING = "3"

    depart_date = models.DateTimeField(blank=True, null=True)
    return_date = models.DateTimeField(blank=True, null=True)
    departurePoint = models.ForeignKey(
        City, blank=False, null=False, related_name='travel_departure_point')
    arrivalPoint = models.ForeignKey(City, blank=False, null=False,
                                     related_name='travel_arrival_point')
    transportation = models.CharField(choices=TRANSPORTATIONS,
                                      max_length=10, blank=True, null=True)
    accomondation_price = models.FloatField(blank=False, null=False,
                                            default=0.0)
    transportation_price = models.FloatField(blank=False, null=False,
                                             default=0.0)
    transport_days_manual = models.IntegerField(blank=False, null=False,
                                                default=0)
    overnights_num_manual = models.IntegerField(blank=False, null=False,
                                                default=0)
    feeding = models.CharField(max_length=10, choices=FEEDINGS,
                               blank=True, null=True)
    movement_num = models.CharField(max_length=200, null=True, blank=True)
    travel_petition = models.ForeignKey('Petition')

    def clean(self):
        if self.depart_date and self.return_date:
            date_validator(self.depart_date, self.return_date,
                           ('depart', 'return'))
            date_validator(self.depart_date, self.petition.taskEndDate,
                           ('depart', 'task end'))
        self.validate_overnight_cost()
        super(TravelInfo, self).clean()

    def validate_overnight_cost(self):
        """
        Checks that the accomondation_price does not surpass the maximum
        overnight limit based on the category of user.

        :raises: ValidationError if accomondation price exceeds the allowable
        limit.
        """
        if self.accomondation_price > common.USER_CATEGORIES[
                self.travel_petition.category]:
            raise ValidationError('Accomondation price %.2f for petition with'
                                  ' DSE %s exceeds the max overnight cost.' % (
                                      self.accomondation_price,
                                      str(self.travel_petition.dse)))

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

    def overnights_num_proposed(self, tsd, ted):
        if not (self.return_date and self.depart_date):
            return 0
        first_day = min(self.depart_date, tsd)\
            if (tsd - self.depart_date).days == 1\
            else max(self.depart_date, tsd)
        last_day = max(ted, self.depart_date) if (
            self.return_date - ted).days == 1 else min(ted, self.depart_date)
        return (last_day - first_day).days

    def overnight_cost(self):
        return self.accomondation_price * self.overnights_num_manual

    def is_city_ny(self):
        if self.arrivalPoint is None:
            return False
        return self.arrivalPoint.name == "NEW YORK"

    class APITravel:
        fields = ('id', 'url', 'depart_date', 'return_date',
                  'departurePoint', 'arrivalPoint',
                  'transportation',
                  'accomondation_price', 'transportation_price',
                  'transport_days_manual',
                  'overnights_num_manual',
                  'feeding', 'movement_num')
        read_only_fields = ('id', 'url')


class SecretarialInfo(models.Model):
    """
    Abstract model which includes information that secretary fills.
    """
    non_grnet_quota = models.FloatField(blank=True, null=True, default=0.0)

    compensation_days_manual = models.IntegerField(blank=False, null=False,
                                                   default=0)
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


def get_next_dse():
    try:
        return Petition.objects.latest('dse').dse + 1
    except:
        return 1


class Petition(UserSnapshot, SecretarialInfo):
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
    travel_info = models.ManyToManyField(TravelInfo, blank=False, null=False)
    user = models.ForeignKey(UserProfile, blank=False, null=False)
    taskStartDate = models.DateTimeField(blank=False, null=False)
    taskEndDate = models.DateTimeField(blank=False, null=False)
    creationDate = models.DateTimeField(blank=False, null=False,
                                        default=timezone.now())
    updateDate = models.DateTimeField(blank=True, null=True)
    project = models.ForeignKey(Project, blank=False, null=False)
    reason = models.CharField(max_length=500, blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    participation_cost = models.FloatField(
        blank=False, null=False, default=0.0,
        validators=[MinValueValidator(0.0)])
    additional_expenses_initial = models.FloatField(
        blank=False, null=False, default=0.0,
        validators=[MinValueValidator(0.0)])
    additional_expenses_initial_description = models.CharField(
        max_length=400, blank=True, null=True)

    class APITravel:
        fields = ('id', 'dse', 'first_name', 'last_name', 'kind',
                  'specialtyID', 'taxOffice', 'taxRegNum', 'category', 'user',
                  'taskStartDate', 'taskEndDate', 'travel_info',
                  'project', 'reason', 'additional_data',
                  'additional_expenses_initial', 'additional_data',
                  'additional_expenses_initial_description',
                  'trip_days_before', 'status', 'participation_cost',
                  'url', 'overnights_sum_cost', 'compensation_final',
                  'total_cost', 'overnights_proposed')
        read_only_fields = ('id', 'user', 'url', 'first_name', 'last_name',
                            'kind', 'specialtyID', 'taxOffice', 'taxRegNum',
                            'category', 'status', 'dse', 'travel_info')

    def __init__(self, *args, **kwargs):
        super(Petition, self).__init__(*args, **kwargs)
        for field in self.USER_FIELDS:
            setattr(self, field, getattr(self.user, field))

    def clean(self):
        """
        Overrides `clean` method and checks if specified dates are valid.
        """
        super(Petition, self).clean()
        self.validate_dates()

    def validate_dates(self):
        date_validator(self.taskStartDate, self.taskEndDate,
                       ('task start', 'task end'))

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

    def compensation_final(self):
        # This code is a hack. The compensation is calculated based on the
        # defined compensation days. However, the number of daily compensation
        # is calculated based on the feeding type, country category and the
        # use category. This code does not predict the case where the user
        # must travel in two destinations with different feeding type and
        # are located in different countries.
        try:
            travel_obj = self.travel_info.all().order_by('-return_date')[0]
        except IndexError:
            return 0
        compensation = common.COMPENSATION_CATEGORIES[(
            self.category, travel_obj.arrivalPoint.country.category)]
        comp_sum = self.compensation_days_manual * compensation\
            + self.additional_expenses_sum()
        if self.same_day_return_task(
                travel_obj.depart_date, travel_obj.return_date):
            comp_sum *= 0.5
        decrease = {
            travel_obj.FULL_FEEDING: 1,
            travel_obj.SEMI_FEEDING: 0.5,
            travel_obj.NON_FEEDING: 0.25
        }
        decrease_rate = decrease[travel_obj.feeding]\
            if travel_obj.feeding else 1
        return comp_sum * decrease_rate * (self.grnet_quota() / 100)

    def same_day_return_task(self, depart_date, return_date):
        if self.taskEndDate is None or return_date is None \
                or self.taskStartDate is None or depart_date is None:
            return False
        return self.taskEndDate.date() == return_date.date()\
            == self.taskStartDate.date() == depart_date.date()

    def transport_days(self):
        return sum(travel.transport_days_manual
                   for travel in self.travel_info.all())

    def trip_days_after(self):
        return self.trip_days_before - self.transport_days()

    def overnights_num(self):
        return sum(travel.overnights_num_manual
                   for travel in self.travel_info.all())

    def overnights_proposed(self):
        return sum(travel.overnights_num_proposed(
            self.taskStartDate, self.taskEndDate)
                   for travel in self.travel_info.all())

    def overnights_sum_cost(self):
        return sum(travel.overnight_cost()
                   for travel in self.travel_info.all())

    def task_duration(self):
        if self.taskEndDate is None or self.taskStartDate is None:
            return 0
        return (self.taskEndDate - self.taskStartDate).days

    def max_overnight_cost(self):
        EXTRA_COST = 100
        default_max_overnight_cost = self.category.max_overnight_cost
        return default_max_overnight_cost + EXTRA_COST if self.is_city_ny()\
            else default_max_overnight_cost

    def additional_expenses_sum(self):
        ae = AdditionalExpenses.objects.filter(petition=self).\
            aggregate(Sum('cost'))
        if ae['cost__sum'] is None:
            return 0
        return ae['cost__sum']

    def total_cost(self):
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
        kwargs['status'] = self.status
        return super(PetitionManager, self).create(
            *args, **kwargs)

    def get_queryset(self):
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

    def save(self, **kwargs):
        self.status = self.SAVED_BY_USER
        super(UserPetition, self).save(**kwargs)


class UserPetitionSubmission(Petition):
    """ A proxy model for the temporary submitted petitions by user. """
    objects = PetitionManager(Petition.SUBMITTED_BY_USER)
    required_fields = ('taskStartDate', 'taskEndDate',
                       'project', 'reason', 'movementCategory',
                       'departurePoint', 'arrivalPoint', 'transportation',
                       'trip_days_before')

    class Meta:
        proxy = True

    class APITravel:
        fields = Petition.APITravel.fields
        read_only_fields = Petition.APITravel.read_only_fields

    def clean(self):
        required_validator(self, self.required_fields)
        super(UserPetitionSubmission, self).clean()

    def save(self, **kwargs):
        self.status = self.SUBMITTED_BY_USER
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
            'non_grnet_quota', 'grnet_quota',
            'expenditure_protocol',
            'expenditure_date_protocol', 'movement_protocol',
            'movement_date_protocol', 'compensation_petition_protocol',
            'compensation_petition_date',
            'compensation_decision_protocol',
            'compensation_decision_date')
        read_only_fields = ('id', 'url', 'first_name', 'last_name',
                            'kind', 'specialtyID', 'taxOffice', 'taxRegNum',
                            'category', 'status', 'dse', 'travel_info')

    def save(self, *args, **kwargs):
        self.status = self.SAVED_BY_SECRETARY
        super(SecretaryPetition, self).save(*args, **kwargs)


class SecretaryPetitionSubmission(Petition):
    """ A proxy model for the temporary submitted petitions by secretary. """
    objects = PetitionManager(Petition.SUBMITTED_BY_SECRETARY)
    required_fields = ('name', 'surname', 'iban', 'specialtyID', 'kind',
                       'taxRegNum', 'taxOffice',
                       'taskStartDate', 'taskEndDate',
                       'project', 'reason',
                       'status', 'user_category', 'trip_days_before',
                       'trip_days_after',
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

    def clean(self):
        required_validator(self, self.required_fields)
        super(SecretaryPetitionSubmission, self).clean()

    def save(self, **kwargs):
        self.status = self.SUBMITTED_BY_SECRETARY
        # Remove temporary saved petition with the corresponding dse.
        try:
            SecretaryPetition.objects.get(dse=self.dse).delete()
        except ObjectDoesNotExist:
            pass
        super(SecretaryPetitionSubmission, self).save(**kwargs)


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
