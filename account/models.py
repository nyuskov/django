from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
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


class Contact(models.Model):
    class Meta:
        indexes = [
            models.Index(fields=['-created']),
        ]
        ordering = ['-created']
        verbose_name = _("Contact")
        verbose_name_plural = _("Contacts")

    user_from: models.ForeignKey = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='rel_from_set',
        on_delete=models.CASCADE,
        verbose_name=_('Follower'),
    )
    user_to: models.ForeignKey = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='rel_to_set',
        on_delete=models.CASCADE,
        verbose_name=_('Following'),
    )
    created: models.DateTimeField = models.DateTimeField(
        auto_now_add=True, verbose_name=_("Creation date"))

    def __str__(self):
        return f'{self.user_from} {_("follows")} {self.user_to}'


# Add the following field to User dynamically
user_model = get_user_model()
user_model.add_to_class(
    'following',
    models.ManyToManyField(
        'self',
        through=Contact,
        related_name='followers',
        symmetrical=False
    )
)
