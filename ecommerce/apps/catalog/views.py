from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from .models import Category, Product


def home(request):
    featured_products = (
        Product.objects
        .filter(
            is_active=True,
            is_featured=True,
        )
        .select_related("category", "brand")
        .prefetch_related("images")[:8]
    )

    latest_products = (
        Product.objects
        .filter(is_active=True)
        .select_related("category", "brand")
        .prefetch_related("images")[:8]
    )

    categories = (
        Category.objects
        .filter(is_active=True)
        .order_by("name")
    )

    return render(
        request,
        "catalog/home.html",
        {
            "featured_products": featured_products,
            "latest_products": latest_products,
            "categories": categories,
        },
    )


def product_list(request):
    products = (
        Product.objects
        .filter(is_active=True)
        .select_related("category", "brand")
        .prefetch_related("images")
    )

    categories = Category.objects.filter(is_active=True)

    # Search
    query = request.GET.get("q", "").strip()

    if query:
        products = products.filter(
            Q(name__icontains=query)
            | Q(description__icontains=query)
            | Q(sku__icontains=query)
            | Q(brand__name__icontains=query)
            | Q(category__name__icontains=query)
        )

    # Category filter
    category_slug = request.GET.get("category", "").strip()

    if category_slug:
        products = products.filter(
            category__slug=category_slug
        )

    # Sorting
    sort = request.GET.get("sort", "newest")

    if sort == "price_low":
        products = products.order_by("price")

    elif sort == "price_high":
        products = products.order_by("-price")

    elif sort == "rating":
        products = products.order_by("-rating", "-review_count")

    elif sort == "name":
        products = products.order_by("name")

    else:
        products = products.order_by("-created_at")

    # Pagination
    paginator = Paginator(products, 12)
    page_number = request.GET.get("page")

    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "catalog/product_list.html",
        {
            "products": page_obj,
            "page_obj": page_obj,
            "categories": categories,
            "query": query,
            "selected_category": category_slug,
            "selected_sort": sort,
        },
    )


def category_detail(request, slug):
    category = get_object_or_404(
        Category,
        slug=slug,
        is_active=True,
    )

    products = (
        Product.objects
        .filter(
            category=category,
            is_active=True,
        )
        .select_related("category", "brand")
        .prefetch_related("images")
    )

    paginator = Paginator(products, 12)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "catalog/category_detail.html",
        {
            "category": category,
            "products": page_obj,
            "page_obj": page_obj,
        },
    )


def product_detail(request, slug):
    product = get_object_or_404(
        Product.objects
        .select_related("category", "brand")
        .prefetch_related("images"),
        slug=slug,
        is_active=True,
    )

    related_products = (
        Product.objects
        .filter(
            category=product.category,
            is_active=True,
        )
        .exclude(pk=product.pk)
        .select_related("category", "brand")
        .prefetch_related("images")[:4]
    )

    return render(
        request,
        "catalog/product_detail.html",
        {
            "product": product,
            "related_products": related_products,
        },
    )


def product_quick_view(request, pk):
    product = get_object_or_404(
        Product.objects
        .select_related("category", "brand")
        .prefetch_related("images"),
        pk=pk,
        is_active=True,
    )

    return render(
        request,
        "catalog/_quick_view.html",
        {
            "product": product,
        },
    )