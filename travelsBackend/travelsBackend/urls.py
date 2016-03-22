from django.conf.urls import url, include
from rest_framework import routers
from texpenses import views
from django.contrib import admin


router = routers.DefaultRouter()
router.register(r'userprofiles', views.UserViewSet)
router.register(r'specialty', views.SpecialtyViewSet)
router.register(r'userkind', views.UserKindViewSet)
router.register(r'taxoffice', views.TaxOfficeViewSet)
# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browseable API.

admin.autodiscover()
urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^auth/', include('djoser.urls.authtoken')),
    url(r'^users/', include(router.urls)),
]
# authpatterns = [

    # url(r'^auth/', include(router.urls)),
    # url(r'^auth/',
    # include('rest_framework.urls', namespace='rest_framework')),
    # url(
        # r'^auth/login/$',
        # LoginView.as_view(),
        # name='login'),
    # url(
        # r'^auth/logout/$',
        # LogoutView.as_view(),
        # name='logout'),

# ]
# urlpatterns += authpatterns
