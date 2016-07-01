from django.contrib.auth import get_user_model
from djoser import settings, serializers as djoser_serializers
from django.contrib.auth.models import Group
from texpenses.models import UserCategory

User = get_user_model()


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
