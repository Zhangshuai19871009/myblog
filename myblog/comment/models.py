from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User

# Create your models here.
class Comment(models.Model):
    content_type = models.ForeignKey(ContentType, verbose_name='对象', on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField(verbose_name='ID')
    content_object = GenericForeignKey('content_type', 'object_id')

    text = models.TextField(verbose_name='评论内容')
    comment_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, verbose_name='评论人', on_delete=models.CASCADE)