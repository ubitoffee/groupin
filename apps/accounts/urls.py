from django.contrib.auth.views import logout_then_login
from django.conf.urls import url
from . import views, password_views


urlpatterns = [
    url(r'^register/?$', views.register, name='register'),
    url(r'^login/?$', views.signin, name='login'),
    url(r'^logout/?$', logout_then_login, name='logout'),
    url(
        r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate_user,
        name='activate'
    ),
    url(r'^password_reset/?$', password_views.password_reset_request, name='password_reset_request'),
    url(
        r'^password_reset_confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        password_views.password_reset_confirm,
        name='password_reset_confirm'
    ),
    url(r'^profile/(?P<username>\w+)/?$', views.profile, name='profile')

]
