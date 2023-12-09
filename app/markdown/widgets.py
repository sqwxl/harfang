from django import forms


class MarkdownTextarea(forms.Textarea):
    template_name = "markdown/widget.html"
