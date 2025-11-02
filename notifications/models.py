from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext as _


class NotificationChannel(models.TextChoices):
    EMAIL = "email", _("Email")
    SMS = "sms", _("SMS")
    TELEGRAM = "telegram", _("Telegram")


class UserNotificationSettings(models.Model):
    user: models.OneToOneField = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="notification_settings",
        verbose_name=_("User"),
    )
    email_enabled: models.BooleanField = models.BooleanField(
        default=True, verbose_name=_("Email enabled")
    )
    sms_enabled: models.BooleanField = models.BooleanField(
        default=False, verbose_name=_("SMS enabled")
    )
    telegram_enabled: models.BooleanField = models.BooleanField(
        default=False, verbose_name=_("Telegram enabled")
    )
    telegram_chat_id: models.CharField = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name=_("Telegram chat id"),
    )
    phone_number: models.CharField = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name=_("Phone number"),
    )
    delivery_priority: models.JSONField = models.JSONField(
        default=list, verbose_name=_("Priority of delivery channels")
    )

    class Meta:
        verbose_name = _("Notification settings")
        verbose_name_plural = _("Notification settings")


class Notification(models.Model):
    user: models.ForeignKey = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="notifications",
        verbose_name=_("User"),
    )
    title: models.CharField = models.CharField(
        max_length=200, verbose_name=_("Title")
    )
    message: models.TextField = models.TextField(verbose_name=_("Message"))
    created_at: models.DateTimeField = models.DateTimeField(
        auto_now_add=True, verbose_name=_("Creation date")
    )
    is_sent: models.BooleanField = models.BooleanField(
        default=False, verbose_name=_("Sent")
    )
    sent_at: models.DateTimeField = models.DateTimeField(
        null=True, blank=True, verbose_name=_("Sent date")
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = _("Notification")
        verbose_name_plural = _("Notifications")


class DeliveryAttempt(models.Model):
    notification: models.ForeignKey = models.ForeignKey(
        Notification,
        on_delete=models.CASCADE,
        related_name="delivery_attempts",
    )
    channel: models.CharField = models.CharField(
        max_length=20,
        choices=NotificationChannel.choices,
    )
    attempted_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    success: models.BooleanField = models.BooleanField(default=False)
    error_message: models.TextField = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ["attempted_at"]
