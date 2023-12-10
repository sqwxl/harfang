import re

import nh3
from django.conf import settings
from markdown import markdown

URL_SCHEMES = {"https", "http"}

TAGS = {
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "b",
    "i",
    "strong",
    "em",
    "tt",
    "p",
    "br",
    "span",
    "div",
    "blockquote",
    "code",
    "pre",
    "hr",
    "ul",
    "ol",
    "li",
    "dd",
    "dt",
    "img",
    "a",
    "sub",
    "sup",
}

ATTRIBUTES = {
    "*": {"id", "class", "style"},
    "a": {"href", "alt", "title"},
    "img": {"src", "alt", "width", "height"},
}


def sanitize_md_links(text):
    schemes = "|".join(URL_SCHEMES)
    pattern = rf"\[(.+)\]\((?!({schemes})).*:(.+)\)"
    return re.sub(pattern, "[\\1](\\3)", text, flags=re.IGNORECASE)


def sanitize_html(html):
    return nh3.clean(
        html,
        tags=TAGS,
        attributes=ATTRIBUTES,
        url_schemes=URL_SCHEMES,
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
