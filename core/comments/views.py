from django.contrib.contenttypes.models import ContentType
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.urls import reverse

from .forms import CommentForm
from .models import Comment


def create_view(request, app_label, model_name, object_id):
    content_type = get_object_or_404(ContentType, app_label=app_label, model=model_name)
    model_class = content_type.model_class()

    if not model_class:
        raise Http404(f'No model found for "{app_label}.{model_name}"')

    target_object = get_object_or_404(model_class, pk=object_id)
    form = CommentForm(request.POST)

    if request.method == "POST" and form.is_valid():
        comment = form.get_comment_object()
        comment.user = request.user
        comment.content_type = content_type
        comment.object_pk = object_id
        comment.save()
        return HttpResponseRedirect(target_object.get_absolute_url())  # type: ignore

    return TemplateResponse(request, "comments/form.html", {"form": form})


def reply_view(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    form = CommentForm(request.POST)
    if request.method == "POST" and form.is_valid():
        comment = form.get_comment_object()
        comment.user = request.user
        comment.parent = comment
        comment.save()
        return HttpResponseRedirect(reverse("comments:comment", args=(comment.pk,)))
    return TemplateResponse(
        request,
        "comments/reply.html",
        {
            "parent": comment,
            "form": form,
        },
    )
