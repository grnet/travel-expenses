from django.contrib import admin
from .models import UserProfile
from .models import Specialty
from .models import TaxOffice
from .models import Kind

# Register custom models here.

admin.site.register(UserProfile)
admin.site.register(Specialty)
admin.site.register(TaxOffice)
admin.site.register(Kind)
