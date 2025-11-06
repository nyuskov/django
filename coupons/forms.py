from django import forms
from django.utils.translation import gettext as _


class CouponApplyForm(forms.Form):
    code = forms.CharField(label=_("Code"))
