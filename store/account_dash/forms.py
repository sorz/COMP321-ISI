from django import forms
from django.contrib.auth.forms import AuthenticationForm


class VendorLoginForm(AuthenticationForm):
    """
    Like a standard authentication form, but only
    staffs or superuser are allowed to login.
    """
    def confirm_login_allowed(self, user):
        super().confirm_login_allowed(user)
        if not user.is_staff:
            raise forms.ValidationError('This account is not a admin.',
                                        code='no_permission')

