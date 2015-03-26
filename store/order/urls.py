from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns(
    '',
    url(r'^$', views.index, name='index'),
    url(r'^new/$', views.create, name='create'),
    url(r'^current/$', views.CurrentView.as_view(), name='current'),
    url(r'^past/$', views.PastView.as_view(), name='past'),
    url(r'^(?P<order_id>\d+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^(?P<order_id>\d+)/done/', views.done, name='done'),
)
