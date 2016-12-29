from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from djoser import settings, serializers as djoser_serializers
from rest_framework import serializers
from texpenses.models import UserProfile

User = get_user_model()


class CustomUserRegistrationSerializer(
        djoser_serializers.UserRegistrationSerializer):

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
                  'user_category', 'user_group', 'trip_days_left')
        read_only_fields = ('username', 'trip_days_left', 'user_category')
        extra_kwargs = {'tax_office': {'view_name':
                                       'resources/tax-office-detail'}}
