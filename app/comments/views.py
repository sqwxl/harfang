from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views.decorators.http import require_GET, require_POST
from django_htmx.http import reswap, retarget, trigger_client_event

from .forms import CommentForm
from .models import Comment


def enforce_comment_moderation(request, comment):
    if request.user != comment.user and not request.user.has_perm(
        "comments.can_moderate"
    ):
        raise PermissionDenied


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

        return trigger_client_event(response, "commentCreated")

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
def edit(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    try:
        enforce_comment_moderation(request, comment)
    except PermissionDenied:
        # TODO flash user
        return HttpResponseRedirect(comment.get_post_url())

    form = CommentForm(instance=comment)

    if request.htmx:
        hx_attrs = {
            # form should replace itself with the comment body
            "target": f"#comment-{comment.pk}-body",
            "select": f"#comment-{comment.pk}-body",
            "push-url": "false",
        }
        return TemplateResponse(
            request,
            "comments/form.html",
            {
                "form": form,
                "form_id": f"comment-{pk}-edit-form",
                "action": reverse("comments:update", kwargs={"pk": pk}),
                "hx_attrs": hx_attrs,
                "can_cancel": True,
            },
        )
    return TemplateResponse(
        request,
        "comments/edit.html",
        {
            "form": form,
            "page_title": _("Edit Comment"),
        },
    )


@login_required
@require_POST
def update(request, pk):
    comment = get_object_or_404(Comment, pk=pk)

    try:
        enforce_comment_moderation(request, comment)
    except PermissionDenied:
        # TODO flash user
        return HttpResponseRedirect(comment.get_post_url())

    form = CommentForm(request.POST, instance=comment)

    if request.htmx:
        return update_htmx(request, form)

    if form.is_valid() and form.has_changed():
        comment = form.save(commit=False)
        comment.is_edited = True
        comment.save()
        return HttpResponseRedirect(comment.get_post_url())

    return TemplateResponse(
        request,
        "comments/edit.html",
        {
            "form": form,
            "page_title": _("Edit Comment"),
        },
    )


def update_htmx(request, form):
    if form.is_valid() and form.has_changed:
        comment = form.save(commit=False)
        comment.is_edited = True
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

        return trigger_client_event(response, "commentUpdated")

    # replace the form fields with the errors
    print(form.errors)
    return reswap(
        retarget(
            TemplateResponse(
                request,
                "comments/form.html#fields",
                {"form": form},
            ),
            request.htmx.trigger + ">#fields",
        ),
        "innerHTML",
    )


@login_required
@require_GET
def reply(request, parent_id):
    parent = get_object_or_404(Comment, id=parent_id)
    form = CommentForm(initial={"parent": parent})

    if request.htmx:
        hx_attrs = {
            # form should replace itself with the comment
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
def delete(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    try:
        enforce_comment_moderation(request, comment)
    except PermissionDenied:
        # TODO flash user
        return HttpResponseRedirect(comment.get_post_url())

    comment.is_removed = True
    comment.save()

    if request.htmx:
        return TemplateResponse(
            request, "comments/detail.html", {"comment": comment}
        )

    return HttpResponseRedirect(comment.get_post_url())


@login_required
def restore(request, pk):
    comment = get_object_or_404(Comment, pk=pk)

    if not request.user.is_moderator:
        # TODO flash user
        return HttpResponseRedirect(comment.get_post_url())

    comment.is_removed = False
    comment.save()

    if request.htmx:
        return TemplateResponse(
            request, "comments/detail.html", {"comment": comment}
        )

    return HttpResponseRedirect(comment.get_post_url())
