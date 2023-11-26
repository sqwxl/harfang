from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, reverse
from django.template.response import TemplateResponse
from django.utils.translation import gettext as _
from django.views.decorators.http import require_GET, require_POST
from django_htmx.http import reswap, retarget, trigger_client_event

from .forms import CommentForm
from .models import Comment


@login_required
@require_POST
def post(request):
    if request.htmx:
        return post_htmx(request)

    form = CommentForm(request.POST)

    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = request.user
        comment.save()
        return HttpResponseRedirect(comment.get_post_url())

    return TemplateResponse(
        request,
        "comments/create.html",
        {
            "form": form,
            "cancel_url": reverse(
                "post", kwargs={"pk": request.POST.get("post")}
            ),
            "page_title": _("Post Comment"),
        },
    )


def post_htmx(request):
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = request.user
        comment.save()
        if request.POST.get("tree"):
            response = TemplateResponse(
                request,
                "comments/tree.html#list-item",
                {"node": comment, "tree_context": True},
            )
        else:
            response = TemplateResponse(
                request,
                "comments/detail.html",
                {"comment": comment},
            )

        return trigger_client_event(response, "commentPosted")

    # replace the form fields with the errors
    return reswap(
        retarget(
            TemplateResponse(
                request,
                "comments/form.html#fields",
                {"form": form},
            ),
            request.htmx.trigger + ">#fields",
        ),
        "outerHTML",
    )


@login_required
@require_GET
def reply(request, parent_id):
    parent = get_object_or_404(Comment, id=parent_id)
    form = CommentForm(initial={"parent": parent})

    if request.htmx:
        hx_attrs = {
            # replace the inline form with the comment
            "target": "this",
            "swap": "outerHTML",
            "push_url": "false",
        }
        return TemplateResponse(
            request,
            "comments/form.html",
            {
                "form": form,
                "form_id": f"inline-form-{parent_id}",
                "hx_attrs": hx_attrs,
                "can_cancel": True,
            },
        )
    else:
        return TemplateResponse(
            request,
            "comments/reply.html",
            {
                "parent": parent,
                "form": form,
                "page_title": _("Reply to {username}").format(
                    username=parent.user.username
                ),
            },
        )


@login_required
@permission_required("comments.change_comment")
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
            "page_title": _("Edit Comment"),
        },
    )


@login_required
@permission_required("comments.can_moderate")
def delete(request, pk):
    # FIXME
    comment = get_object_or_404(Comment, pk=pk)
    if request.method == "POST":
        post_url = comment.get_post_url()
        comment.delete()
        return HttpResponseRedirect(post_url)

    return TemplateResponse(
        request,
        "comments/delete.html",
        {
            "comment": comment,
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
