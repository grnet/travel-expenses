import django_filters as filters
from texpenses.models import Petition


class PetitionFilter(filters.FilterSet):

    created = filters.DateTimeFilter(name='created',
                                     lookup_type='exact')
    created_year__gt = filters.NumberFilter(name='created',
                                            lookup_type='year__gt')
    created_year__lt = filters.NumberFilter(name='created',
                                            lookup_type='year__lt')

    class Meta:
        model = Petition
        fields = ['created', 'created_year__gt', 'created_year__lt', 'project']
