from django.db import models


class Inventory(models.Model):

    product = models.OneToOneField(
        "catalog.Product",
        on_delete=models.CASCADE,
        related_name="inventory",
    )

    quantity = models.PositiveIntegerField(
        default=0,
    )

    reserved_quantity = models.PositiveIntegerField(
        default=0,
    )

    reorder_level = models.PositiveIntegerField(
        default=5,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        verbose_name_plural = "Inventory"

    def __str__(self):
        return f"{self.product.name} - {self.available_quantity}"

    @property
    def available_quantity(self):
        return max(
            self.quantity - self.reserved_quantity,
            0,
        )

    @property
    def is_in_stock(self):
        return self.available_quantity > 0

    @property
    def is_low_stock(self):
        return (
            self.available_quantity <= self.reorder_level
        )