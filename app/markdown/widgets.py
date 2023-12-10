from django import forms


class MarkdownTextarea(forms.Textarea):
    template_name = "markdown/widget.html"

    def __init__(self, html=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print(html)
        self.html = html

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        if self.html:
            context["widget"]["html"] = self.html
        return context
