from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone

# 阅读数量
class ReadNum(models.Model):
    read_num = models.IntegerField(verbose_name='阅读总数', default=0)

    content_type = models.ForeignKey(ContentType, verbose_name='对象', on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField(verbose_name='ID')
    content_object = GenericForeignKey('content_type', 'object_id')

# 阅读明细
class ReadDetail(models.Model):
    date = models.DateField(verbose_name='阅读日期', default=timezone.now())
    read_num = models.IntegerField(verbose_name='阅读数', default=0)

    content_type = models.ForeignKey(ContentType, verbose_name='对象', on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField(verbose_name='ID')
    content_object = GenericForeignKey('content_type', 'object_id')
