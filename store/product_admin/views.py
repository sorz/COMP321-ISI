from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db import transaction


from .forms import ProductForm, PhotoFormSet
from product.models import Product
from admin.decorators import vendor_required


@vendor_required
def detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    if request.method == 'POST':
        product_form = ProductForm(request.POST, instance=product)
        photo_formset = PhotoFormSet(request.POST, request.FILES, instance=product)

        if product_form.is_valid() and photo_formset.is_valid():
            product_form.save()
            photo_formset.save()
            messages.add_message(request, messages.SUCCESS, "Product saved.")
            return redirect('admin:category:detail', product.category_id)

    else:
        product_form = ProductForm(instance=product)
        photo_formset = PhotoFormSet(instance=product)

    dictionary = {'product': product, 'product_form': product_form,
                  'photo_formset': photo_formset}
    return render(request, 'product_admin/detail.html', dictionary)


class PhotoFormNotValidException(Exception):
    pass


@vendor_required
def create(request):
    if request.method == 'POST':
        product_form = ProductForm(request.POST)

        if product_form.is_valid():

            photo_formset = None
            # Product form have to be saved, then we can validate photo form.
            # Disable autocommit, so we can rollback if photo form is invalid.
            try:
                with transaction.atomic():
                    product = product_form.save()
                    photo_formset = PhotoFormSet(request.POST, request.FILES, instance=product)

                    if photo_formset.is_valid():
                        photo_formset.save()
                        messages.add_message(request, messages.SUCCESS,
                                             "Product %s added." % product.name)
                        return redirect('admin:product:create')

                    else:
                        # Photo form validate failed,
                        # raise a exception which cause product rollback.
                        raise PhotoFormNotValidException

            except PhotoFormNotValidException:
                if photo_formset is None:
                    photo_formset = PhotoFormSet(request.POST, request.FILES)
        else:
            photo_formset = PhotoFormSet(request.POST, request.FILES)

    else:
        product_form = ProductForm()
        photo_formset = PhotoFormSet()

    dictionary = {'product_form': product_form, 'photo_formset': photo_formset}
    return render(request, 'product_admin/detail.html', dictionary)
