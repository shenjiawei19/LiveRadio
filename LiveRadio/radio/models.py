# -*- coding: utf-8 -*-
# Create your models here.
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import AbstractUser
#奇异代码-->解决date = date['date_publish'].strftime('%Y/%m文章')问题
#'ascii' codec can't encode characters in position 5-6: ordinal not in range(128)
import sys
reload(sys)
sys.setdefaultencoding('utf8')


# 用户组
class Group(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='用户组编号')
    name = models.CharField(max_length=30, verbose_name='用户组分类')

    class Meta:
        verbose_name_plural = '用户组'
        ordering = ['id']

    def __unicode__(self):
        return self.name


# 用户
# 用户-->使用Django原生用户类
# 注意在setting下添加AUTH_USER_MODEL = 'blog.User'
class User(AbstractUser):
    id = models.AutoField(primary_key=True, verbose_name='用户编号')
#    avatar = models.ImageField(upload_to='avatar/%Y/%m', default='avatar/default.png', max_length=200, blank=True, null=True, verbose_name='用户头像')
    level = models.IntegerField(verbose_name='用户权限', default=0)#1: admin 2: user 3: guest
    group = models.ForeignKey(Group, max_length=30, blank=True, null=True, verbose_name='用户所属组')
    is_delete = models.IntegerField(verbose_name='删除标志位', default=0)#1: admin 2: user 3: guest

    class Meta:
        verbose_name_plural = '用户'
        ordering = ['-id']

    def __unicode__(self):
        return self.username


# 任务信息
class Task(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='任务编号')
    title = models.CharField(max_length=50, verbose_name='任务标题')
    description = models.CharField(max_length=200,  verbose_name='任务描述')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    start_time = models.DateTimeField(verbose_name='开始时间')
    update_time = models.DateTimeField(auto_now_add=True, verbose_name='修改时间')
    finish_time = models.DateTimeField(verbose_name='完成时间')
    channel = models.CharField(max_length=50, verbose_name='频道号')
    task_status = models.IntegerField(default=0, verbose_name='状态')
    is_delete = models.IntegerField(verbose_name='删除标志位', default=0)

    class Meta:
        verbose_name_plural = '直播任务'
        ordering = ['id']

    def __unicode__(self):
        return self.title


# 节点类型
class Category(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='节点类编号')
    name = models.CharField(max_length=30, verbose_name='分类名称')

    class Meta:
        verbose_name_plural = '节点类型'
        ordering = ['id']

    def __unicode__(self):
        return self.name


# 节点信息
class Node(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='节点编号')
    name = models.CharField(max_length=30, blank=True, unique=True, verbose_name='节点名')
    category = models.ForeignKey(Category, blank=True, null=True, verbose_name='分类名称')
    node_status = models.IntegerField(default=0, verbose_name='节点状态')
    node_info = models.CharField(max_length=20, null=True, blank=True,  verbose_name='状态描述')
    is_delete = models.IntegerField(verbose_name='删除标志位', default=0)

    class Meta:
        verbose_name_plural = '节点'
        ordering = ['id']

    def __unicode__(self):
        return self.name


# 节点详情
class Node_detail(models.Model):
    ip = models.URLField(blank=True, null=True, verbose_name='节点地址')
    node_name = models.ForeignKey(Node, max_length=30,  verbose_name='节点名')
    channel = models.IntegerField(blank=True, null=True, verbose_name='频道号')
    node_status = models.IntegerField(default=0, verbose_name='节点状态')
    ip_info = models.CharField(max_length=20, null=True, blank=True,  verbose_name='状态描述')
    is_delete = models.IntegerField(verbose_name='删除标志位', default=0)
    method = models.CharField(max_length=200,  verbose_name='重启方式')

    class Meta:
        verbose_name_plural = '节点详情'

    def __unicode__(self):
        return self.ip


# 操作记录
class Op_log(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='操作序号')
    op_name = models.CharField(max_length=200, verbose_name='操作人员')
    op_detail = models.CharField(max_length=200, blank=True, null=True, verbose_name='操作详情')
    op_time = models.DateTimeField(auto_now_add=True, verbose_name='操作时间')

    class Meta:
        verbose_name_plural = '操作记录'

    def __unicode__(self):
        return self.op_detail