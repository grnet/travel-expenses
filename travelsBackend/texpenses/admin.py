from django.contrib import admin
from .models import UserProfile
from .models import TaxOffice
from .models import Petition
from .models import Project
from .models import Country
from .models import City

from .models import AdditionalExpenses
# Register custom models here.

# user profile related models
admin.site.register(UserProfile)
admin.site.register(TaxOffice)

# user petition related models
admin.site.register(Petition)
admin.site.register(Project)

# advanced petition info models
admin.site.register(AdditionalExpenses)

admin.site.register(Country)
admin.site.register(City)
