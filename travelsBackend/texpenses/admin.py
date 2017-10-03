from django.contrib import admin
from .models import UserProfile
from .models import TaxOffice
from .models import Petition
from .models import Project
from .models import Country
from .models import City
from .models import TravelInfo
from .models import CityDistances


admin.site.register(UserProfile)
admin.site.register(TaxOffice)
admin.site.register(Petition)
admin.site.register(Project)
admin.site.register(Country)
admin.site.register(City)
admin.site.register(TravelInfo)
admin.site.register(CityDistances)
