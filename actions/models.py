from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext as _


class Action(models.Model):
    class Meta:
        indexes = [
            models.Index(fields=["-created"]),
            models.Index(fields=["target_ct", "target_id"]),
        ]
        ordering = ["-created"]
        verbose_name = _("Action")
        verbose_name_plural = _("Actions")

    user: models.ForeignKey = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="actions",
        on_delete=models.CASCADE,
        verbose_name=_("User"),
    )
    verb: models.CharField = models.CharField(
        max_length=255, verbose_name=_("Action")
    )
    created: models.DateTimeField = models.DateTimeField(
        auto_now_add=True, verbose_name=_("Creation date")
    )
    target_ct: models.ForeignKey = models.ForeignKey(
        ContentType,
        blank=True,
        null=True,
        related_name="target_obj",
        on_delete=models.CASCADE,
        verbose_name=_("Target content type"),
    )
    target_id: models.PositiveIntegerField = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name=_("Target object id"),
    )
    target: GenericForeignKey = GenericForeignKey("target_ct", "target_id")
