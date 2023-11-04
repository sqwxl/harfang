import copy

from django.core.paginator import Paginator
from django.db.models import QuerySet
from django.http.request import HttpRequest, QueryDict


def get_page_by_request(request, queryset: QuerySet, paginate_by=10):
    return Paginator(queryset, per_page=paginate_by).get_page(request.GET.get("page"))


def make_get_request(request: HttpRequest) -> HttpRequest:
    """
    Returns a new GET request based on passed in request.
    """
    new_request = copy.copy(request)
    new_request.POST = QueryDict()
    new_request.method = "GET"
    return new_request
