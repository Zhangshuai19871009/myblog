from django import template
from django.contrib.contenttypes.models import ContentType
from django.db.models import ObjectDoesNotExist
from ..models import ReadNum

register = template.Library()

@register.simple_tag
def get_read_num(obj):
    try:
        content_type = ContentType.objects.get_for_model(obj)
        readNum = ReadNum.objects.get(content_type=content_type, object_id=obj.pk)
        return readNum.read_num
    except ObjectDoesNotExist:
        return 0
