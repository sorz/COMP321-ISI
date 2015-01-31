from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import HttpResponseRedirect
from django.contrib import messages

from .models import Product, Rating
from .forms import RatingForm


@ensure_csrf_cookie
def detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    # Handle rating.
    rating = None
    if request.user.is_authenticated():
        try:
            rating = request.user.rating_set.get(product=product)
        except Rating.DoesNotExist:
            if product.has_bought_by_user(request.user):
                rating = Rating(product=product, user=request.user)

    if request.method == 'POST':
        rating_form = RatingForm(request.POST, instance=rating)

        if rating_form.is_valid():
            rating_form.save()
            product.update_rating()

            messages.add_message(request, messages.SUCCESS,
                                 "Thanks for your rating.")
            # Refresh page to prevent duplicate submission
            return HttpResponseRedirect('.')

    else:
        if rating is not None:
            rating_form = RatingForm(instance=rating)
        else:
            rating_form = None

    dictionary = {'product': product,
                  'rating_form': rating_form}
    if product.off_shelf:
        return render(request, 'product/off-shelf.html', dictionary, status=404)
    else:
        return render(request, 'product/detail.html', dictionary)
