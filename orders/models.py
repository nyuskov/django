from django.db import models
from django.utils.translation import gettext as _


class Order(models.Model):
    first_name: models.CharField = models.CharField(
        max_length=50, verbose_name=_("First name")
    )
    last_name: models.CharField = models.CharField(
        max_length=50, verbose_name=_("Last name")
    )
    email: models.EmailField = models.EmailField(verbose_name=_("Email"))
    address: models.CharField = models.CharField(
        max_length=250, verbose_name=_("Address")
    )
    postal_code: models.CharField = models.CharField(
        max_length=20, verbose_name=_("Postal code")
    )
    city: models.CharField = models.CharField(
        max_length=100, verbose_name=_("City")
    )
    created: models.DateTimeField = models.DateTimeField(
        auto_now_add=True, verbose_name=_("Creation date")
    )
    updated: models.DateTimeField = models.DateTimeField(
        auto_now=True, verbose_name=_("Update date")
    )
    paid: models.BooleanField = models.BooleanField(
        default=False, verbose_name=_("Paid")
    )

    class Meta:
        ordering = ["-created"]
        indexes = [
            models.Index(fields=["-created"]),
        ]
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")

    def __str__(self):
        return f"{_("Order")} {self.id}"

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order: models.ForeignKey = models.ForeignKey(
        Order, related_name="items", on_delete=models.CASCADE,
        verbose_name=_("Order"),
    )
    product: models.ForeignKey = models.ForeignKey(
        "shop.Product", related_name="order_items", on_delete=models.CASCADE,
        verbose_name=_("Product"),
    )
    price: models.DecimalField = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name=_("Price"),
    )
    quantity: models.PositiveIntegerField = models.PositiveIntegerField(
        default=1, verbose_name=_("Quantity"),
    )

    class Meta:
        verbose_name = _("Order item")
        verbose_name_plural = _("Order items")

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity
