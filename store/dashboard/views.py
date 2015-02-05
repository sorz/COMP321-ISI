from django.shortcuts import render

from .decorators import vendor_required

@vendor_required
def overview(request):
    dictionary = {}
    return render(request, 'dashboard/overview.html', dictionary)
