# Generated by Django 2.0.5 on 2018-09-17 02:30

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('read_statistics', '0007_auto_20180913_1513'),
    ]

    operations = [
        migrations.AlterField(
            model_name='readdetail',
            name='date',
            field=models.DateField(default=datetime.datetime(2018, 9, 17, 2, 30, 1, 294261, tzinfo=utc), verbose_name='阅读日期'),
        ),
    ]