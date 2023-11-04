from django.contrib.contenttypes.models import ContentType
from django.http import Http404
from django.shortcuts import get_object_or_404


def get_content_type_or_404(app_label, model_name):
    return get_object_or_404(ContentType, app_label=app_label, model=model_name)


def get_content_objects_or_404(app_label, model_name, object_id):
    content_type = get_content_type_or_404(app_label, model_name)
    model_class = content_type.model_class()

    if not model_class:
        raise Http404(f'No model found for "{app_label}.{model_name}"')

    target_object = get_object_or_404(model_class, pk=object_id)

    return content_type, target_object
