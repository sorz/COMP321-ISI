from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def create(request):

    dictionary = {}
    return render(request, 'order/create.html', dictionary)