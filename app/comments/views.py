from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext as _
from django.views.decorators.http import require_GET, require_POST
from django_htmx.http import reswap, retarget, trigger_client_event

from app.utils.decorators import AccessDecorators

from .forms import CommentForm
from .models import Comment, CommentVote

can = AccessDecorators(Comment)


@login_required
def create(request):
    if request.method == "POST":
        if request.htmx:
            return create_htmx(request)

        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.save()
            return HttpResponseRedirect(comment.get_post_url())

    form = CommentForm()

    return TemplateResponse(
        request,
        "comments/form.html",
        {
            "form": form,
            "page_title": _("Post Comment"),
            "submit_text": _("Post"),
        },
    )


def create_htmx(request):
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = request.user
        comment.save()
        if request.POST.get("tree"):
            response = TemplateResponse(
                request,
                "comments/partials/tree.html#list-item",
                {"node": comment, "tree_context": True},
            )
        else:
            response = TemplateResponse(
                request,
                "comments/partials/article.html",
                {"comment": comment},
            )
        if event := request.POST.get("commentFormEvent"):
            trigger_client_event(response, event)
        return response

    # replace the form fields with the errors
    return reswap(
        retarget(
            TemplateResponse(
                request,
                "comments/form.html#fields",
                {"form": form},
            ),
            f"#{request.htmx.trigger}>#fields",
        ),
        "outerHTML",
    )


@login_required
@require_GET
def create_reply(request, parent_id):
    parent = get_object_or_404(Comment, id=parent_id)
    form = CommentForm(initial={"parent": parent})

    if request.htmx:
        hx_attrs = {
            "target": f"#comment-{parent_id}-children",
            "swap": "afterbegin",
        }
        return TemplateResponse(
            request,
            "comments/form.html#form",
            {
                "form_id": f"comment-{parent_id}-reply-form",
                "form": form,
                "hx_attrs": hx_attrs,
                "can_cancel": True,
                "submit_text": _("Reply"),
            },
        )
    else:
        return TemplateResponse(
            request,
            "comments/reply.html",
            {
                "form": form,
                "page_title": _("Reply to {username}").format(
                    username=parent.user
                ),
                "submit_text": _("Reply"),
            },
        )


def detail(request, pk):
    comment = get_object_or_404(Comment, pk=pk)

    if request.user.is_authenticated:
        form = CommentForm(initial={"parent": comment})
    else:
        form = None

    return TemplateResponse(
        request,
        "comments/detail.html",
        {
            "comment": comment,
            "form": form,
            "page_title": _("{username}'s comment").format(
                username=comment.user
            ),
        },
    )


@login_required
@can.edit
def update(request, pk):
    if request.method == "POST":
        return _update_post(request, pk)
    return _update_get(request, pk)


@require_GET
def _update_get(request, pk):
    comment = get_object_or_404(Comment, pk=pk)

    form = CommentForm(instance=comment)

    if request.htmx:
        hx_attrs = {
            "target": f"#comment-{comment.pk}-body",
            "select": f"#comment-{comment.pk}-body",
        }
        return TemplateResponse(
            request,
            "comments/form.html#form",
            {
                "form_id": f"comment-{comment.pk}-edit-form",
                "form": form,
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


@require_POST
def _update_post(request, pk):
    comment = get_object_or_404(Comment, pk=pk)

    form = CommentForm(request.POST, instance=comment)

    if request.htmx:
        return _update_post_htmx(request, form)

    if form.is_valid() and form.has_changed():
        comment = form.save(commit=False)
        comment.is_edited = True
        comment.save()
        return HttpResponseRedirect(comment.get_post_url())

    return TemplateResponse(
        request,
        "comments/form.html",
        {
            "form": form,
            "page_title": _("Edit Comment"),
        },
    )


def _update_post_htmx(request, form):
    if form.is_valid() and form.has_changed():
        comment = form.save(commit=False)
        comment.is_edited = True
        comment.save()
        if request.POST.get("tree"):
            response = TemplateResponse(
                request,
                "comments/partials/tree.html#list-item",
                {"node": comment, "tree_context": True},
            )
        else:
            response = TemplateResponse(
                request,
                "comments/partials/article.html",
                {"comment": comment},
            )

        if event := request.POST.get("commentFormEvent"):
            trigger_client_event(response, event)
        return response

    # replace the form fields with the errors
    response = retarget(
        TemplateResponse(
            request,
            "comments/form.html#form",
            {"form": form},
        ),
        f"#{request.htmx.trigger}>#fields",
    )

    response["HX-Reselect"] = "#fields"

    return response


@login_required
@can.delete
def delete(request, pk):
    comment = get_object_or_404(Comment, pk=pk)

    if request.htmx:
        # delete regardless of method used
        # (confirm dialog is issued on the client-side)
        comment.is_removed = True
        comment.save()
        return TemplateResponse(
            request, "comments/partials/article.html", {"comment": comment}
        )

    if request.method == "POST":
        comment.is_removed = True
        comment.save()
        return HttpResponseRedirect(comment.get_post_url())

    return TemplateResponse(
        request,
        "comments/delete.html",
        {
            "comment": comment,
            "page_title": _("Delete Comment"),
            "submit_text": _("Confirm"),
        },
    )


@login_required
@can.restore
def restore(request, pk):
    # restore regardless of method used (no confirm)
    comment = get_object_or_404(Comment, pk=pk)

    comment.is_removed = False
    comment.save()

    if request.htmx:
        return TemplateResponse(
            request, "comments/partials/article.html", {"comment": comment}
        )

    return HttpResponseRedirect(comment.get_post_url())


@login_required
@require_POST
def vote(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    try:
        vote = comment.votes.get(user=request.user)
        vote.delete()
        comment.has_voted = False
    except CommentVote.DoesNotExist:
        CommentVote(
            user=request.user, comment=comment, submit_date=timezone.now()
        ).save()
        comment.has_voted = True

    comment.refresh_from_db()

    if request.htmx:
        return TemplateResponse(
            request,
            "partials/vote_form.html",
            {"item": comment},
        )
    else:
        return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))
