from django.forms.renderers import TemplatesSetting


class FormRenderer(TemplatesSetting):
    form_template_name = "forms/div.html"


class FormMixin:
    default_renderer = FormRenderer()
    template_name_label = "forms/label.html"
