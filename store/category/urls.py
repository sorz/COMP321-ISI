from django.conf.urls import patterns, url

from category import views

urlpatterns = patterns(
    '',
    url(r'^$', views.index, name='index'),
    url(r'^(?P<category_id>\d+)/$', views.detail, name='detail')
)