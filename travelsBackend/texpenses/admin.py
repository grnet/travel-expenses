from django.contrib import admin
from .models import UserProfile
from .models import Specialty
from .models import TaxOffice
from .models import Kind
from .models import MovementCategories
from .models import Petition
from .models import Project
from .models import Transportation
from .models import PetitionStatus
from .models import CountryCategory
from .models import Country
from .models import City
from .models import UserCategory

from .models import AdvancedPetition
from .models import AdditionalWages
from .models import Compensation
from .models import FeedingKind
from .models import Flight
from .models import Accomondation
# Register custom models here.

# user profile related models
admin.site.register(UserProfile)
admin.site.register(Specialty)
admin.site.register(TaxOffice)
admin.site.register(Kind)
admin.site.register(UserCategory)

# user petition related models
admin.site.register(MovementCategories)
admin.site.register(Petition)
admin.site.register(Project)
admin.site.register(Transportation)
admin.site.register(PetitionStatus)

# advanced petition info models
admin.site.register(AdvancedPetition)
admin.site.register(AdditionalWages)
admin.site.register(Compensation)
admin.site.register(FeedingKind)
admin.site.register(Flight)
admin.site.register(Accomondation)

admin.site.register(CountryCategory)
admin.site.register(Country)
admin.site.register(City)
