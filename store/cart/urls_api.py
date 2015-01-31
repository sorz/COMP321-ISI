from django.conf.urls import patterns, url

from cart.views import ItemView

urlpatterns = patterns(
    '',
    url(r'^(?P<product_id>\d+)/', ItemView.as_view(), name='item'),
)
