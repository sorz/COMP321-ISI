from django.conf.urls import patterns, url, include

from . import views

urlpatterns = patterns(
    '',
    url(r'^$', views.overview, name='overview'),

    url(r'^category/', include('category_dash.urls', namespace='category')),

)