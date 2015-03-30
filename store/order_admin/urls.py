from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns(
    '',
    url(r'pending/$', views.PendingView.as_view(), name='pending'),
    url(r'on-delivery/$', views.OnDeliveryView.as_view(), name='on-delivery'),
    url(r'fulfilled/$', views.FulfilledView.as_view(), name='fulfilled'),
    url(r'cancelled/$', views.CancelledView.as_view(), name='cancelled'),
    url(r'(?P<order_id>\d+)/$', views.DetailView.as_view(), name='detail'),
)
