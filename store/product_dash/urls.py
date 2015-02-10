from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns(
    '',
    url(r'^(?P<product_id>\d+)/$', views.detail, name='detail'),
    url(r'^new/$', views.create, name='create'),

)
