from django.conf import settings
from markdown import markdown


def md_to_html(text):
    return markdown(
        text,
        extensions=settings.MARKDOWN_EXTENSIONS,
        extension_configs=settings.MARKDOWN_EXTENSION_CONFIGS,
    )
