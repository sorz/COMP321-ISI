from .models import Cart


def get_or_create_cart(request):
    """Return user's shopping cart object if authenticated or None."""
    if not request.user.is_authenticated():
        return
    try:
        return request.user.cart
    except Cart.DoesNotExist:
        return Cart.objects.create(owner=request.user)
