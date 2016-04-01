from django.conf.urls import url
from djoser import views as djoser_views
from django.contrib.auth import get_user_model
from texpenses import views

User = get_user_model()

auth_urlpatterns = (
    url(r'^me/$', djoser_views.UserView.as_view(), name='user'),
    url(r'^me/detailed/$', views.CustomUserView.as_view(),
        name='user_detailed'),
    url(r'^register/$', views.CustomUserRegistrationView.as_view(),
        name='register'),
    url(r'^activate/(?P<uid>\w{2,3})\/(?P<token>.*)',
        views.custom_activation_view, name='url_activation'),
    url(r'^activate/$', djoser_views.ActivationView.as_view(), name='activate'),
    url(r'^{0}/$'.format(User.USERNAME_FIELD),
        djoser_views.SetUsernameView.as_view(), name='set_username'),
    url(r'^password/$', djoser_views.SetPasswordView.as_view(),
        name='set_password'),
    url(r'^password/reset/$', djoser_views.PasswordResetView.as_view(),
        name='password_reset'),
    url(r'^password/reset/confirm/$',
        djoser_views.PasswordResetConfirmView.as_view(),
        name='password_reset_confirm'),
    url(r'^login/$', djoser_views.LoginView.as_view(), name='login'),
    url(r'^logout/$', djoser_views.LogoutView.as_view(), name='logout'),
    url(r'^$', djoser_views.RootView.as_view(
        urls_extra_mapping={
            'login': 'login', 'logout': 'logout',
            'me_detailed': 'user_detailed'}), name='root'),
)

urlpatterns = auth_urlpatterns +\
    (url(r'^$', djoser_views.RootView.as_view(), name='root'),)
