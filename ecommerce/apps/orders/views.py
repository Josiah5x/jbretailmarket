from decimal import Decimal

from django.contrib import messages
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render

from apps.cart.services import get_cart

from .forms import CheckoutForm
from .models import Order, OrderItem


def checkout(request):

    cart = get_cart(request)

    cart_items = (
        cart.items
        .select_related("product")
        .all()
    )

    if not cart_items:
        messages.warning(
            request,
            "Your cart is empty."
        )

        return redirect("cart:detail")


    if request.method == "POST":

        form = CheckoutForm(
            request.POST
        )

        if form.is_valid():

            with transaction.atomic():

                order = form.save(
                    commit=False
                )

                if request.user.is_authenticated:
                    order.user = request.user

                order.subtotal = cart.subtotal

                # Temporary delivery fee.
                # We'll build a delivery system later.
                order.delivery_fee = Decimal(
                    "1500.00"
                )

                order.calculate_total()

                order.save()


                for cart_item in cart_items:

                    OrderItem.objects.create(

                        order=order,

                        product=cart_item.product,

                        product_name=(
                            cart_item.product.name
                        ),

                        product_sku=getattr(
                            cart_item.product,
                            "sku",
                            "",
                        ),

                        price=(
                            cart_item.product.price
                        ),

                        quantity=cart_item.quantity,
                    )


                # Empty cart
                cart.clear()


            return redirect(
                "orders:success",
                order_id=order.pk,
            )

    else:

        initial = {}

        if request.user.is_authenticated:

            initial = {
                "full_name": (
                    request.user.get_full_name()
                    or request.user.username
                ),
                "email": request.user.email,
            }

        form = CheckoutForm(
            initial=initial
        )


    return render(
        request,
        "order/checkout.html",
        {
            "form": form,
            "cart": cart,
            "cart_items": cart_items,
        },
    )


def order_success(
    request,
    order_id,
):

    order = get_object_or_404(
        Order,
        pk=order_id,
    )

    return render(
        request,
        "order/order_success.html",
        {
            "order": order,
        },
    )


def order_detail(
    request,
    order_id,
):

    order = get_object_or_404(
        Order.objects.prefetch_related(
            "items"
        ),
        pk=order_id,
    )

    if (
        order.user
        and order.user != request.user
        and not request.user.is_staff
    ):
        messages.error(
            request,
            "You cannot access this order."
        )

        return redirect(
            "catalog:product_list"
        )

    return render(
        request,
        "order/order_detail.html",
        {
            "order": order,
        },
    )