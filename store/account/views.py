from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse


@login_required
def profile(request):

    dictionary = {}
    return render(request, 'account/profile.html', dictionary)

