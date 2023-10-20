from comments.models import Comment
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from news.models import Article, NewsSite
from users.models import User

from core.utils import for_htmx, get_page_by_request


@for_htmx(use_block_from_params=True)
def news(request):
    return TemplateResponse(
        request,
        "news.html",
        {
            "page_obj": get_page_by_request(request, Article.objects.all()),
        },
    )


@for_htmx(use_block_from_params=True)
def article(request, pk):
    item = Article.objects.get(pk=pk)
    template = "article.html"

    return TemplateResponse(
        request,
        template,
        {"article": item, "submission": item},
    )


def site(request, pk):
    news_site = NewsSite.objects.get(pk=pk)
    return TemplateResponse(request, "news_site.html", {"news_site": news_site})


@for_htmx(use_block_from_params=True)
def user_comments(request, username):
    view_user = get_object_or_404(User, username=username)
    return TemplateResponse(
        request,
        "comments/list.html",
        {
            "view_user": view_user,
            "page_obj": get_page_by_request(request, Comment.objects.filter(user=view_user).order_by("-created_on")),
        },
    )
