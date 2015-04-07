from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.views import login as login_view
from django.db.models import Q

from .forms import VendorRegistrationForm


def _vendor_account_exists():
    return User.objects.filter(Q(is_staff=True) | Q(is_superuser=True)).exists()


def login(request, **kwargs):
    if not _vendor_account_exists():
        return redirect('admin:account:register')
    else:
        return login_view(request, **kwargs)


def register(request):
    """Registering a staff account.

    Forbidden if any staff or superuser exists.
    """
    if _vendor_account_exists():
        return render(request, 'account_admin/create.html', status=403)

    if request.method == 'POST':
        form = VendorRegistrationForm(request.POST)

        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "Registered successfully.")
            return redirect('admin:account:login')

    else:
        form = VendorRegistrationForm()

    dictionary = {'form': form}
    return render(request, 'account_admin/create.html', dictionary)
