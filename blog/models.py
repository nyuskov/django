from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _

class Post(models.Model):
    class Meta:
        ordering = ('-publish',)
        indexes = [
            models.Index(fields=['-publish']),
        ]
        verbose_name = _('Post')
        verbose_name_plural = _('Posts')

    class Status(models.TextChoices):
        DRAFT = 'DF', _('Draft')
        PUBLISH = 'PB', _('Publish')

    title = models.CharField(max_length=250, verbose_name=_('Title'))
    slug = models.SlugField(max_length=250, verbose_name=_('Slug'))
    body = models.TextField(verbose_name=_('Body'))
    publish = models.DateTimeField(
        default=timezone.now,
        verbose_name=_('Publish date'),
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.DRAFT,
        verbose_name=_('Status'),
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='blog_posts',
        verbose_name=_('Author'),
    )

    def __str__(self):
        return self.title