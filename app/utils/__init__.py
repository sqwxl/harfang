from django.conf import settings
from django.core.paginator import Paginator
from django.db.models import QuerySet


def get_page(
    request, queryset: QuerySet, paginate_by=settings.DEFAULT_PAGE_SIZE
):
    return Paginator(queryset, per_page=paginate_by).get_page(
        request.GET.get("page")
    )
