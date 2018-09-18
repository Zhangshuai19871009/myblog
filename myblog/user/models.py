from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, verbose_name='用户', on_delete=models.CASCADE)
    nickname = models.CharField(verbose_name='昵称', max_length=20, default='')

    def __str__(self):
        return "<Profile: %s for %s>" % (self.nickname, self.user.username)

    # 动态绑定昵称
    # 获取昵称
    def get_nickname(self):
        if Profile.objects.filter(user=self).exists():
            profile = Profile.objects.get(user=self)
            return profile.nickname
        else:
            return ''

    # 获取昵称或用户名
    def get_nickname_or_username(self):
        if Profile.objects.filter(user=self).exists():
            profile = Profile.objects.get(user=self)
            return profile.nickname
        else:
            return ''

    # 是否有昵称
    def has_nickname(self):
        return Profile.objects.filter(user=self).exists()

    User.get_nickname = get_nickname
    User.has_nickname = has_nickname
    User.get_nickname_or_username = get_nickname_or_username
