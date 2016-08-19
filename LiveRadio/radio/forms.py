# -*- coding:utf-8 -*-
from django import forms
from django.conf import settings
from django.db.models import Q
from models import User
import re


class LoginForm(forms.Form):
    '''
    登录Form
    '''
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "邮箱", "required": "required",
                                                             "id": "username", "class": "form-control"}),
                              max_length=50, error_messages={"required": "邮箱不能为空",})
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "密码", "required": "required",
                                                                 "id": "password", "class": "form-control"}),
                              max_length=20, error_messages={"required": "密码不能为空",})


class PwdForm(forms.Form):
    '''
    修改密码Form
    '''
    old_pwd = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "旧密码", "required": "required",
                                                             "id": "username", "class": "form-control"}),
                              max_length=50, error_messages={"required": "旧密码不能为空",})
    new_pwd = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "新密码", "required": "required",
                                                                 "id": "password", "class": "form-control"}),
                              max_length=20, error_messages={"required": "新密码不能为空",})
    re_new_pwd = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "确认新密码", "required": "required",
                                                                 "id": "password", "class": "form-control"}),
                              max_length=20, error_messages={"required": "新密码不能为空",})



class AddUserForm(forms.Form):
    '''
    添加用户Form
    '''
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "请输入用户密码", "required": "required",
                                                                 "id": "addpassword", "class": "form-control"}),
                              max_length=20, error_messages={"required": "密码不能为空",})
    re_password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "请确认输入用户密码", "required": "required",
                                                                 "id": "addpassword", "class": "form-control"}),
                              max_length=20, error_messages={"required": "密码不能为空",})
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "请输入用户邮箱", "required": "required",
                                                                 "id": "addemail", "class": "form-control"}),
                              max_length=20, error_messages={"required": "邮箱不能为空",})

class AddRadioForm(forms.Form):
    '''
    添加直播Form
    <th>直播标题</th>
    <th>直播任务描述</th>
        <th>频道号</th>
        <th>开始时间</th>
        <th>结束时间</th>
    title
    describe
    channel
    start_time
    over_time
    '''
    title = forms.CharField(widget=forms.TextInput(attrs={"id": "ra_title", "placeholder": "直播标题（唯一）",
                                                          "required": "required", "class": "form-control"}),
                            max_length=20, error_messages={"required": "标题不能为空",})
    description = forms.CharField(widget=forms.TextInput(attrs={"id": "ra_des", "placeholder": "直播任务描述",
                                                                "required": "required", "class": "form-control"}),
                                  max_length=20, error_messages={"required": "描述不能为空",})
    channel = forms.CharField(widget=forms.TextInput(attrs={"id": "ra_cha", "placeholder": "频道",
                                                            "required": "required", "class": "form-control"}),
                              max_length=20, error_messages={"required": "频道不能为空",})
    start_time = forms.CharField(widget=forms.TextInput(attrs={"id": "ra_start", "placeholder": "开始时间必须提前一小时输入",
                                                               "required": "required", "class": "form_datetime",
                                                               "name": "start", "value": ""}),
                                 max_length=20, error_messages={"required": "开始时间不能为空",})
    finish_time = forms.CharField(widget=forms.TextInput(attrs={"id": "ra_finish", "placeholder": "结束时间",
                                                                "required": "required", "class": "form_datetime",
                                                                "name": "start", "value": ""}),
                                  max_length=20, error_messages={"required": "结束时间不能为空",})