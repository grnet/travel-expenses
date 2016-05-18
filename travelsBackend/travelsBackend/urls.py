from django.conf.urls import url, include
from rest_framework import routers
from texpenses import views
from django.contrib import admin
from . import auth_urls

router = routers.DefaultRouter()
router.register(r'specialty', views.SpecialtyViewSet)
router.register(r'taxoffice', views.TaxOfficeViewSet)
router.register(r'kind', views.KindViewSet)
router.register(r'category', views.UserCategoryViewSet)


router_petition = routers.DefaultRouter()
router_petition.register(r'project', views.ProjectViewSet)
router_petition.register(
    r'movement_categories', views.MovementCategoriesViewSet)
router_petition.register(r'city', views.CityViewSet)
router_petition.register(r'country', views.CountryViewSet)
router_petition.register(r'country_categories', views.CountryCategoryViewSet)
router_petition.register(r'transportation', views.TransportationViewSet)
# router_petition.register(r'user', views.PetitionUserView)
router_petition.register(r'accomondation', views.AccomondationViewSet,
                         base_name='accomondation')
router_petition.register(r'advanced_petition', views.AdvancedPetitionViewSet,
                         base_name='advancedpetition')
router_petition.register(r'compensation_categories', views.CompensationViewSet)
router_petition.register(r'feeding', views.FeedingViewSet)
router_petition.register(r'flight', views.FlightViewSet, base_name='flight')
router_petition.register(r'additional_expenses',
                         views.AdditionalExpensesViewSet,
                         base_name='additionalexpenses')

router_petition.register(
    r'user_petition', views.UserPetitionViewSet, 'petition')
router_petition.register(
    r'petition_status', views.PetitionStatusViewSet)


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browseable API.
admin.autodiscover()
urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^auth/', include(auth_urls)),
    url(r'^users_related/', include(router.urls)),
    url(r'^petition/', include(router_petition.urls)),
    url(r'^docs/', include('rest_framework_docs.urls')),

]
