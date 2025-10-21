from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, TemplateView, FormView

from .forms import EmailPostForm, CommentForm
from .models import Post


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = "posts"
    paginate_by = 3
    template_name = "blog/post/list.html"


class PostCommentView(TemplateView):
    def post(self, request, post_id, *args, **kwargs):
        post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
        comment = None
        # A comment was posted
        form = CommentForm(data=request.POST)
        if form.is_valid():
            # Create a Comment object without saving it to the database
            comment = form.save(commit=False)
            # Assign the post to the comment
            comment.post = post
            # Save the comment to the database
            comment.save()
        return render(
            request,
            "blog/post/comment.html",
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

    def get(self, request, year, month, day, post, *args, **kwargs):
        post = get_object_or_404(
            Post,
            status=Post.Status.PUBLISHED,
            slug=post,
            publish__year=year,
            publish__month=month,
            publish__day=day,
        )

        # List of active comments for this post
        comments = post.comments.filter(active=True)
        # Form for users to comment
        form = self.form_class()
        context = {"post": post, "comments": comments, "form": form}

        return render(
            request,
            self.template_name,
            context,
        )
