from django.contrib.auth.decorators import login_required
from django.shortcuts import render
import logging

from app.http import HttpResponseNoContent
from app.metadata.scraper import scrape_metadata

logger = logging.getLogger(__name__)


@login_required
def scrape(request):
    url = request.GET.get("url")

    if not url:
        return HttpResponseNoContent()

    metadata = scrape_metadata(url)

    if metadata is None:
        return HttpResponseNoContent()

    logger.debug(metadata)

    return render(
        request, "metadata/url_preview.html", {"metadata": metadata, "url": url}
    )
