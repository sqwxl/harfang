from django import forms

from app.form_renderer import FormMixin


class AppModelForm(FormMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        kwargs["label_suffix"] = ""
        super().__init__(*args, **kwargs)
