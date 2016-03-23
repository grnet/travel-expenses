from django.contrib import admin

# Register your models here.

from .models import UserProfile
from .models import Specialty
from .models import TaxOffice
admin.site.register(UserProfile)
admin.site.register(Specialty)
admin.site.register(TaxOffice)
