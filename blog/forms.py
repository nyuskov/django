from django import forms
from django.utils.translation import gettext as _

from .models import Comment


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25, label=_("Name"))
    email = forms.EmailField(label=_("From"))
    to = forms.EmailField(label=_("To"))
    comments = forms.CharField(
        required=False, widget=forms.Textarea, label=_("Comment")
    )


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["name", "email", "body"]


class SearchForm(forms.Form):
    query = forms.CharField(label=_("Query"))
