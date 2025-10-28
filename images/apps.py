from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ImagesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "images"
    verbose_name = _("Images")

    def ready(self):
        # import signal handlers
        import images.signals
