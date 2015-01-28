from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect

from .forms import UserRegistrationForm, ProfileChangeForm

@login_required
def profile(request):

    dictionary = {}
    return render(request, 'account/profile.html', dictionary)


def register(request):
    if request.user.is_authenticated():
        logout(request)

    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)

        if user_form.is_valid():
            user_form.save()
            return redirect('account:register_done')

    else:
        user_form = UserRegistrationForm()

    dictionary = {'user_form': user_form}
    return render(request, 'account/register.html', dictionary)


def register_done(request):

    dictionary = {}
    return render(request, 'account/register_done.html', dictionary)


@login_required
def profile_change(request):

    if request.method == 'POST':
        form = ProfileChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()

            # TODO: tell user it's done.
            return redirect('account:profile')
    else:
        form = ProfileChangeForm(instance=request.user)

    dictionary = {'form': form}
    return render(request, 'account/profile_change.html', dictionary)
