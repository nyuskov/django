from django.conf import settings
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext as _


class Image(models.Model):
    class Meta:
        indexes = [
            models.Index(fields=["-created"]),
        ]
        ordering = ["-created"]
        verbose_name = _("Image")
        verbose_name_plural = _("Images")

    user: models.ForeignKey = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="images_created",
        on_delete=models.CASCADE,
        verbose_name=_("User"),
    )
    title: models.CharField = models.CharField(
        max_length=200, verbose_name=_("Title")
    )
    slug: models.SlugField = models.SlugField(
        max_length=200, blank=True, verbose_name=_("Slug")
    )
    url: models.URLField = models.URLField(
        max_length=2000, verbose_name=_("URL")
    )
    image: models.ImageField = models.ImageField(
        upload_to="images/%Y/%m/%d/", verbose_name=_("Image")
    )
    description: models.TextField = models.TextField(
        blank=True, verbose_name=_("Description")
    )
    created: models.DateTimeField = models.DateTimeField(
        auto_now_add=True, verbose_name=_("Creation date")
    )

    users_like: models.ManyToManyField = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="images_liked",
        blank=True,
        verbose_name=_("Users who liked it"),
    )

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
