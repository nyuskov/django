from typing import Literal
from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext as _


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


class Post(models.Model):
    class Meta:
        ordering: tuple[Literal["-publish"]] = ("-publish",)
        indexes: list[models.Index] = [
            models.Index(fields=["-publish"]),
        ]
        verbose_name: str = _("Post")
        verbose_name_plural: str = _("Posts")

    class Status(models.TextChoices):
        DRAFT = "DF", _("Draft")
        PUBLISHED = "PB", _("Published")

    objects = models.Manager()
    published = PublishedManager()
    title: models.CharField = models.CharField(
        max_length=250,
        verbose_name=_("Title"),
    )
    slug: models.SlugField = models.SlugField(
        max_length=250, verbose_name=_("Slug"), unique_for_date="publish"
    )
    body: models.TextField = models.TextField(verbose_name=_("Body"))
    publish: models.DateTimeField = models.DateTimeField(
        default=timezone.now,
        verbose_name=_("Published date"),
    )
    created: models.DateTimeField = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created date"),
    )
    updated: models.DateTimeField = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Updated date"),
    )
    status: models.CharField = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.DRAFT,
        verbose_name=_("Status"),
    )
    author: models.ForeignKey = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="blog_posts",
        verbose_name=_("Author"),
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(
            "blog:post_detail",
            args=[
                self.publish.year,
                self.publish.month,
                self.publish.day,
                self.slug,
            ],
        )


class Comment(models.Model):
    class Meta:
        ordering = ["created"]
        indexes = [
            models.Index(fields=["created"]),
        ]
        verbose_name: str = _("Comment")
        verbose_name_plural: str = _("Comments")

    post: models.ForeignKey = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name=_("Post"),
    )
    name: models.CharField = models.CharField(
        max_length=80, verbose_name=_("Name")
    )
    email: models.EmailField = models.EmailField(verbose_name=_("E-mail"))
    body: models.TextField = models.TextField(verbose_name=_("Body"))
    created: models.DateTimeField = models.DateTimeField(
        auto_now_add=True, verbose_name=_("Created date")
    )
    updated: models.DateTimeField = models.DateTimeField(
        auto_now=True, verbose_name=_("Updated date")
    )
    active: models.BooleanField = models.BooleanField(
        default=True, verbose_name=_("Status")
    )

    def __str__(self):
        return _("Comment by {name} on {post}").format(
            name=self.name, post=self.post.title
        )
