from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns(
    '',
    url(r'^$', views.VendorIndexView.as_view(
        template_name='category_dash/index.html'), name='index'),
    url(r'^(?P<category_id>\d+)/$', views.VendorDetailView.as_view(
        template_name='category_dash/detail.html'), name='detail')
)
