from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from .forms import CommentForm
from .models import Comment


@login_required
def reply(request, parent_id):
    parent = get_object_or_404(Comment, id=parent_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.save()
            return HttpResponseRedirect(
                comment.post.get_absolute_url() + "#comment-" + str(comment.id)
            )  # type: ignore
    else:
        form = CommentForm(initial={"parent": parent})

    return TemplateResponse(
        request,
        "comments/reply.html",
        {
            "parent": parent,
            "form": form,
            "page_title": "Reply",
        },
    )


def update(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid() and form.has_changed():
            comment = form.save(commit=False)
            comment.save()
            return HttpResponseRedirect(comment.get_post_url())
    else:
        form = CommentForm(instance=comment)

    return TemplateResponse(
        request,
        "comments/edit.html",
        {
            "form": form,
        },
    )


@login_required
def delete(request, pk):
    reply = get_object_or_404(Comment, pk=pk)
    if request.method == "POST":
        post_url = reply.get_post_url()
        reply.delete()
        return HttpResponseRedirect(post_url)

    return TemplateResponse(
        request,
        "comments/delete.html",
        {
            "reply": reply,
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
