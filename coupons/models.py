from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext as _


class Coupon(models.Model):
    code: models.CharField = models.CharField(
        max_length=50, unique=True, verbose_name=_("Code")
    )
    valid_from: models.DateTimeField = models.DateTimeField(
        verbose_name=_("Valid from"),
    )
    valid_to: models.DateTimeField = models.DateTimeField(
        verbose_name=_("Valid to"),
    )
    discount: models.IntegerField = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text=_("Percentage value (0 to 100)"),
        verbose_name=_("Discount"),
    )
    active: models.BooleanField = models.BooleanField(verbose_name=_("Active"))

    class Meta:
        verbose_name = _("Coupon")
        verbose_name_plural = _("Coupons")

    def __str__(self):
        return self.code
