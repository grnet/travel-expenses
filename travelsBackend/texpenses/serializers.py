from django.contrib.auth import get_user_model
from rest_framework import serializers
from djoser import settings, serializers as djoser_serializers
from django.contrib.auth.models import Group
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

from models import AdditionalWage
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
                  'category', 'trip_days_left')
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
        fields = ('name', 'id', 'url', )
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


class AdditionalWagesSerializer(serializers.HyperlinkedModelSerializer):

    def create(self, validated_data):
        request = self.context['request']
        validated_data['user'] = request.data['user']

        return AdditionalWage.objects.create(**validated_data)

    class Meta:
        model = AdditionalWage
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
        fields = ('id', 'dse', 'depart_date', 'return_date', 'accomondation',
                  'flight', 'feeding', 'non_grnet_quota', 'compensation',
                  'overnights_sum_cost', 'sum_compensation', 'same_day_return',
                  'expenditure_protocol',
                  'expenditure_date_protocol', 'movement_protocol',
                  'movement_date_protocol',
                  'compensation_petition_protocol',
                  'compensation_petition_date',
                  'compensation_decision_protocol',
                  'compensation_decision_date', 'url')
        read_only_fields = ('id', 'url')


class UserPetitionSerializer(serializers.HyperlinkedModelSerializer):

    # user = UserProfileSerializer()
    # def create(self, validated_data):
        # self.
        # user = User.objects.create_user(**validated_data)
        # group = Group.objects.get(name='USER')
        # group.user_set.add(user)

        # if settings.get('SEND_ACTIVATION_EMAIL'):
            # user.is_active = False
            # user.save(update_fields=['is_active'])
        # return user

    def create(self, validated_data):
        user_object = self.context['request'].user
        validated_data['user'] = user_object

        advanced_pet_info = validated_data['advanced_info']
        if not (advanced_pet_info and advanced_pet_info != ""):
            print "Create an empty advanced petition"
            ac = Accomondation(user=user_object, hotel="Hotel")
            ac.save()
            fl = Flight(user=user_object, flightName="Flight")
            fl.save()
            ap = AdvancedPetition(accomondation=ac, flight=fl, user=user_object)
            ap.save()
            print "Done"
            validated_data['advanced_info'] = ap

        return Petition.objects.create(**validated_data)

    class Meta:
        model = Petition
        fields = ('id', 'name', 'surname', 'iban', 'specialtyID', 'kind',
                  'taxRegNum', 'taxOffice',
                  'taskStartDate', 'taskEndDate', 'creationDate', 'updateDate',
                  'project', 'reason', 'movementCategory',
                  'departurePoint', 'arrivalPoint', 'overnights_num',
                  'transport_days', 'overnight_cost', 'overnights_sum_cost',
                  'task_duration', 'same_day_return_task', 'compensation_level',
                  'transportation', 'compensation_days',
                  'recTransport', 'recAccomondation',
                  'recCostParticipation', 'advanced_info', 'max_compensation',
                  'status', 'user_category', 'url')
        read_only_fields = ('id', 'url',)
