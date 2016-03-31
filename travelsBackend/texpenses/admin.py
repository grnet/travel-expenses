from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import UserProfile
from .models import Specialty
from .models import TaxOffice
# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton


class CustomUserInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'grnet_related_info'

# Define a new User admin


class UserAdmin(BaseUserAdmin):
    inlines = (CustomUserInline, )

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# Register custom models here.

admin.site.register(UserProfile)
admin.site.register(Specialty)
admin.site.register(TaxOffice)
