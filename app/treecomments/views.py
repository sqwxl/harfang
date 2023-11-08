from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from .forms import TreeCommentForm
from .models import TreeComment


def reply(request, parent_comment_id):
    parent = get_object_or_404(TreeComment, id=parent_comment_id)
    if request.method == "POST":
        form = TreeCommentForm(request.POST)
        if form.is_valid():
            comment = form.get_comment_object()
            comment.parent = parent  # type: ignore
            comment.save()
            return HttpResponseRedirect(comment.get_content_object_url())
    else:
        form = TreeCommentForm(parent.content_object, initial={"parent": parent_comment_id})

    return TemplateResponse(
        request,
        "comments/reply.html",
        {
            "parent": parent,
            "form": form,
        },
    )


def update(request, pk):
    comment = get_object_or_404(TreeComment, pk=pk)
    if request.method == "POST":
        form = TreeCommentForm(request.POST)
        if form.is_valid() and form.has_changed():
            comment = form.get_comment_object()
            comment.save()
            return HttpResponseRedirect(comment.get_content_object_url())
    else:
        form = TreeCommentForm(comment.content_object, instance=comment)

    return TemplateResponse(
        request,
        "comments/update.html",
        {
            "form": form,
        },
    )


# def create(request, app_label, model_name, object_id):
#     content_type, target_object = get_content_objects_or_404(app_label, model_name, object_id)
#     form = CommentForm(request.POST)
#
#     if request.method == "POST" and form.is_valid():
#         reply = form.get_comment_object()
#         reply.user = request.user
#         reply.content_type = content_type
#         reply.object_pk = object_id
#         reply.save()
#         return HttpResponseRedirect(target_object.get_absolute_url())  # type: ignore
#
#     return TemplateResponse(request, "comments/create.html", {"form": form})
#
#


# TODO  this should be a POST; don't actually delete the comment, just mark it as deleted
# might be redundant with django_comments' delete view, check that
# def delete(request, pk):
#     reply = get_object_or_404(Comment, pk=pk)
#     if request.method == "POST":
#         reply.delete()
#         return HttpResponseRedirect(reverse("comments:reply", args=(reply.pk,)))
#
#     return TemplateResponse(
#         request,
#         "comments/delete.html",
#         {
#             "reply": reply,
#         },
#     )
#
#
