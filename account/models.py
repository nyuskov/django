from django.db import models
from django.conf import settings
from django.utils.translation import gettext as _


class Profile(models.Model):
    class Meta:
        verbose_name = _("Profile")
        verbose_name_plural = _("Profiles")

    user: models.OneToOneField = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        verbose_name=_("User"),
    )
    date_of_birth: models.DateField = models.DateField(
        blank=True, null=True, verbose_name=_("Date of birth"))
    photo: models.ImageField = models.ImageField(
        upload_to="users/%Y/%m/%d/", blank=True, verbose_name=_("Photo")
    )
    styles: models.FileField = models.FileField(
        upload_to="styles/%Y/%m/%d/",
        blank=True,
        verbose_name=_("CSS styles"),
    )

    def __str__(self):
        return f"{_("Profile of")} {self.user.username}"
