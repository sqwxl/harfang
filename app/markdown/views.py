from django.views.decorators.http import require_POST
from django.http import HttpResponse


from app.markdown.utils import md_to_html


@require_POST
def to_html(request):
    md = request.POST["body"]

    html = md_to_html(md)

    return HttpResponse(html)
