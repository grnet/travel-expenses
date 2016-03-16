from django.conf.urls import url, include
from rest_framework import routers
from texpenses import views
# from django.conf.urls import patterns, include, url

# from django.contrib import admin

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'account', views.AccountViewSet)
router.register(r'specialty', views.SpecialtyViewSet)
router.register(r'userkind', views.UserKindViewSet)
router.register(r'taxoffice', views.TaxOfficeViewSet)
# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browseable API.

# admin.autodiscover()
urlpatterns = [
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/',
        include('rest_framework.urls', namespace='rest_framework'))
]


'''admin.autodiscover()
urlpatterns = patterns('',
    Examples:
    url(r'^$', 'travelsBackend.views.home', name='home'),
    url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
)'''
