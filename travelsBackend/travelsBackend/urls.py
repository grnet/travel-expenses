from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.views.generic.base import RedirectView
from . import auth_urls
from django.conf.urls.static import static
from texpenses.actions import load_apimas_urls

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browseable API.
admin.autodiscover()

api_prefix = settings.API_PREFIX

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^' + api_prefix + '/auth/', include(auth_urls)),
    url(r'^' + api_prefix + '/docs/', include('rest_framework_docs.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns.extend(load_apimas_urls())

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
