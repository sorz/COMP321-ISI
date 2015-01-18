from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns(
    '',
    url(r'^new/$', views.create, name='create'),
    url(r'^current/$', views.current, name='current'),
    url(r'^past/$', views.past, name='past')
)
