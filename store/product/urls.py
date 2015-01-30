from django.conf.urls import patterns, url

from product import views

urlpatterns = patterns(
    '',
    url(r'^(?P<product_id>\d+)/$', views.detail, name='detail')
)