from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count, F
from django.shortcuts import render

from apps.catalog.models import Product
# from apps.orders.models import Order
from apps.accounts.models import User


@login_required
def dashboard(request):

    # --------------------------------------------------
    # PRODUCTS
    # --------------------------------------------------

    total_products = Product.objects.filter(
        is_active=True
    ).count()


    # --------------------------------------------------
    # CUSTOMERS
    # --------------------------------------------------

    total_customers = User.objects.filter(
        role=User.Role.CUSTOMER
    ).count()


    # --------------------------------------------------
    # ORDERS
    # --------------------------------------------------

    total_orders = Order.objects.count()

    pending_orders = Order.objects.filter(
        status=Order.Status.PENDING
    ).count()

    processing_orders = Order.objects.filter(
        status=Order.Status.PROCESSING
    ).count()

    delivered_orders = Order.objects.filter(
        status=Order.Status.DELIVERED
    ).count()


    # --------------------------------------------------
    # REVENUE
    # --------------------------------------------------

    revenue = (
        Order.objects
        .filter(
            payment_status=Order.PaymentStatus.PAID
        )
        .aggregate(
            total=Sum("total")
        )
        ["total"]
        or Decimal("0.00")
    )


    # --------------------------------------------------
    # RECENT ORDERS
    # --------------------------------------------------

    recent_orders = (
        Order.objects
        .select_related("user")
        .order_by("-created_at")[:8]
    )


    # --------------------------------------------------
    # LOW STOCK
    # --------------------------------------------------

    low_stock_products = (
        Product.objects
        .filter(
            is_active=True,
            inventory__quantity__lte=F(
                "inventory__reorder_level"
            ),
        )
        .select_related("inventory")
        .order_by(
            "inventory__quantity"
        )[:8]
    )


    # --------------------------------------------------
    # CONTEXT
    # --------------------------------------------------

    context = {

        "total_products":
            total_products,

        "total_customers":
            total_customers,

        "total_orders":
            total_orders,

        "pending_orders":
            pending_orders,

        "processing_orders":
            processing_orders,

        "delivered_orders":
            delivered_orders,

        "revenue":
            revenue,

        "recent_orders":
            recent_orders,

        "low_stock_products":
            low_stock_products,
    }


    return render(
        request,
        "core/dashboard.html",
        context,
    )