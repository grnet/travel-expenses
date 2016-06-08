from django.contrib.auth import get_user_model
import datetime
from rest_framework import serializers
from djoser import settings, serializers as djoser_serializers
from django.contrib.auth.models import Group
from django.conf import settings as django_settings

from models import Specialty
from models import TaxOffice
from models import Kind
from models import Petition
from models import Project
from models import MovementCategories
from models import City
from models import Country
from models import CountryCategory
from models import Transportation
from models import PetitionStatus
from models import UserCategory

from models import AdditionalExpenses
from models import Compensation
from models import FeedingKind
from models import Flight
from models import Accomondation
from models import AdvancedPetition

User = get_user_model()


class UserProfileSerializer(serializers.HyperlinkedModelSerializer):

    """Serializer class for User model """

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name',
                  'email', 'password',
                  'iban', 'specialtyID', 'kind', 'taxRegNum', 'taxOffice',
                  'category', 'user_group', 'trip_days_left')
        read_only_fields = (
            'username',
            'password',
            'trip_days_left'
        )


class SpecialtySerializer(serializers.HyperlinkedModelSerializer):

    """Serializer class for specialty model """

    class Meta:
        model = Specialty
        fields = ('name', 'id', 'url', )
        read_only_fields = ('id', 'url',)


class KindSerializer(serializers.HyperlinkedModelSerializer):

    """Serializer class for kind model """

    class Meta:
        model = Kind
        fields = ('name', 'id', 'url', )
        read_only_fields = ('id', 'url',)


class UserCategorySerializer(serializers.HyperlinkedModelSerializer):

    """Serializer class for kind model """

    class Meta:
        model = UserCategory
        fields = ('name', 'id', 'max_overnight_cost', 'url', )
        read_only_fields = ('id', 'url',)


class TaxOfficeSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = TaxOffice
        fields = ('name', 'kindDescription', 'address',
                  'email', 'phone', 'id', 'url',)


class CustomUserRegistrationSerializer(
        djoser_serializers.UserRegistrationSerializer):

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        group = Group.objects.get(name='USER')
        group.user_set.add(user)

        category = UserCategory.objects.get(name='B')

        if settings.get('SEND_ACTIVATION_EMAIL'):
            user.is_active = False
            user.category = category
            user.save(update_fields=['is_active', 'category'])
        return user


class ProjectSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Project
        fields = ('id', 'name', 'accountingCode', 'url')
        read_only_fields = ('id', 'url',)


class MovementCategoriesSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = MovementCategories
        fields = ('id', 'name', 'url')
        read_only_fields = ('id', 'url')


class CitySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = City
        fields = ('id', 'name', 'country', 'url')
        read_only_fields = ('id', 'url')


class CountrySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Country
        fields = ('id', 'name', 'category', 'url')
        read_only_fields = ('id', 'url')


class CountryCategorySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = CountryCategory
        fields = ('id', 'name', 'url')
        read_only_fields = ('id', 'url')


class TransportationSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Transportation
        fields = ('id', 'name', 'url')
        read_only_fields = ('id', 'url')


class PetitionStatusSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = PetitionStatus
        fields = ('id', 'name', 'url')
        read_only_fields = ('id', 'url')


class AdditionalExpensesSerializer(serializers.HyperlinkedModelSerializer):

    def create(self, validated_data):
        request = self.context['request']
        validated_data['user'] = request.data['user']

        return AdditionalExpenses.objects.create(**validated_data)

    class Meta:
        model = AdditionalExpenses
        fields = ('id', 'name', 'cost', 'petition', 'url')
        read_only_fields = ('id', 'url')


class CompensationSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Compensation
        fields = ('id', 'name', 'country_category', 'user_category',
                  'compensation', 'url')
        read_only_fields = ('id', 'url')


class FeedingKindSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = FeedingKind
        fields = ('id', 'name', 'url')
        read_only_fields = ('id', 'url')


class FlightSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Flight
        fields = ('id', 'flightName', 'flightPrice', 'url')
        read_only_fields = ('id', 'url')


class AccomondationSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Accomondation
        fields = ('id', 'hotel', 'hotelPrice', 'url')
        read_only_fields = ('id', 'url')


class AdvancedPetitionSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = AdvancedPetition
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


class UserPetitionSerializer(serializers.HyperlinkedModelSerializer):

    def create(self, validated_data):

        user_object = self.context['request'].user
        validated_data['user'] = user_object

        # advanced_pet_info = validated_data['advanced_info']
        validated_data['trip_days_before'] = user_object.trip_days_left

        arrival_point = validated_data['arrivalPoint']
        user_category = user_object.category

        compensation_object = None

        if arrival_point and user_category:
            country_category_name = arrival_point.country.category.name
            compensation_object = Compensation.objects.get(
                name=user_category.name + country_category_name)

        # if not (advanced_pet_info and advanced_pet_info != ""):

        print "Create an empty advanced petition"

        ac = Accomondation(user=user_object, hotel="Hotel", hotelPrice=0.0)
        ac.save()
        fl = Flight(user=user_object, flightName="Flight", flightPrice=0.0)
        fl.save()
        feeding_kind_1 = FeedingKind.objects.get(id=1)
        ap = AdvancedPetition(accomondation=ac, flight=fl,
                              user=user_object,
                              compensation=compensation_object,
                              feeding=feeding_kind_1)
        ap.save()
        print "Done"
        validated_data['advanced_info'] = ap

        now = datetime.datetime.now()
        validated_data['creationDate'] = now
        validated_data['updateDate'] = now

        return Petition.objects.create(**validated_data)

    def update(self, instance, validated_data):

        user_object = instance.user
        arrival_point = validated_data['arrivalPoint']

        user_category = user_object.category

        compensation_object = None
        status = validated_data['status']

        print user_category
        if arrival_point and user_category:
            country_category_name = arrival_point.country.category.name
            compensation_object = Compensation.objects.get(
                name=user_category.name + country_category_name)

        instance.advanced_info.compensation = compensation_object
        instance.advanced_info.save()
        submission_statuses = [2, 4, 5, 6, 7, 8, 9]

        if status.id in submission_statuses:
            user_object.trip_days_left = instance.trip_days_after()
            user_object.save()

        days_left = user_object.trip_days_left
        days_left_default = django_settings.MAX_HOLIDAY_DAYS

        if status.id == 10 and days_left < days_left_default:
            user_object.trip_days_left = days_left + \
                instance.transport_days()
            user_object.save()
        now = datetime.datetime.now()
        validated_data['updateDate'] = now
        return super(UserPetitionSerializer, self).update(instance,
                                                          validated_data)

    class Meta:
        model = Petition
        fields = ('id', 'name', 'surname', 'iban', 'specialtyID', 'kind',
                  'taxRegNum', 'taxOffice',
                  'taskStartDate', 'taskEndDate', 'depart_date', 'return_date',
                  'creationDate', 'updateDate',
                  'project', 'reason', 'movementCategory',
                  'departurePoint', 'arrivalPoint', 'overnights_num',
                  'overnights_num_proposed',
                  'overnight_cost', 'max_overnight_cost', 'overnights_sum_cost',
                  'transport_days', 'transport_days_proposed',
                  'task_duration', 'same_day_return_task',
                  'compensation_level', 'compensation_days',
                  'compensation_days_proposed',
                  'additional_expenses_sum',
                  'max_compensation', 'compensation_final', 'total_cost',
                  'transportation', 'recTransport', 'recAccomondation',
                  'recCostParticipation', 'advanced_info',
                  'status', 'user_category', 'trip_days_before',
                  'trip_days_after', 'url')
        read_only_fields = (
            'id', 'url', 'creationDate', 'updateDate', 'advanced_info')
