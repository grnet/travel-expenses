from django.contrib import admin
from .models import UserProfile
from .models import Specialty
from .models import TaxOffice
from .models import Kind
from .models import Accomondation
from .models import MovementCategories
from .models import Petition
from .models import Project
from .models import Transportation
from .models import PetitionStatus
from .models import CountryCategory
from .models import Country
from .models import City
# Register custom models here.

# user profile related models
admin.site.register(UserProfile)
admin.site.register(Specialty)
admin.site.register(TaxOffice)
admin.site.register(Kind)

# user petition related models
admin.site.register(Accomondation)
admin.site.register(MovementCategories)
admin.site.register(Petition)
admin.site.register(Project)
admin.site.register(Transportation)
admin.site.register(PetitionStatus)

admin.site.register(CountryCategory)
admin.site.register(Country)
admin.site.register(City)
