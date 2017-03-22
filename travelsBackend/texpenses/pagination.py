from rest_framework.pagination import PageNumberPagination
from django.conf import settings


class TexpensesPagination(PageNumberPagination):
    page_size = settings.PAGINATION_PAGE_SIZE
