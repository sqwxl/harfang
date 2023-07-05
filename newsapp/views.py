from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, UserCreationForm
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.urls import reverse

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


def about(request):
    return TemplateResponse(request, "newsapp/about.html")


def login(request):
    if request.method == "POST":
        if "register" in request.POST:
            form = UserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse("newsapp:index"))
            else:
                return TemplateResponse(
                    request, "newsapp/login.html", {"login_form": AuthenticationForm(), "register_form": form}
                )

        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data["username"], password=form.cleaned_data["password"])
            if user is not None:
                return HttpResponseRedirect(reverse("newsapp:index"))
            else:
                form.add_error(None, "Invalid username or password")
                return TemplateResponse(
                    request, "newsapp/login.html", {"login_form": form, "register_form": UserCreationForm()}
                )
        else:
            return TemplateResponse(
                request, "newsapp/login.html", {"login_form": form, "register_form": UserCreationForm()}
            )

    return TemplateResponse(
        request, "newsapp/login.html", {"login_form": AuthenticationForm(), "register_form": UserCreationForm()}
    )


def logout(request):
    logout(request)
    return HttpResponseRedirect(reverse("newsapp:index"))


def forgot(request):
    if request.method == "POST":
        # todo
        ...
    return TemplateResponse(request, "newsapp/forgot.html", {"form": PasswordResetForm()})
