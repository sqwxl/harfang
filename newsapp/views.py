from django.core.paginator import Paginator
from django.template.response import TemplateResponse

from newsapp.models import NewsItem

from .utils import for_htmx


def get_page_by_request(request, queryset, paginate_by=10):
    return Paginator(queryset, per_page=paginate_by).get_page(request.GET.get("page"))


@for_htmx(use_block_from_params=True)
def index(request):
    return TemplateResponse(
        request,
        "newsapp/index.html",
        {
            "page_obj": get_page_by_request(request, NewsItem.objects.all()),
        },
    )


def article(request, pk):
    return TemplateResponse(
        request,
        "newsapp/article.html",
        {
            "article": NewsItem.objects.get(pk=pk),
        },
    )
