from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import HttpResponseRedirect

from .models import Product, Rating
from .forms import RatingForm


@ensure_csrf_cookie
def detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    # Handle rating.
    if request.method == 'POST':
        rating_form = RatingForm(request.POST)

        rating_form.instance.user = request.user
        if rating_form.is_valid():
            rating_form.save()
            product.update_rating()

            # TODO: Show a "success" message to user.
            # Refresh page to prevent duplicate submission
            return HttpResponseRedirect('.')

    else:
        if product.has_bought_by_user(request.user):
            try:
                rating = request.user.rating_set.get(product=product)
            except Rating.DoesNotExist:
                rating = Rating(product=product)
            rating_form = RatingForm(instance=rating)
        else:
            rating_form = None

    dictionary = {'product': product,
                  'rating_form': rating_form}
    if product.off_shelf:
        return render(request, 'product/off-shelf.html', dictionary, status=404)
    else:
        return render(request, 'product/detail.html', dictionary)
