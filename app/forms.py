from django import forms



class AppModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        kwargs["label_suffix"] = ""
        super().__init__(*args, **kwargs)
