from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User

# 点赞数
class LikeCount(models.Model):
    content_type = models.ForeignKey(ContentType, verbose_name='对象', on_delete=models.CASCADE)
    object_id = models.PositiveSmallIntegerField(verbose_name='ID')
    content_object = GenericForeignKey('content_type', 'object_id')

    liked_num = models.IntegerField(default=0)

class LikeRecord(models.Model):
    content_type = models.ForeignKey(ContentType, verbose_name='对象', on_delete=models.CASCADE)
    object_id = models.PositiveSmallIntegerField(verbose_name='ID')
    content_object = GenericForeignKey('content_type', 'object_id')

    user = models.ForeignKey(User, verbose_name='点赞人', on_delete=models.CASCADE)
    liked_time = models.DateTimeField(verbose_name='点赞时间', auto_now_add=True)
