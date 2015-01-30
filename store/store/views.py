from django.shortcuts import render


def home(request):
    dictionary = {'user': request.user}
    return render(request, 'store/home.html', dictionary)