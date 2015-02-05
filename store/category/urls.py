from django.conf.urls import patterns, url

from category import views

urlpatterns = patterns(
    '',
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<category_id>\d+)/$', views.DetailView.as_view(), name='detail')
)