from django.contrib import admin

from .models import Inventory


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):

    list_display = (
        "product",
        "quantity",
        "reserved_quantity",
        "available_quantity",
        "reorder_level",
        "is_in_stock",
        "updated_at",
    )

    list_filter = (
        "quantity",
        "reserved_quantity",
    )

    search_fields = (
        "product__name",
        "product__sku",
    )

    readonly_fields = (
        "available_quantity",
        "is_in_stock",
        "is_low_stock",
        "updated_at",
    )