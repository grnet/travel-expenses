import django_filters as filters
from texpenses.models import Petition


class PetitionFilter(filters.FilterSet):

    depart_date = filters.DateTimeFilter(name='travel_info__depart_date',
                                         lookup_type='exact')
    depart_date__gt = filters.DateTimeFilter(name='travel_info__depart_date',
                                             lookup_type='gt')
    depart_date__gte = filters.DateTimeFilter(name='travel_info__depart_date',
                                              lookup_type='gte')
    depart_date__lt = filters.DateTimeFilter(name='travel_info__depart_date',
                                             lookup_type='lt')
    depart_date__lte = filters.DateTimeFilter(name='travel_info__depart_date',
                                              lookup_type='lte')

    return_date = filters.DateTimeFilter(name='travel_info__return_date',
                                         lookup_type='exact')
    return_date__gt = filters.DateTimeFilter(name='travel_info__return_date',
                                             lookup_type='gt')
    return_date__gte = filters.DateTimeFilter(name='travel_info__return_date',
                                              lookup_type='gte')
    return_date__lt = filters.DateTimeFilter(name='travel_info__return_date',
                                             lookup_type='lt')
    return_date__lte = filters.DateTimeFilter(name='travel_info__return_date',
                                              lookup_type='lte')

    class Meta:
        model = Petition
        fields = ['id', 'first_name', 'last_name', 'created', 'updated',
                  'depart_date', 'depart_date__gt', 'depart_date__gte',
                  'depart_date__lt', 'depart_date__lte',  'project',
                  'return_date', 'return_date__gt', 'return_date__lt',
                  'return_date__gte', 'return_date__lte', 'dse'
                  ]
