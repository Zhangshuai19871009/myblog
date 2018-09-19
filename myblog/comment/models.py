import threading
from django.db import models
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.shortcuts import render

# 多线程-发送邮件
class SendMail(threading.Thread):
    # 初始化参数
    def __init__(self, subject, text, email, fail_silently=False):
        self.subject = subject
        self.text = text
        self.email = email
        self.fail_silently = fail_silently
        threading.Thread.__init__(self)

    # 发送邮件
    def run(self):
        send_mail(
            self.subject,
            '',
            settings.EMAIL_HOST_USER,
            [self.email],
            fail_silently=self.fail_silently,
            html_message=self.text,
        )

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

    # 发送邮件
    def send_mail(self):
        if self.parent is None:
            # 评论博客
            subject = '有人评论你的博客'
            email = self.content_object.get_email()
        else:
            # 回复评论
            subject = '有人回复你的评论'
            email = self.reply_to.email
        if email != '':
            context = {}
            context['comment_text'] = self.text
            context['url'] = self.content_object.get_url()
            text = render(None, 'comment/send_mail.html', context).content.decode('utf-8')
            send_mail = SendMail(subject, text, email)
            # 开启多线程
            send_mail.start()

    def __str__(self):
        return self.text

    class Meta:
        ordering = ['comment_time']
