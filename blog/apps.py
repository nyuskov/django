from django.apps import AppConfig
from django.contrib.admin import AdminSite
from django.utils.translation import gettext_lazy as _


class BlogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'
    verbose_name = _('Blog')