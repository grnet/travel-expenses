from django.contrib.auth import get_user_model
from rest_framework import serializers
from djoser import settings, serializers as djoser_serializers
from django.contrib.auth.models import Group
from models import Specialty
from models import TaxOffice
from models import Kind
from models import Petition
from models import Accomondation
from models import Project
from models import MovementCategories
from models import City
from models import Country
from models import CountryCategory
from models import Transportation
from models import PetitionStatus
from models import UserCategory

User = get_user_model()


class UserProfileSerializer(serializers.HyperlinkedModelSerializer):

    """Serializer class for User model """

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name',
                  'email', 'password',
                  'iban', 'specialtyID', 'kind', 'taxRegNum', 'taxOffice',
                  'category')
        read_only_fields = (
            'username',
            'password',
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


class AccomondationSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Accomondation
        fields = ('id', 'hotel', 'hotelPrice',
                  'checkInDate', 'checkOutDate', 'url')
        read_only_fields = ('id', 'url',)


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
        fields = ('id', 'name', 'compensation', 'url')
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
        validated_data['user'] = self.context['request'].user
        return Petition.objects.create(**validated_data)

    class Meta:
        model = Petition
        fields = ('id', 'name', 'surname', 'iban', 'specialtyID', 'kind',
                  'taxRegNum', 'taxOffice', 'accomondation',
                  'taskStartDate', 'taskEndDate', 'creationDate', 'updateDate',
                  'project', 'reason', 'movementCategory',
                  'departurePoint', 'arrivalPoint', 'transportation',
                  'recTransport', 'recAccomondation',
                  'recCostParticipation', 'status', 'url')
        read_only_fields = ('id', 'url',)
