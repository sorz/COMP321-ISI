from .models import Cart


def get_or_create_cart(request):
    """Return user's shopping cart object if authenticated or None."""
    if not request.user.is_authenticated():
        return
    cart, created = Cart.objects.get_or_create(owner=request.user, order=None)
    return cart