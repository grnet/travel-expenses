from django.conf.urls import url, include
from rest_framework import routers
from texpenses import views
from django.contrib import admin
from django.conf import settings
from django.views.generic.base import RedirectView
from texpenses.views.factories import viewset_factory
from texpenses.models import Specialty, TaxOffice, Kind, UserCategory
from . import auth_urls

router = routers.DefaultRouter()
router.register(r'specialty', viewset_factory(Specialty))
router.register(r'tax-office', viewset_factory(TaxOffice))
router.register(r'kind', viewset_factory(Kind))
router.register(r'category', viewset_factory(UserCategory))


router_petition = routers.DefaultRouter()
router_petition.register(r'project', views.ProjectViewSet)
router_petition.register(
    r'movement-categories', views.MovementCategoriesViewSet)
router_petition.register(r'city', views.CityViewSet)
router_petition.register(r'country', views.CountryViewSet)
router_petition.register(r'country-categories', views.CountryCategoryViewSet)
router_petition.register(r'transportation', views.TransportationViewSet)
# router_petition.register(r'user', views.PetitionUserView)
router_petition.register(r'accommondation', views.AccomondationViewSet,
                         base_name='accomondation')
router_petition.register(r'advanced_petition', views.AdvancedPetitionViewSet,
                         base_name='advancedpetition')
router_petition.register(r'compensation-categories', views.CompensationViewSet)
router_petition.register(r'feeding', views.FeedingViewSet)
router_petition.register(r'flight', views.FlightViewSet, base_name='flight')
router_petition.register(r'additional-expenses',
                         views.AdditionalExpensesViewSet,
                         base_name='additionalexpenses')

router_petition.register(
    r'user_petition', views.UserPetitionViewSet, 'petition')
router_petition.register(
    r'petition-status', views.PetitionStatusViewSet)


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browseable API.
admin.autodiscover()
api_prefix = settings.API_PREFIX
urlpatterns = [
    url(r'^' + api_prefix + '/admin/', include(admin.site.urls)),
    url(r'^' + api_prefix + '/auth/', include(auth_urls)),
    url(r'^' + api_prefix + '/users_related/', include(router.urls)),
    url(r'^' + api_prefix + '/petition/', include(router_petition.urls)),
    url(r'^' + api_prefix + '/docs/', include('rest_framework_docs.urls')),

]

ui_prefix = getattr(settings, 'UI_PREFIX', 'ui/')
if ui_prefix and ui_prefix != '/':
    urlpatterns += [
        url('^$', RedirectView.as_view(url=ui_prefix))
    ]

if getattr(settings, 'SERVE_UI', True):
    # make django app serve ember dist files
    from django.conf.urls.static import static
    from django.views.static import serve
    from os import path

    root = path.dirname(__file__)
    ui_root = path.abspath(path.join(root, '..', '..', 'travelsFront/dist'))

    # admin may optionaly use a custom dist dir via settings
    ui_root = getattr(settings, 'UI_ROOT', ui_root)
    assets = path.join(ui_root, 'assets')

    # this should match ember application baseURL setting
    urlpatterns += static('%sassets/' % ui_prefix, document_root=assets)

    # serve index.html for all paths
    urlpatterns += [
        url('^%s.*' % ui_prefix, serve, {
            'path': 'index.html',
            'document_root': ui_root
            }),
    ]
