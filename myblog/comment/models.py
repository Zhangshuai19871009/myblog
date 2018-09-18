from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User

# 评论
class Comment(models.Model):
    content_type = models.ForeignKey(ContentType, verbose_name='对象', on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField(verbose_name='ID')
    content_object = GenericForeignKey('content_type', 'object_id')

    text = models.TextField(verbose_name='评论内容')
    comment_time = models.DateTimeField(verbose_name='评论时间', auto_now_add=True)
    user = models.ForeignKey(User, related_name='comments', verbose_name='评论人', on_delete=models.CASCADE)

    # 最顶级的评论
    root = models.ForeignKey('self', verbose_name='最顶级的评论', related_name='root_comment', null=True, on_delete=models.CASCADE)
    # 被回复的评论的ID
    parent = models.ForeignKey('self', verbose_name='被回复评论', related_name='parent_comment', on_delete=models.CASCADE, null=True)
    reply_to = models.ForeignKey(User, related_name='replies', verbose_name='被回复人', null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.text

    class Meta:
        ordering = ['comment_time']
