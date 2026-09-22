from django.contrib import admin

from .models import (
    Brand,
    Category,
    Product,
    ProductImage,
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "is_active",
        "created_at",
    )

    list_filter = (
        "is_active",
    )

    search_fields = (
        "name",
    )

    prepopulated_fields = {
        "slug": ("name",),
    }


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "is_active",
        "created_at",
    )

    list_filter = (
        "is_active",
    )

    search_fields = (
        "name",
    )

    prepopulated_fields = {
        "slug": ("name",),
    }


class ProductImageInline(admin.TabularInline):

    model = ProductImage

    extra = 2

    fields = (
        "image",
        "alt_text",
        "display_order",
        "is_primary",
    )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "sku",
        "category",
        "brand",
        "price",
        "is_on_sale",
        "is_featured",
        "is_active",
        "created_at",
    )

    list_filter = (
        "category",
        "brand",
        "is_active",
        "is_featured",
    )

    search_fields = (
        "name",
        "sku",
        "description",
    )

    prepopulated_fields = {
        "slug": ("name",),
    }

    readonly_fields = (
        "rating",
        "review_count",
    )

    inlines = [
        ProductImageInline,
    ]