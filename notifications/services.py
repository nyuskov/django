from datetime import datetime
import logging
import requests  # type: ignore

from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.utils.translation import gettext as _

logger = logging.getLogger(__name__)


class EmailService:
    def __init__(self):
        self.enabled = getattr(settings, "EMAIL_ENABLED", True)

    def send_notification(self, user_email, subject, message):
        if not self.enabled:
            raise Exception(_("Email service is disabled"))

        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user_email],
                fail_silently=False,
            )
            logger.info("Email sent successfully to %s" % user_email)
            return True
        except Exception as e:
            logger.error(
                "Failed to send email to %s: %s" % (user_email, str(e))
            )
            raise Exception(f"{_('Email sending failed')}: {str(e)}")


class SMSService:
    def __init__(self):
        self.enabled = getattr(settings, "SMS_ENABLED", False)
        self.api_key = getattr(settings, "SMS_API_KEY", None)

    def send_notification(self, phone_number, message):
        if not self.enabled:
            raise Exception(_("SMS service is disabled"))

        if not phone_number:
            raise Exception(_("Phone number not provided"))

        try:
            # TODO: imitation of sending SMS
            # In real realization you should use some library:
            # client = Client(settings.TWILIO_ACCOUNT_SID,
            #                 settings.TWILIO_AUTH_TOKEN)
            # message = client.messages.create(
            #     body=message,
            #     from_=settings.TWILIO_PHONE_NUMBER,
            #     to=phone_number
            # )
            logger.info("SMS sent to %s: %s..." % (phone_number, message[:50]))

            return True
        except Exception as e:
            logger.error(
                "Failed to send SMS to %s: %s" % (phone_number, str(e))
            )
            raise Exception(f"{_('SMS sending failed')}: {str(e)}")


class TelegramService:
    def __init__(self):
        self.enabled = getattr(settings, "TELEGRAM_ENABLED", False)
        self.bot_token = getattr(settings, "TELEGRAM_BOT_TOKEN", None)

    def send_notification(self, chat_id, message):
        if not self.enabled:
            raise Exception(_("Telegram service is disabled"))

        if not chat_id:
            raise Exception(_("Telegram chat ID not provided"))

        try:
            url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
            payload = {
                "chat_id": chat_id,
                "text": message,
                "parse_mode": "HTML",
            }

            response = requests.post(url, json=payload)
            response.raise_for_status()

            logger.info("Telegram message sent to chat %s" % chat_id)
            return True
        except Exception as e:
            logger.error(
                "Failed to send Telegram message to %s: %s" % (chat_id, str(e))
            )
            raise Exception(f"{_('Telegram sending failed')}: {str(e)}")


# Main service
class NotificationService:
    def __init__(self):
        self.email_service = EmailService()
        self.sms_service = SMSService()
        self.telegram_service = TelegramService()

        self.channel_services = {
            "email": self.email_service,
            "sms": self.sms_service,
            "telegram": self.telegram_service,
        }

    def _send_via_channel(self, user, channel, title, message):
        """Отправка уведомления через конкретный канал"""
        try:
            settings = user.notification_settings

            if channel == "email":
                full_message = f"{title}\n\n{message}"
                return self.email_service.send_notification(
                    user.email, title, full_message
                )

            elif channel == "sms":
                sms_message = f"{title}: {message}"[
                    :160
                ]  # Ограничение длины SMS
                return self.sms_service.send_notification(
                    settings.phone_number, sms_message
                )

            elif channel == "telegram":
                telegram_message = f"<b>{title}</b>\n\n{message}"
                return self.telegram_service.send_notification(
                    settings.telegram_chat_id, telegram_message
                )

            else:
                raise ValueError(f"{_('Unknown channel')}: {channel}")

        except User.notification_settings.RelatedObjectDoesNotExist:
            if channel == "email":
                full_message = f"{title}\n\n{message}"
                return self.email_service.send_notification(
                    user.email, title, full_message
                )
            else:
                raise Exception(
                    f"{_('Notification settings not found for user')} {
                        user.username}"
                )

    def get_user_channels(self, user):
        """Получить доступные каналы пользователя в порядке приоритета"""
        try:
            settings = user.notification_settings
            if settings.delivery_priority:
                return settings.delivery_priority

            # Дефолтный порядок приоритета
            default_priority = ["telegram", "email", "sms"]
            return [
                channel
                for channel in default_priority
                if getattr(settings, f"{channel}_enabled", False)
            ]
        except User.notification_settings.RelatedObjectDoesNotExist:
            # Если настройки не созданы, используем только email
            return ["email"]

    def send_notification(self, user, title, message):
        """Основной метод отправки уведомления с отказоустойчивостью"""
        from .models import Notification, DeliveryAttempt

        # Создаём запись уведомления
        notification = Notification.objects.create(
            user=user, title=title, message=message
        )

        # Получаем каналы пользователя
        channels = self.get_user_channels(user)

        if not channels:
            logger.error(
                "No notification channels available for user %s" % user.username
            )
            return False

        # Пытаемся отправить через доступные каналы
        success = False
        last_error = None

        for channel in channels:
            try:
                attempt = DeliveryAttempt.objects.create(
                    notification=notification, channel=channel
                )

                channel_success = self._send_via_channel(
                    user, channel, title, message
                )

                attempt.success = channel_success
                attempt.save()

                if channel_success:
                    success = True
                    logger.info(
                        "Notification sent successfully via %s to user %s"
                        % (
                            channel,
                            user.username,
                        )
                    )
                    break

            except Exception as e:
                logger.error(
                    "Failed to send via %s for user %s: %s"
                    % (channel, user.username, str(e))
                )
                attempt.error_message = str(e)
                attempt.save()
                last_error = str(e)

        # Обновляем статус уведомления
        notification.is_sent = success
        notification.sent_at = datetime.now() if success else None
        notification.save()

        if not success:
            logger.error(
                "All delivery attempts failed for user %s. Last error: %s"
                % (user.username, last_error)
            )

        return success
