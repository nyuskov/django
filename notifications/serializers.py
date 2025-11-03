from rest_framework import serializers  # type: ignore

from .models import Notification, UserNotificationSettings, DeliveryAttempt


class DeliveryAttemptSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryAttempt
        fields = ["channel", "attempted_at", "success", "error_message"]


class NotificationSerializer(serializers.ModelSerializer):
    delivery_attempts = DeliveryAttemptSerializer(many=True, read_only=True)

    class Meta:
        model = Notification
        fields = [
            "user",
            "id",
            "title",
            "message",
            "created_at",
            "is_sent",
            "sent_at",
            "delivery_attempts",
        ]


class UserNotificationSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserNotificationSettings
        fields = [
            "email_enabled",
            "sms_enabled",
            "telegram_enabled",
            "telegram_chat_id",
            "phone_number",
            "delivery_priority",
        ]
