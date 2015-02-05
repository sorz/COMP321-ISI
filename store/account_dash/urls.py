from django.conf.urls import patterns, url
from django.contrib.auth import views as auth_views

from .forms import VendorLoginForm


urlpatterns = patterns(
    '',
    url(r'^login/$', auth_views.login, name='login',
        kwargs={'template_name': 'account_dash/login.html',
                'authentication_form': VendorLoginForm}),

)
