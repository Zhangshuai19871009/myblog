from django import forms
from django.contrib import auth
from django.contrib.auth.models import User

# 登录
class LoginForm(forms.Form):
    username = forms.CharField(
        label='用户名',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': '请输入用户名',
            }
        )
    )
    password = forms.CharField(
        label='密码',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': '请输入密码',
            }
        )
    )

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']

        user = auth.authenticate(username=username, password=password)
        if user is None:
            raise forms.ValidationError('用户名或密码不正确！')
        else:
            self.cleaned_data['user'] = user
        return self.cleaned_data

# 注册
class RegForm(forms.Form):
    username = forms.CharField(
        label='用户名',
        max_length=20,
        min_length=3,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': '请输入用户名',
            }
        )
    )
    email = forms.EmailField(
        label='邮箱',
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': '请输入邮箱',
            }
        )
    )
    password = forms.CharField(
        label='密码',
        min_length=6,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': '请输入密码',
            }
        )
    )
    password_again = forms.CharField(
        label='密码',
        min_length=6,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': '请再输入一次密码',
            }
        )
    )
    # 判断用户名是否存在
    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('用户名已存在！')
        return username

    # 判断用户名是否存在
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(username=email).exists():
            raise forms.ValidationError('邮箱已存在！')
        return email

    # 判断两次输入密码是否一致
    def clean_password_again(self):
        password = self.cleaned_data['password']
        password_again = self.cleaned_data['password_again']
        if password != password_again:
            raise forms.ValidationError('两次输入密码不一致！')
        return password_again
