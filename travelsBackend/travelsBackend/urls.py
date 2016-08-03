from django.conf.urls import url, include
from rest_framework import routers
from django.contrib import admin
from django.conf import settings
from django.views.generic.base import RedirectView
from texpenses.factories.views import factory
from texpenses.models import (TaxOffice, Project, City, Country,
                              UserProfile,
                              UserPetition, UserPetitionSubmission,
                              SecretaryPetition, SecretaryPetitionSubmission)
from texpenses.permissions.custom_permissions import IsOwnerOrAdmin
from . import auth_urls

router = routers.DefaultRouter()
router.register(r'users', factory(UserProfile))

router_user = routers.DefaultRouter()
router_secretary = routers.DefaultRouter()
router_petition = routers.DefaultRouter()
router_resources = routers.DefaultRouter()

router_resources.register(r'tax-office', factory(TaxOffice))
router_resources.register(r'project', factory(Project))
router_resources.register(r'city', factory(City))
router_resources.register(r'country', factory(Country))


router_user.register(
    r'saved', factory(UserPetition, custom_permissions=(IsOwnerOrAdmin,),
                      serializer_module_name='petition'))
router_secretary.register(
    r'saved', factory(SecretaryPetition, serializer_module_name='petition'))
router_user.register(
    r'submitted', factory(UserPetitionSubmission,
                          custom_permissions=(IsOwnerOrAdmin,),
                          serializer_module_name='petition',
                          custom_methods=['cancel']))
router_secretary.register(
    r'submitted', factory(SecretaryPetitionSubmission,
                          serializer_module_name='petition'))


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browseable API.
admin.autodiscover()
api_prefix = settings.API_PREFIX
urlpatterns = [
    url(r'^' + api_prefix + '/admin/', include(admin.site.urls)),
    url(r'^' + api_prefix + '/auth/', include(auth_urls)),
    url(r'^' + api_prefix + '/users_related/', include(router.urls)),
    url(r'^' + api_prefix + '/resources/', include(router_resources.urls)),
    url(r'^' + api_prefix + '/petition/', include(router_petition.urls)),
    url(r'^' + api_prefix + '/petition/user/', include(router_user.urls)),
    url(r'^' + api_prefix + '/petition/secretary/',
        include(router_secretary.urls)),
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
