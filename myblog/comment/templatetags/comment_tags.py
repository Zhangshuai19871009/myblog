from django import template
from django.contrib.contenttypes.models import ContentType
from ..models import Comment
from ..forms import CommentForm

register = template.Library()

# 获取评论数
@register.simple_tag
def get_comment_count(obj):
    content_type = ContentType.objects.get_for_model(obj)
    count = Comment.objects.filter(content_type=content_type, object_id=obj.pk).count()
    return count

# 获取评论表单
@register.simple_tag
def get_comment_form(obj):
    content_type = ContentType.objects.get_for_model(obj)
    form = CommentForm(
            initial={
                'content_type': content_type.model,
                'object_id': obj.pk,
                'reply_comment_id': 0
            }
        )
    return form

# 获取博客的顶级评论列表
@register.simple_tag
def get_comment_list(obj):
    content_type = ContentType.objects.get_for_model(obj)
    comments = Comment.objects.filter(content_type=content_type, object_id=obj.pk, parent=None)
    return comments.order_by('-comment_time')
