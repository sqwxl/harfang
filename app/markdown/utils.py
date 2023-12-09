import re

import bleach
from bleach_allowlist import markdown_tags, markdown_attrs
from django.conf import settings
from markdown import markdown


def sanitize_md_links(text):
    schemes = "|".join(settings.BLEACH_ALLOWED_PROTOCOLS)
    pattern = rf"\[(.+)\]\((?!({schemes})).*:(.+)\)"
    return re.sub(pattern, "[\\1](\\3)", text, flags=re.IGNORECASE)


def sanitize_html(html):
    return bleach.clean(
        html,
        tags=markdown_tags,
        attributes=markdown_attrs,
        protocols=settings.BLEACH_ALLOWED_PROTOCOLS,
        strip=True,
    )


def md_to_html(text):
    md = sanitize_md_links(text)
    html = markdown(
        md,
        extensions=settings.MARKDOWN_EXTENSIONS,
        extension_configs=settings.MARKDOWN_EXTENSION_CONFIGS,
        output_format="html",
    )
    return sanitize_html(html)
