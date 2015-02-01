from django.shortcuts import render


def overview(request):
    dictionary = {}
    return render(request, 'dashboard/overview.html', dictionary)
