from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from djoser import settings, serializers as djoser_serializers

User = get_user_model()


class CustomUserRegistrationSerializer(
        djoser_serializers.UserRegistrationSerializer):

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        group, created = Group.objects.get_or_create(name='USER')
        group.user_set.add(user)

        if settings.get('SEND_ACTIVATION_EMAIL'):
            user.is_active = False
            user.save(update_fields=['is_active', 'category'])
        return user
