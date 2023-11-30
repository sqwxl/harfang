from django import template

register = template.Library()


@register.filter(name="class_name")
def class_name(obj):
    return obj.__class__.__name__


@register.simple_tag(takes_context=True)
def hx_attrs(context):
    """Returns a string of 'hx-*' attributes from a context dict named 'hx_attrs'
    keys must be either full htmx attributes or the suffix of an htmx attributes
    (e.g. "hx-confirm" or "confirm")"""
    if attrs := context.get("hx_attrs"):
        rv = []
        for k, v in attrs.items():
            attr = k if k.startswith("hx") else f"hx-{k}"
            attr = attr.replace("_", "-")
            rv.append(f"{attr}={v}")

        return " ".join(rv)
