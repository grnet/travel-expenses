from django.conf.urls import url, include
from rest_framework import routers
from texpenses import views
from django.contrib import admin
from . import auth_urls

router = routers.DefaultRouter()
router.register(r'user_profiles', views.UserViewSet)
router.register(r'specialty', views.SpecialtyViewSet)
router.register(r'taxoffice', views.TaxOfficeViewSet)
# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browseable API.

admin.autodiscover()
urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^auth/', include(auth_urls)),
    url(r'^users/', include(router.urls)),

]
