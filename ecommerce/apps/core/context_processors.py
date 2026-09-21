from apps.cart.services import get_cart


def cart_context(request):

    cart = get_cart(request)

    return {
        "cart": cart,
        "cart_item_count": cart.item_count,
    }