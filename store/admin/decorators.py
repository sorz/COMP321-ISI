from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test


# Reference:
# https://github.com/django/django/blob/master/django/contrib/admin/views/decorators.py
def vendor_required(view_func):
    """
    Decorator for views that checks that the user is logged in and is a staff
    member, displaying the login page if necessary.
    """
    return user_passes_test(
        lambda u: u.is_active and u.is_staff,
        login_url='admin:account:login',
        redirect_field_name=REDIRECT_FIELD_NAME
    )(view_func)
