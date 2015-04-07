from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q

from .forms import VendorRegistrationForm


def register(request):
    """Registering a staff account.

    Forbidden if any staff or superuser exists.
    """
    if User.objects.filter(Q(is_staff=True) | Q(is_superuser=True)).exists():
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
