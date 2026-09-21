from django.db import transaction

from .models import Cart, CartItem


SESSION_CART_KEY = "cart_id"


def get_cart(request):
    """
    Return the user's database cart or guest session cart.
    """

    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(
            user=request.user
        )

        return cart

    # Guest cart
    if not request.session.session_key:
        request.session.create()

    session_key = request.session.session_key

    cart, created = Cart.objects.get_or_create(
        session_key=session_key,
        user=None,
    )

    return cart


@transaction.atomic
def add_to_cart(request, product, quantity=1):
    cart = get_cart(request)

    item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={
            "quantity": quantity,
        },
    )

    if not created:
        item.quantity += quantity
        item.save(update_fields=["quantity", "updated_at"])

    return cart, item


@transaction.atomic
def update_cart_item(request, cart_item, quantity):
    if quantity <= 0:
        cart_item.delete()
    else:
        cart_item.quantity = quantity
        cart_item.save(
            update_fields=[
                "quantity",
                "updated_at",
            ]
        )

    return get_cart(request)


def remove_from_cart(request, cart_item):
    cart_item.delete()
    return get_cart(request)