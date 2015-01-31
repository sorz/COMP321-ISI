from django.conf.urls import patterns, url

from cart import views

urlpatterns = patterns(
    '',
    url(r'^$', views.index, name='index'),
    url(r'^api/$', views.rest_cart, name='cart'),
)
