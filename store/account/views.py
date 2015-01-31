from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import UserRegistrationForm, ProfileForm, UserChangeForm
from .models import Profile


@login_required
def profile(request):

    dictionary = {}
    return render(request, 'account/profile.html', dictionary)


def register(request):
    if request.user.is_authenticated():
        logout(request)

    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        profile_form = ProfileForm(request.POST, prefix='profile')

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user_profile = profile_form.save(commit=False)
            user_profile.user = user
            user_profile.save()

            return redirect('account:register_done')

    else:
        user_form = UserRegistrationForm()
        profile_form = ProfileForm(prefix='profile')

    dictionary = {'user_form': user_form, 'profile_form': profile_form}
    return render(request, 'account/register.html', dictionary)


def register_done(request):

    dictionary = {}
    return render(request, 'account/register_done.html', dictionary)


@login_required
def profile_change(request):

    try:
        user_profile = request.user.profile
    except Profile.DoesNotExist:
        user_profile = Profile(user=request.user)

    if request.method == 'POST':
        user_form = UserChangeForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST,
                                   instance=user_profile, prefix='profile')
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

            messages.add_message(request, messages.SUCCESS,
                                 "Profile has been changed.")
            return redirect('account:profile')
    else:
        user_form = UserChangeForm(instance=request.user)
        profile_form = ProfileForm(instance=user_profile, prefix='profile')

    dictionary = {'user_form': user_form, 'profile_form': profile_form}
    return render(request, 'account/profile_change.html', dictionary)
