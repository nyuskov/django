from django.core.mail import send_mail
from django.db.models import Count
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, FormView
from taggit.models import Tag  # type: ignore

from .forms import EmailPostForm, CommentForm
from .models import Post


class PostListView(ListView):
    queryset = Post.published.none()
    context_object_name = "posts"
    paginate_by = 3
    template_name = "blog/post/list.html"

    def get_context_data(self, **kwargs):
        tag_slug = self.kwargs.get("tag_slug")
        tag = None
        object_list = Post.published.all()
        if tag_slug:
            tag = get_object_or_404(Tag, slug=tag_slug)
            object_list = Post.objects.filter(tags__in=[tag])

        return super().get_context_data(
            tag=tag, object_list=object_list, **kwargs
        )


class PostCommentView(FormView):
    form_class = CommentForm
    template_name = "blog/post/comment.html"

    def post(self, request, post_id, *args, **kwargs):
        post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
        comment = None
        # A comment was posted
        form = self.form_class(data=request.POST)
        if form.is_valid():
            # Create a Comment object without saving it to the database
            comment = form.save(commit=False)
            # Assign the post to the comment
            comment.post = post
            # Save the comment to the database
            comment.save()
        return render(
            request,
            self.template_name,
            {"post": post, "form": form, "comment": comment},
        )


class PostShareView(FormView):
    form_class = EmailPostForm
    template_name = "blog/post/share.html"

    def post(self, request, post_id, *args, **kwargs):
        # Retrieve post by id
        post = get_object_or_404(
            Post,
            id=post_id,
            status=Post.Status.PUBLISHED,
        )
        sent = False

        # Form was submitted
        form = self.form_class(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = (
                f"{cd['name']} ({cd['email']}) "
                f"recommends you read {post.title}"
            )
            message = (
                f"Read {post.title} at {post_url}\n\n"
                f"{cd['name']}'s comments: {cd['comments']}"
            )
            send_mail(
                subject=subject,
                message=message,
                from_email=None,
                recipient_list=[cd["to"]],
            )
            sent = True

        context = {"post": post, "form": form, "sent": sent}

        return render(
            request,
            self.template_name,
            context,
        )


class PostDetailView(FormView):
    form_class = CommentForm
    template_name = "blog/post/detail.html"

    def get_context_data(self, **kwargs):
        post = get_object_or_404(
            Post,
            status=Post.Status.PUBLISHED,
            slug=self.kwargs.get("post"),
            publish__year=self.kwargs.get("year"),
            publish__month=self.kwargs.get("month"),
            publish__day=self.kwargs.get("day"),
        )

        # List of active comments for this post
        comments = post.comments.filter(active=True)

        # List of similar posts
        post_tags_ids = post.tags.values_list("id", flat=True)
        similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(
            id=post.id
        )
        similar_posts = similar_posts.annotate(
            same_tags=Count("tags")
        ).order_by("-same_tags", "-publish")[:4]

        return super().get_context_data(
            post=post, comments=comments, similar_posts=similar_posts, **kwargs
        )
