from django.conf.urls import patterns, url, include

from . import views

urlpatterns = patterns(
    '',
    url(r'^$', views.overview, name='overview'),

    url(r'^category/', include('category_admin.urls', namespace='category')),
    url(r'^product/', include('product_admin.urls', namespace='product')),
    url(r'^account/', include('account_admin.urls', namespace='account')),
    url(r'order/', include('order_admin.urls', namespace='order')),

)
