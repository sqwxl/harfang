from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.urls import reverse

from app.utils import get_page_by_request
from app.utils.shortcuts import get_content_objects_or_404, get_content_type_or_404

from .forms import CommentForm
from .models import Comment


def tree(request, app_name, model_name, object_id):
    content_type = get_content_type_or_404(app_name, model_name)
    return TemplateResponse(
        request,
        "comments/tree.html",
        {
            "page_obj": get_page_by_request(
                request, Comment.objects.filter(content_type=content_type, object_pk=object_id)
            ),
        },
    )


def create(request, app_label, model_name, object_id):
    content_type, target_object = get_content_objects_or_404(app_label, model_name, object_id)
    form = CommentForm(request.POST)

    if request.method == "POST" and form.is_valid():
        reply = form.get_comment_object()
        reply.user = request.user
        reply.content_type = content_type
        reply.object_pk = object_id
        reply.save()
        return HttpResponseRedirect(target_object.get_absolute_url())  # type: ignore

    return TemplateResponse(request, "comments/create.html", {"form": form})


def update(request, pk):
    reply = get_object_or_404(Comment, pk=pk)
    form = CommentForm(request.POST)
    if request.method == "POST" and form.is_valid():
        reply = form.get_comment_object()
        reply.user = request.user
        reply.save()
        return HttpResponseRedirect(reverse("comments:reply", args=(reply.pk,)))

    return TemplateResponse(
        request,
        "comments/update.html",
        {
            "reply": reply,
            "form": form,
        },
    )


# TODO  this should be a POST; don't actually delete the comment, just mark it as deleted
# might be redundant with django_comments' delete view, check that
def delete(request, pk):
    reply = get_object_or_404(Comment, pk=pk)
    if request.method == "POST":
        reply.delete()
        return HttpResponseRedirect(reverse("comments:reply", args=(reply.pk,)))

    return TemplateResponse(
        request,
        "comments/delete.html",
        {
            "reply": reply,
        },
    )


def reply(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    form = CommentForm(request.POST)
    if request.method == "POST" and form.is_valid():
        comment = form.get_comment_object()
        comment.user = request.user
        comment.parent = comment  # type: ignore
        comment.save()
        # TODO implement `next` in the form
        return HttpResponseRedirect(request.next or comment.get_absolute_url())
    return TemplateResponse(
        request,
        "comments/reply.html",
        {
            "parent": comment,
            "form": form,
        },
    )
