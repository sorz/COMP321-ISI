from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages


from .forms import ProductForm, PhotoFormSet
from product.models import Product


def detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    if request.method == 'POST':
        product_form = ProductForm(request.POST, instance=product)
        photo_formset = PhotoFormSet(request.POST, request.FILES, instance=product)

        if product_form.is_valid() and photo_formset.is_valid():
            product_form.save()
            photo_formset.save()
            messages.add_message(request, messages.SUCCESS, "Product saved.")
            return redirect('dashboard:category:detail', product.category_id)

    else:
        product_form = ProductForm(instance=product)
        photo_formset = PhotoFormSet(instance=product)

    dictionary = {'product': product, 'product_form': product_form,
                  'photo_formset': photo_formset}
    return render(request, 'product_dash/detail.html', dictionary)


def create(request):
    # TODO: add new product.
    pass