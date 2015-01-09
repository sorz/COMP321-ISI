from django.shortcuts import render, get_object_or_404

from category.models import Category


def index(request):
    categories = Category.objects.all()

    dictionary = {'categories': categories}
    return render(request, 'category/index.html', dictionary)


def detail(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    products = category.product_set.all()

    dictionary = {'category': category, 'products': products}
    return render(request, 'category/detail.html', dictionary)
