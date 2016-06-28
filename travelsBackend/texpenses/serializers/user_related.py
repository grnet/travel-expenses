from django.contrib.auth import get_user_model
from rest_framework import serializers
from djoser import settings, serializers as djoser_serializers
from django.contrib.auth.models import Group
from texpenses.models import Specialty, Kind, UserCategory, TaxOffice

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
        group, created = Group.objects.get_or_create(name='USER')
        group.user_set.add(user)

        category, created = UserCategory.objects.get_or_create(name='B')

        if settings.get('SEND_ACTIVATION_EMAIL'):
            user.is_active = False
            user.category = category
            user.save(update_fields=['is_active', 'category'])
        return user
