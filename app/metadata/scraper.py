from typing import TypedDict

import extruct
import requests

from django.conf import settings
from w3lib.html import get_base_url

# ordered by priority
# TODO: support more syntaxes
SYTAXES = ["opengraph"]


class SiteData(TypedDict):
    _type: str
    title: str
    description: str
    site_name: str
    image: str


def get_opengraph_data(data):
    for item in data:
        obj_type = item.get("@type")
        if obj_type is not None:
            return SiteData(
                _type=obj_type,
                title=item.get("og:title"),
                description=item.get("og:description"),
                site_name=item.get("og:site_name"),
                image=item.get("og:image"),
            )


def get_data(data):
    for syntax in SYTAXES:
        if syntax in data:
            if syntax == "opengraph":
                return get_opengraph_data(data[syntax])


def scrape_metadata(url) -> SiteData | None:
    r = requests.get(url, timeout=settings.METADATA_SCRAPER_TIMEOUT)

    content_type = r.headers.get("Content-Type", "")
    if not content_type.startswith("text/html"):
        return None

    base_url = get_base_url(r.text, r.url)

    data = extruct.extract(
        r.text, base_url=base_url, syntaxes=SYTAXES, uniform=True
    )
    return get_data(data)
