from django.conf.urls import patterns, url

from .views import OrderView

urlpatterns = patterns(
    '',

    url(r'^(?P<order_id>\d+)/', OrderView.as_view(), name='order'),
)
