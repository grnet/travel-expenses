from django.contrib import admin
from .models import UserProfile
from .models import Specialty
from .models import TaxOffice
from .models import Kind
from .models import Accomondation
from .models import ArrivalPoint
from .models import DeparturePoint
from .models import MovementCategories
from .models import Petition
from .models import Project
from .models import Transportation

# Register custom models here.

# user profile related models
admin.site.register(UserProfile)
admin.site.register(Specialty)
admin.site.register(TaxOffice)
admin.site.register(Kind)

# user petition related models
admin.site.register(Accomondation)
admin.site.register(ArrivalPoint)
admin.site.register(DeparturePoint)
admin.site.register(MovementCategories)
admin.site.register(Petition)
admin.site.register(Project)
admin.site.register(Transportation)
