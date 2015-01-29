from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from .models import Category


def index(request):
    categories = Category.objects.all()

    dictionary = {'categories': categories}
    return render(request, 'category/index.html', dictionary)


def detail(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    products = category.product_set.filter(off_shelf=False)

    name_filter = request.GET.get('filter', '')
    if name_filter:
        products = products.filter(name__contains=name_filter)

    sort = request.GET.get('sort')
    if sort in ('price', '-price', 'rating', '-rating'):
        products = products.order_by(sort)
    else:
        sort = ''

    # Code of pagination is from
    # https://docs.djangoproject.com/en/1.7/topics/pagination/#using-paginator-in-a-view

    paginator = Paginator(products, 3)  # 3 products per page for testing

    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        products = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        products = paginator.page(paginator.num_pages)

    dictionary = {'category': category, 'products': products,
                  'sort': sort, 'filter': name_filter}
    return render(request, 'category/detail.html', dictionary)
