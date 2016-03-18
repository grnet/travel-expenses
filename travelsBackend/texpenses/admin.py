from django.contrib import admin

# Register your models here.

from .models import UserProfile
from .models import Specialty
from .models import TaxOffice
from .models import UserKind
admin.site.register(UserProfile)
admin.site.register(Specialty)
admin.site.register(TaxOffice)
admin.site.register(UserKind)
