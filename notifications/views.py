from django.utils.translation import gettext as _
from rest_framework import viewsets, status  # type: ignore
from rest_framework.decorators import action  # type: ignore
from rest_framework.response import Response  # type: ignore

from .models import Notification, UserNotificationSettings
from .services import NotificationService
from .serializers import (
    NotificationSerializer,
    UserNotificationSettingsSerializer,
)


class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    notification_service = NotificationService()

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)

    @action(detail=False, methods=["post"])
    def send(self, request):
        user = request.user
        title = request.data.get("title")
        message = request.data.get("message")

        success = self.notification_service.send_notification(
            user, title, message
        )

        if success:
            return Response({"status": _("Notification sent successfully")})
        else:
            return Response(
                {"status": _("Failed to send notification")},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class UserNotificationSettingsViewSet(viewsets.ModelViewSet):
    serializer_class = UserNotificationSettingsSerializer

    def get_queryset(self):
        return UserNotificationSettings.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
