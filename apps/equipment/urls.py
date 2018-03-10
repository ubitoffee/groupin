from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^list/?$', views.get_list, name='list'),
    url(r'^register/?$', views.register, name='register'),
    url(r'^edit/(?P<id>\d+)/?$', views.edit, name='edit'),
    # url(r'^remove/?$', views.remove, name='remove')
]
