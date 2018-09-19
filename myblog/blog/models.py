from django.shortcuts import reverse
from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from ckeditor_uploader.fields import RichTextUploadingField
from read_statistics.models import ReadDetail

class BlogType(models.Model):
    type_name = models.CharField(verbose_name='类型', max_length=15)

    def __str__(self):
        return self.type_name

class Blog(models.Model):
    title = models.CharField(verbose_name='标题', max_length=50)
    blog_type = models.ForeignKey(BlogType, verbose_name='类型', on_delete=models.CASCADE)
    content = RichTextUploadingField(verbose_name='内容')
    author = models.ForeignKey(User, verbose_name='作者', on_delete=models.CASCADE)
    read_details = GenericRelation(ReadDetail) # 反向泛型关系
    created_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    last_updated_time = models.DateTimeField(verbose_name='最后修改时间', auto_now=True)

    # 反解析，通过对象反解析出对应的url
    def get_url(self):
        return reverse('blog_detail', kwargs={'blog_pk': self.pk})

    # 获取当前博客的发布者的email
    def get_email(self):
        return self.author.email

    def __str__(self):
        return "<Blog: %s>" % self.title

    class Meta:
        ordering = ['-created_time']
