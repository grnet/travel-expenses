import django_filters as filters
from texpenses.models import Petition


class PetitionFilter(filters.FilterSet):

    depart_date = filters.DateTimeFilter(name='travel_info__depart_date',
                                         lookup_expr='exact')
    depart_date__gt = filters.DateTimeFilter(name='travel_info__depart_date',
                                             lookup_expr='gt')
    depart_date__gte = filters.DateTimeFilter(name='travel_info__depart_date',
                                              lookup_expr='gte')
    depart_date__lt = filters.DateTimeFilter(name='travel_info__depart_date',
                                             lookup_expr='lt')
    depart_date__lte = filters.DateTimeFilter(name='travel_info__depart_date',
                                              lookup_expr='lte')

    return_date = filters.DateTimeFilter(name='travel_info__return_date',
                                         lookup_expr='exact')
    return_date__gt = filters.DateTimeFilter(name='travel_info__return_date',
                                             lookup_expr='gt')
    return_date__gte = filters.DateTimeFilter(name='travel_info__return_date',
                                              lookup_expr='gte')
    return_date__lt = filters.DateTimeFilter(name='travel_info__return_date',
                                             lookup_expr='lt')
    return_date__lte = filters.DateTimeFilter(name='travel_info__return_date',
                                              lookup_expr='lte')

    first_name = filters.CharFilter(name='first_name',
                                    lookup_expr='unaccent__icontains')
    last_name = filters.CharFilter(name='last_name',
                                   lookup_expr='unaccent__icontains')

    class Meta:
        model = Petition
        fields = ['id', 'first_name', 'last_name', 'status', 'created',
                  'updated', 'withdrawn',
                  'depart_date', 'depart_date__gt', 'depart_date__gte',
                  'depart_date__lt', 'depart_date__lte',  'project',
                  'return_date', 'return_date__gt', 'return_date__lt',
                  'return_date__gte', 'return_date__lte', 'dse', 'user'
                  ]
