from decimal import Decimal

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext as _

from coupons.models import Coupon


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
    stripe_id: models.CharField = models.CharField(
        max_length=250, blank=True, verbose_name=_("Stripe ID"))
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
    coupon: models.ForeignKey = models.ForeignKey(
        Coupon,
        related_name='orders',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name=_("Coupon"),
    )
    discount: models.IntegerField = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name=_("Discount"),
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

    def get_total_cost_before_discount(self):
        return sum(item.get_cost() for item in self.items.all())

    def get_discount(self):
        total_cost = self.get_total_cost_before_discount()
        if self.discount:
            return total_cost * (self.discount / Decimal(100))
        return Decimal(0)

    def get_total_cost(self):
        total_cost = self.get_total_cost_before_discount()
        return total_cost - self.get_discount()

    def get_stripe_url(self):
        if not self.stripe_id:
            # no payment associated
            return ''
        if '_test_' in settings.STRIPE_SECRET_KEY:
            # Stripe path for test payments
            path = '/test/'
        else:
            # Stripe path for real payments
            path = '/'
        return f'https://dashboard.stripe.com{path}payments/{self.stripe_id}'


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
