from django.conf.urls import url
from django.contrib.auth import get_user_model
from texpenses import views

User = get_user_model()

auth_urlpatterns = (
    url(r'^me/$', views.CustomUserView.as_view(), name='user'),
    url(r'^me/detailed/$', views.CustomUserDetailedView.as_view(),
        name='user_detailed'),
    url(r'^register/$', views.CustomUserRegistrationView.as_view(),
        name='register'),
    url(r'^activate/$', views.CustomEmailActivationView.as_view(),
        name='activate'),
    url(r'^{0}/$'.format(User.USERNAME_FIELD),
        views.CustomSetUsernameView.as_view(), name='set_username'),
    url(r'^password/$', views.CustomSetPasswordView.as_view(),
        name='set_password'),
    url(r'^password/reset/$', views.CustomPasswordResetView.as_view(),
        name='password_reset'),
    url(r'^password/reset/confirm/$',
        views.PasswordResetView.as_view(),
        name='password_reset_confirm'),
    url(r'^login/$', views.CustomLoginView.as_view(), name='login'),
    url(r'^logout/$', views.CustomLogoutView.as_view(), name='logout'),
    url(r'^$', views.CustomRootView.as_view(
        urls_extra_mapping={
            'login': 'login', 'logout': 'logout',
            'me_detailed': 'user_detailed'}), name='root'),
)

urlpatterns = auth_urlpatterns +\
    (url(r'^$', views.CustomRootView.as_view(), name='root'),)
