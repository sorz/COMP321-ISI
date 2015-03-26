from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns(
    '',
    url(r'pending/$', views.PendingView.as_view(), name='pending'),
    url(r'on-delivery/$', views.OnDeliveryView.as_view(), name='on-delivery'),
    url(r'(?P<order_id>\d+)/$', views.DetailView.as_view(), name='detail'),
)
