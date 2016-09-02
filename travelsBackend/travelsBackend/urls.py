from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.views.generic.base import RedirectView
from rest_framework import routers
from texpenses.generators.views import generate
from texpenses.models import (TaxOffice, Project, City, Country,
                              UserProfile,
                              UserPetition, UserPetitionSubmission,
                              UserCompensationSubmission,
                              UserCompensation,
                              SecretaryPetition, SecretaryPetitionSubmission)
from . import auth_urls

router = routers.DefaultRouter()
router.register(r'users', generate(UserProfile), base_name='userprofile')

router_user = routers.DefaultRouter()
router_secretary = routers.DefaultRouter()
router_petition = routers.DefaultRouter()
router_resources = routers.DefaultRouter()

router_resources.register(r'tax-office', generate(TaxOffice),
                          base_name='taxoffice')
router_resources.register(r'project', generate(Project), base_name='project')
router_resources.register(r'city', generate(City), base_name='city')
router_resources.register(r'country', generate(Country), base_name='country')


router_user.register(
    r'saved', generate(UserPetition), base_name='userpetition')
router_secretary.register(
    r'saved', generate(SecretaryPetition))
router_user.register(
    r'compensation/saved', generate(UserCompensation),
    base_name='usercompensation')
router_user.register(
    r'submitted', generate(UserPetitionSubmission),
    base_name='userpetitionsubmission')
router_secretary.register(
    r'submitted', generate(SecretaryPetitionSubmission),
    base_name='secretarypetitionsubmission')
router_user.register(
    r'compensation/submitted', generate(UserCompensationSubmission),
    base_name='usercompensationsubmission')

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browseable API.
admin.autodiscover()
api_prefix = settings.API_PREFIX
urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
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
