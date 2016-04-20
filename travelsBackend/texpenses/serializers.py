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
from models import DeparturePoint
from models import ArrivalPoint
from models import Transportation

User = get_user_model()


class UserProfileSerializer(serializers.HyperlinkedModelSerializer):

    """Serializer class for User model """

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name',
                  'email', 'password',
                  'iban', 'specialtyID', 'kind', 'taxRegNum', 'taxOffice')
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


class TaxOfficeSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = TaxOffice
        fields = ('name', 'kindDescription',
                  'address', 'email', 'phone', 'id', 'url')


class CustomUserRegistrationSerializer(
        djoser_serializers.UserRegistrationSerializer):

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        group = Group.objects.get(name='USER')
        group.user_set.add(user)

        if settings.get('SEND_ACTIVATION_EMAIL'):
            user.is_active = False
            user.save(update_fields=['is_active'])
        return user


class AccomondationSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Accomondation
        fields = ('id', 'hotel', 'hotelPrice',
                  'checkInDate', 'checkOutDate', 'url')
        read_only_fieldsd = ('id',)


class ProjectSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Project
        fields = ('id', 'name', 'accountingCode', 'url')
        read_only_fieldsd = ('id',)


class MovementCategoriesSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = MovementCategories
        fields = ('id', 'name', 'url')
        read_only_fieldsd = ('id',)


class DeparturePointSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = DeparturePoint
        fields = ('id', 'name', 'url')
        read_only_fieldsd = ('id',)


class ArrivalPointSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ArrivalPoint
        fields = ('id', 'name', 'url')
        read_only_fieldsd = ('id',)


class TransportationSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Transportation
        fields = ('id', 'name', 'url')
        read_only_fieldsd = ('id',)


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
        fields = ('id', 'accomondation',
                  'taskStartDate', 'taskEndDate',
                  'project', 'reason', 'movementCategory',
                  'departurePoint', 'arrivalPoint', 'transportation',
                  'recTransport', 'recAccomondation',
                  'recCostParticipation', 'url')
        read_only_fields = ('id',)


# class UserProfilePetitionSerializer(serializers.HyperlinkedModelSerializer):

    # class Meta:
        # model = User
        # fields = ('id', 'username', 'first_name', 'last_name',
                  # 'email', 'password',
                  # 'iban', 'specialtyID', 'taxRegNum', 'taxOffice')
