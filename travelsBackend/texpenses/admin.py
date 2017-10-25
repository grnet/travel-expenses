from django.contrib import admin
from .models import UserProfile
from .models import TaxOffice
from .models import Petition
from .models import Project
from .models import Country
from .models import City
from .models import TravelInfo
from .models import CityDistances


class PetitionAdmin(admin.ModelAdmin):
    search_fields = ['dse']
    list_display = ('dse', 'project', 'user', 'created', 'deleted',
                    'updated', 'status', 'task_start_date', 'task_end_date')
    list_filter = ('created', 'updated', 'task_start_date', 'task_end_date',
                   'project', 'user')
    date_hierarchy = 'updated'
    ordering = ('-updated', '-task_start_date', '-task_end_date')


class CityAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_filter = ('country',)

admin.site.register(UserProfile)
admin.site.register(TaxOffice)
admin.site.register(Petition, PetitionAdmin)
admin.site.register(Project)
admin.site.register(Country)
admin.site.register(City, CityAdmin)
admin.site.register(TravelInfo)
admin.site.register(CityDistances)
