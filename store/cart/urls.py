from django.conf.urls import patterns, url

from cart import views

urlpatterns = patterns(
    '',
    url(r'^$', views.index, name='index'),
)
