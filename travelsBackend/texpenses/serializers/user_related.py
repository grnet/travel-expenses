from django.db import transaction
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.http import HttpResponse
from djoser import settings, serializers as djoser_serializers
from rest_framework import serializers
from texpenses.models import UserProfile

User = get_user_model()


class CustomUserRegistrationSerializer(
        djoser_serializers.UserRegistrationSerializer):

    @transaction.atomic
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        group, created = Group.objects.get_or_create(name='USER')
        group.user_set.add(user)

        if settings.get('SEND_ACTIVATION_EMAIL'):
            user.is_active = False
            user.save(update_fields=['is_active', 'user_category'])
        return user


class PasswordResetConfirmRetypeSerializer(djoser_serializers.
                                           PasswordRetypeSerializer):
    pass


class UserProfileSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = UserProfile
        fields = ('username', 'first_name', 'last_name', 'email',
                  'iban', 'specialty', 'kind', 'tax_reg_num', 'tax_office',
                  'user_category', 'user_group', 'trip_days_left', 'id')
        read_only_fields = ('username', 'trip_days_left', 'user_category', 'id')
        extra_kwargs = {'tax_office': {'view_name':
                                       'api_tax-office-detail'}}
