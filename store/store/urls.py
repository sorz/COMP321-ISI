from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'store.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', 'store.views.home', name='home'),
    url('^about/$', 'store.views.about', name='about'),

    url(r'^category/', include('category.urls', namespace='category')),
    url(r'^product/', include('product.urls', namespace='product')),
    url(r'^cart/', include('cart.urls', namespace='cart')),
    url(r'^order/', include('order.urls', namespace='order')),
    url(r'^account/', include('account.urls', namespace='account')),
    url(r'^admin/', include('admin.urls', namespace='admin')),

    # RESTful APIs.
    url(r'^api/cart/', include('cart.urls_api', namespace='cart_api')),
    url(r'^api/order/', include('order.urls_api', namespace='order_api')),

    # url(r'^admin/', include(admin.site.urls)),

)


# Serving media (user-uploaded) files by Django.
# This should only be used in development environment.
# HTTP server should be configured to serve them directly in product environment.

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
