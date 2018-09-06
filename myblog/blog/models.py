from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.
class BlogType(models.Model):
    type_name = models.CharField(verbose_name='类型', max_length=15)

    def __str__(self):
        return self.type_name

class Blog(models.Model):
    title = models.CharField(verbose_name='标题', max_length=50)
    blog_type = models.ForeignKey(BlogType, verbose_name='类型', on_delete=models.CASCADE)
    content = RichTextUploadingField(verbose_name='内容')
    author = models.ForeignKey(User, verbose_name='作者', on_delete=models.CASCADE)
    read_num = models.IntegerField(verbose_name='阅读数', default=0)
    created_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    last_updated_time = models.DateTimeField(verbose_name='最后修改时间', auto_now=True)

    def __str__(self):
        return "<Blog: %s>" % self.title

    class Meta:
        ordering = ['-created_time']
