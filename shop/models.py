from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _


class Category(models.Model):
    name: models.CharField = models.CharField(
        max_length=200, verbose_name=_("Name")
    )
    slug: models.SlugField = models.SlugField(
        max_length=200, unique=True, verbose_name=_("Slug")
    )

    class Meta:
        ordering = ["name"]
        indexes = [
            models.Index(fields=["name"]),
        ]
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("shop:product_list_by_category", args=[self.slug])


class Product(models.Model):
    category: models.ForeignKey = models.ForeignKey(
        Category,
        related_name="products",
        on_delete=models.CASCADE,
        verbose_name=_("Category"),
    )
    name: models.CharField = models.CharField(
        max_length=200, verbose_name=_("Name")
    )
    slug: models.SlugField = models.SlugField(
        max_length=200, verbose_name=_("Slug")
    )
    image: models.ImageField = models.ImageField(
        upload_to="products/%Y/%m/%d",
        blank=True,
        verbose_name=_("Image"),
    )
    description: models.TextField = models.TextField(
        blank=True, verbose_name=_("Description")
    )
    price: models.DecimalField = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name=_("Price")
    )
    available: models.BooleanField = models.BooleanField(
        default=True, verbose_name=_("Availability")
    )
    created: models.DateTimeField = models.DateTimeField(
        auto_now_add=True, verbose_name=_("Creation date")
    )
    updated: models.DateTimeField = models.DateTimeField(
        auto_now=True, verbose_name=_("Update date")
    )

    class Meta:
        ordering = ["name"]
        indexes = [
            models.Index(fields=["id", "slug"]),
            models.Index(fields=["name"]),
            models.Index(fields=["-created"]),
        ]
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("shop:product_detail", args=[self.id, self.slug])
