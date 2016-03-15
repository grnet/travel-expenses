from django.conf.urls import url, include
from rest_framework import routers
from texpenses import views
# from django.conf.urls import patterns, include, url

# from django.contrib import admin
# from texpenses import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browseable API.

urlpatterns = [
    url(r'^', include(router.urls)),
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
