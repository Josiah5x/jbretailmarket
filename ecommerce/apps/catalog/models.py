from decimal import Decimal

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(
        max_length=120,
        unique=True,
    )

    slug = models.SlugField(
        max_length=140,
        unique=True,
        blank=True,
    )

    description = models.TextField(
        blank=True,
    )

    image = models.ImageField(
        upload_to="categories/",
        blank=True,
        null=True,
    )

    is_active = models.BooleanField(
        default=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            "catalog:category_detail",
            kwargs={"slug": self.slug},
        )


class Brand(models.Model):
    name = models.CharField(
        max_length=120,
        unique=True,
    )

    slug = models.SlugField(
        max_length=140,
        unique=True,
        blank=True,
    )

    logo = models.ImageField(
        upload_to="brands/",
        blank=True,
        null=True,
    )

    is_active = models.BooleanField(
        default=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)


class Product(models.Model):

    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="products",
    )

    brand = models.ForeignKey(
        Brand,
        on_delete=models.SET_NULL,
        related_name="products",
        blank=True,
        null=True,
    )

    name = models.CharField(
        max_length=200,
    )

    slug = models.SlugField(
        max_length=220,
        unique=True,
        blank=True,
    )

    sku = models.CharField(
        max_length=100,
        unique=True,
    )

    description = models.TextField(
        blank=True,
    )

    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    compare_at_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Original price before discount.",
    )

    image = models.ImageField(
        upload_to="products/",
        blank=True,
        null=True,
    )

    rating = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        default=Decimal("0.0"),
        validators=[
            MinValueValidator(0),
            MaxValueValidator(5),
        ],
    )

    review_count = models.PositiveIntegerField(
        default=0,
    )

    is_active = models.BooleanField(
        default=True,
    )

    is_featured = models.BooleanField(
        default=False,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["-created_at"]

        indexes = [
            models.Index(fields=["is_active"]),
            models.Index(fields=["category", "is_active"]),
            models.Index(fields=["is_featured", "is_active"]),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

    @property
    def is_on_sale(self):
        return (
            self.compare_at_price is not None
            and self.compare_at_price > self.price
        )

    @property
    def discount_percentage(self):
        if not self.is_on_sale:
            return 0

        discount = (
            (self.compare_at_price - self.price)
            / self.compare_at_price
        ) * 100

        return round(discount)

    def get_absolute_url(self):
        return reverse(
            "catalog:product_detail",
            kwargs={"slug": self.slug},
        )


class ProductImage(models.Model):

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="images",
    )

    image = models.ImageField(
        upload_to="products/gallery/",
    )

    alt_text = models.CharField(
        max_length=200,
        blank=True,
    )

    display_order = models.PositiveIntegerField(
        default=0,
    )

    is_primary = models.BooleanField(
        default=False,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["display_order", "id"]

    def __str__(self):
        return f"{self.product.name} - Image"