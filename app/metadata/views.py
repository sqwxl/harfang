from django.shortcuts import render
from w3lib.url import canonicalize_url

from app.http import HttpResponseNoContent
from app.metadata.scraper import scrape_metadata


def scrape(request):
    if not request.user.is_authenticated:
        return HttpResponseNoContent()

    url = request.GET.get("url")

    if not url:
        return HttpResponseNoContent()

    clean = canonicalize_url(url)

    metadata = scrape_metadata(clean)

    if metadata is None:
        return HttpResponseNoContent()

    return render(request, "metadata/url_preview.html", {"metadata": metadata})
