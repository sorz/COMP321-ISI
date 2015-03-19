from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns(
    '',
    url(r'^$', views.VendorIndexView.as_view(
        template_name='category_admin/index.html'), name='index'),
    url(r'^(?P<category_id>\d+)/$', views.VendorDetailView.as_view(
        template_name='category_admin/detail.html'), name='detail'),
    url(r'^(?P<category_id>\d+)/edit/$', views.modify, name='modify'),
    url(r'^new/$', views.create, name='create'),
)
