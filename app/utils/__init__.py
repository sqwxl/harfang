from django.core.paginator import Paginator
from django.db.models import QuerySet


def get_page_by_request(request, queryset: QuerySet, paginate_by=10):
    return Paginator(queryset, per_page=paginate_by).get_page(
        request.GET.get("page")
    )
