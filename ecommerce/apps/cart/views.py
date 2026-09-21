from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from apps.catalog.models import Product

from .models import CartItem
from .services import (
    add_to_cart,
    get_cart,
    remove_from_cart,
    update_cart_item,
)


def cart_detail(request):
    cart = get_cart(request)

    cart_items = (
        cart.items
        .select_related("product", "product__category")
        .all()
    )

    return render(
        request,
        "cart/cart.html",
        {
            "cart": cart,
            "cart_items": cart_items,
        },
    )


def add_to_cart_view(request, product_id):

    if request.method != "POST":
        return JsonResponse(
            {
                "success": False,
                "message": "POST request required.",
            },
            status=405,
        )

    product = get_object_or_404(
        Product,
        pk=product_id,
        is_active=True,
    )

    try:
        quantity = int(
            request.POST.get("quantity", 1)
        )
    except (TypeError, ValueError):
        quantity = 1

    try:

        cart, item = add_to_cart(
            request,
            product,
            quantity,
        )

    except ValueError as exc:

        return JsonResponse(
            {
                "success": False,
                "message": str(exc),
            },
            status=400,
        )

    return JsonResponse(
        {
            "success": True,
            "message": f"{product.name} added to cart.",
            "item_count": cart.item_count,
            "subtotal": f"{cart.subtotal:.2f}",
            "product": product.name,
            "quantity": item.quantity,
        }
    )


def update_cart_item_view(request, item_id):

    if request.method != "POST":
        return JsonResponse(
            {
                "success": False,
                "message": "POST request required.",
            },
            status=405,
        )

    cart = get_cart(request)

    item = get_object_or_404(
        CartItem,
        pk=item_id,
        cart=cart,
    )

    try:
        quantity = int(
            request.POST.get("quantity", 1)
        )
    except (TypeError, ValueError):

        return JsonResponse(
            {
                "success": False,
                "message": "Invalid quantity.",
            },
            status=400,
        )

    try:

        cart = update_cart_item(
            request,
            item,
            quantity,
        )

    except ValueError as exc:

        return JsonResponse(
            {
                "success": False,
                "message": str(exc),
            },
            status=400,
        )

    return JsonResponse(
        {
            "success": True,
            "item_count": cart.item_count,
            "subtotal": f"{cart.subtotal:.2f}",
        }
    )


def remove_cart_item(request, item_id):

    if request.method != "POST":
        return JsonResponse(
            {
                "success": False,
                "message": "POST request required.",
            },
            status=405,
        )

    cart = get_cart(request)

    item = get_object_or_404(
        CartItem,
        pk=item_id,
        cart=cart,
    )

    remove_from_cart(
        request,
        item,
    )

    cart = get_cart(request)

    return JsonResponse(
        {
            "success": True,
            "item_count": cart.item_count,
            "subtotal": f"{cart.subtotal:.2f}",
        }
    )


def clear_cart(request):

    if request.method != "POST":
        return JsonResponse(
            {
                "success": False,
                "message": "POST request required.",
            },
            status=405,
        )

    cart = get_cart(request)

    cart.clear()

    return JsonResponse(
        {
            "success": True,
            "item_count": 0,
            "subtotal": "0.00",
        }
    )