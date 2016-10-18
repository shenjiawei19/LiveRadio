# -*- coding: utf-8 -*-
from django.db import models
from radio.models import User
import time


# 监控系统
class System(models.Model):

    id = models.AutoField(primary_key=True, verbose_name='系统编号')
    # linux,windows,
    name = models.CharField(max_length=30, verbose_name='系统名')

    Linux = 'Linux'
    Windows = 'Windows'
    exchange = '交换机'
    SYSTEM_CHOICES = (
        (Linux, 'Linux'),
        (Windows, 'Windows'),
        (exchange, '交换机'),
    )
    system = models.CharField(
        max_length=20,
        choices=SYSTEM_CHOICES,
        default=Linux,
    )

    class Meta:
        verbose_name_plural = '系统名'

    def __unicode__(self):
        return self.name

# 监控主机组
class Host_group(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='编号')

    name = models.CharField(max_length=30, verbose_name='监控组类')

    class Meta:
        verbose_name_plural = '监控组'

    def __unicode__(self):
        return self.name

# 监控主机
class Host(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='编号')

    ip = models.GenericIPAddressField(verbose_name='主机地址')

    name = models.CharField(max_length=30, verbose_name='主机名')

    username = models.CharField(blank=True, null=True, max_length=30, verbose_name='用户名')

    password = models.CharField(blank=True, null=True, max_length=64, verbose_name='密码')

    system = models.ForeignKey(System, max_length=30, verbose_name='系统类型')

    group = models.ForeignKey(Host_group, max_length=30, verbose_name='监控组')


    class Meta:
        verbose_name_plural = '监控主机'

    def __unicode__(self):
        return self.name

# 监控项分类
class Item_Group(models.Model):

    id = models.AutoField(primary_key=True, verbose_name='编号')

    name = models.CharField(max_length=10,unique=True, verbose_name='监控项分类')


    class Meta:
        verbose_name_plural = '监控项分类'
        ordering = ['id']

    def __unicode__(self):
        return self.name

# 监控服务项
class Item(models.Model):

    id = models.AutoField(primary_key=True, verbose_name='编号')

    name = models.CharField(max_length=64,unique=True,blank=True,verbose_name='指标名称')

    host = models.ForeignKey(Host,verbose_name='关联主机')

    key = models.CharField(max_length=64,verbose_name='监控服务项')

    last_clock = models.IntegerField(blank=True,null=True,verbose_name='监控最后获取时间')

    last_value = models.IntegerField(blank=True,null=True,verbose_name='监控最后获取数据')

    Str = 'str'
    Int = 'int'
    Float = 'float'

    DATA_TYPE_CHOICES = (
        (Str, 'str'),
        (Int, 'int'),
        (Float, 'float'),
    )
    charset = models.CharField(
        max_length=5,
        choices=DATA_TYPE_CHOICES,
        default=Str,
        verbose_name='监控获取值类型'
    )

    MY = '自建CDN'
    BUS = '商用CDN'
    NODE = '源节点'
    OTHER = '其他'

    ITEM_TYPE_CHOICES = (
        (MY, '自建CDN'),
        (BUS, '商用CDN'),
        (NODE, '源节点'),
        (OTHER, '其他'),
    )

    item_type = models.CharField(
        max_length=10,
        choices=ITEM_TYPE_CHOICES,
        default=MY,
        verbose_name='CDN类型'
    )

    group = models.ForeignKey(Item_Group,blank=True,null=True,verbose_name='监控分类')

    memo = models.CharField(max_length=64,verbose_name='备注')

    class Meta:
        verbose_name_plural = '监控项'
        ordering = ['id']

    def __unicode__(self):
        return self.name

# 监控服务组
class Service_Group(models.Model):

    id = models.AutoField(primary_key=True, verbose_name='编号')

    name = models.CharField(max_length=10,unique=True, verbose_name='监控服务组名')


    class Meta:
        verbose_name_plural = '监控服务组'
        ordering = ['id']

    def __unicode__(self):
        return self.name


# 监控服务
class Service(models.Model):

    id = models.AutoField(primary_key=True, verbose_name='编号')

    name = models.CharField(max_length=65, unique=True, verbose_name='监控名')

    interval = models.IntegerField(default=60, verbose_name='监控间隔')

    plugin = models.CharField(max_length=200, verbose_name='插件脚本')

    items = models.ManyToManyField(Item, verbose_name='监控项列表')

    group = models.ForeignKey(Service_Group,blank=True,null=True)

    memo = models.CharField(max_length=64, verbose_name='备注')

    class Meta:
        verbose_name_plural = '监控服务'
        ordering = ['id']

    def __unicode__(self):
        return self.name



# 监控触发器
class Trigger(models.Model):

    id = models.AutoField(primary_key=True, verbose_name='编号')

    name = models.CharField(max_length=64, verbose_name='触发器列表')

    expression = models.TextField(verbose_name='表达式')

    info = 'info'
    warn = 'warning'
    high = 'high'
    critical = 'critical'
    WARN_CHOICES = (
        (info, 'info'),
        (warn, 'warning'),
        (high, 'high'),
        (critical, 'critical')
    )
    severity = models.CharField(
        max_length=10,
        choices=WARN_CHOICES,
        verbose_name='告警等级'
    )

    enabled = models.BooleanField(default=True, verbose_name='是否启用')

    class Meta:
        verbose_name_plural = '触发器'
        ordering = ['id']

    def __unicode__(self):
        return self.name

# 模板
class Template(models.Model):

    id = models.AutoField(primary_key=True, verbose_name='编号')

    name = models.CharField(max_length=64, unique=True, verbose_name='模板名')

    services = models.ManyToManyField(Service, verbose_name='服务列表')

    triggers = models.ManyToManyField(Trigger, blank=True, verbose_name='触发器列表')

    hosts = models.ManyToManyField(Host, blank=True, verbose_name='关联主机')


    class Meta:
        verbose_name_plural = '模板'
        ordering = ['id']

    def __unicode__(self):
        return self.name


# 触发选择列表
class Action_method(models.Model):

    id = models.AutoField(primary_key=True, verbose_name='编号')

    name = models.CharField(max_length=64,verbose_name='执行名称')

    step = models.SmallIntegerField(default=1,verbose_name='第N次告警')

    ACTION_TYPE_CHOICES = (
        ('email','Email'),
        ('sms','SMS'),
        ('script','RunScript'),
    )
    action_type = models.CharField(
        max_length=10,
        choices=ACTION_TYPE_CHOICES,
        verbose_name='告警发送方式'
    )

    notifiers = models.ManyToManyField(User,verbose_name='通知对象',blank=True)

    class Meta:
        verbose_name_plural = '告警方式'
        ordering = ['id']

    def __unicode__(self):
        return self.name


# 触发执行
class Action(models.Model):

    id = models.AutoField(primary_key=True, verbose_name='编号')

    name = models.CharField(max_length=64,unique=True,verbose_name='触发方式')

    host_groups = models.ManyToManyField(Host_group,blank=True,verbose_name='触发群组列表')

    hosts = models.ManyToManyField(Host,blank=True,verbose_name='触发主机列表')

    conditions = models.TextField(verbose_name='告警条件')

    level = models.ForeignKey(Trigger,verbose_name='告警触发列表')

    interval = models.IntegerField(verbose_name='轮循时间')

    operations = models.ManyToManyField(Action_method,verbose_name='触发告警后到方式')

    enabled = models.BooleanField(default=True,verbose_name='告警是否启用')

    subject = models.CharField(max_length=64,verbose_name='告警主题')

    message = models.CharField(max_length=640,verbose_name='告警消息')

    recover_enabled = models.BooleanField(default=True,verbose_name='恢复后是否发送通知')

    recover_subject = models.CharField(max_length=64,verbose_name='恢复主题')

    recover_message = models.CharField(max_length=640,verbose_name='恢复到消息')

    class Meta:
        verbose_name_plural = '告警详情'
        ordering = ['id']

    def __unicode__(self):
        return self.name


class Maintenance(models.Model):

    id = models.AutoField(primary_key=True, verbose_name='编号')

    name = models.CharField(max_length=64,unique=True, verbose_name='名称')

    hosts = models.ManyToManyField(Host,blank=True, verbose_name='主机')

    host_groups = models.ManyToManyField(Host_group, blank=True, verbose_name='主机组')

    start_time = models.IntegerField(verbose_name='维护开始时间')

    end_time = models.IntegerField(verbose_name='维护结束时间')

    memo = models.CharField(max_length=64,verbose_name='备注')

    class Meta:
        verbose_name_plural = '维保系统'
        ordering = ['id']

    def __unicode__(self):
        return self.name


class Special(models.Model):

    id = models.AutoField(primary_key=True, verbose_name='编号')

    name = models.CharField(max_length=30, verbose_name='标识名')

    memo = models.CharField(max_length=64, verbose_name='备注')

    class Meta:
        verbose_name_plural = '特别信息'
        ordering = ['id']

    def __unicode__(self):
        return self.name

class HistoryManager(models.Manager):

    def cdn_queryset(self,name):
        return super(HistoryManager, self).get_queryset().filter(special__name=name).order_by('-his_clock')[:250].values('value','his_clock')


    def get_cdn(self,name):
        yun_value = []
        yun_clock = []
        cdn = self.cdn_queryset(name)
        for t in cdn:
            timeArray = time.localtime(t['his_clock'])
            StyleTime = time.strftime("%Y%m%d%H%M", timeArray)
            if int(StyleTime) not in yun_clock :
                yun_value.append(int(t['value']))
                yun_clock.append(int(StyleTime))
        yun_value.reverse()
        yun_clock.reverse()
        return yun_value[:],yun_clock

    def flow_queryset(self,name):
        return super(HistoryManager, self).get_queryset().filter(items__name=name).order_by('-his_clock')[:150].values('items__memo','add_value','his_clock')


    def get_flow(self,name):
        item = ''
        value = []
        clock = []
        flow = self.flow_queryset(name)

        try:
            for t in flow:
                item = t['items__memo']
                timeArray = time.localtime(t['his_clock'] )
                StyleTime = time.strftime("%Y%m%d%H%M", timeArray)
                if t['add_value'] is 'None' or t['add_value'] <0 :
                    t['add_value'] = 0
                if int(StyleTime) not in clock:
                    value.append(round(int(t['add_value'])/300/128/1024.00,2))
                    clock.append(int(StyleTime))
            value.reverse()
            clock.reverse()
        except Exception as e:
            print e
        return item,value, clock

    def day_queryset(self,name,today,tomorrow):
        return super(HistoryManager, self).get_queryset().filter(items__name=name,his_clock__gt=today,his_clock__lte = tomorrow).values('items__name','his_clock','add_value')

    def get_day(self,name,today,tomorrow):
        value = []
        clock = []
        data =self.day_queryset(name,today,tomorrow)
        for d in data:
            d['his_clock'] = time.strftime("%Y%m%d%H%M", time.localtime(d['his_clock'] ))
            clock.append(int(d['his_clock']))
            if d['add_value'] is 'None' or d['add_value'] < 0:
                d['add_value'] = 0
            d['add_value'] = round(int(d['add_value'])/300/128/1024.00,2)
            value.append(d['add_value'])
        return value,clock


    def group_by_all(self):
        value = []
        clock = []
        item = ''
        print "1"
        data =self.filter(add_value__isnull=False).order_by('-his_clock','add_value')[:4500]
        print data
        for d in data:
            timeArray = time.localtime(d.his_clock)
            StyleTime = int(time.strftime("%Y%m%d%H%M", timeArray))
            if StyleTime not in clock:
                clock.append(StyleTime)
                print clock
                value.append(round(int(d.add_value) / 300 / 128 / 1024.00, 2))
                item = d.items
                print d.items
            else:
                if item == d.items:
                    pass
                else:
                    value[clock.index(StyleTime)] += round(int(d.add_value) / 300 / 128 / 1024.00, 2)
        value.reverse()
        clock.reverse()
        return value,clock

class History(models.Model):

    id = models.AutoField(primary_key=True, verbose_name='编号')

    items = models.ForeignKey(Item,blank=True,null=True,verbose_name='监控项')

    his_clock = models.IntegerField(verbose_name='数据获取时间')

    value = models.DecimalField(max_digits=20,decimal_places=2,verbose_name='数据值')

    interval_time = models.IntegerField(blank=True,null=True,verbose_name='轮询时间')

    add_value = models.DecimalField(max_digits=20,decimal_places=2,blank=True,null=True,verbose_name='变化值')

    hosts = models.ForeignKey(Host,blank=True,null=True,verbose_name='主机信息')

    status = models.SmallIntegerField(default=0,verbose_name='数据状态信息')

    special = models.ForeignKey(Special,blank=True,null=True,verbose_name='特别标识信息')

    objects = HistoryManager()

    class Meta:
        verbose_name_plural = '监控历史数据'
        ordering = ['id']

    def __unicode__(self):
        return str(self.id)

# 宽带分类 :(
class FlowCar(models.Model):

    id = models.AutoField(primary_key=True, verbose_name='编号')

    name = models.ForeignKey(Item, verbose_name='名称')

    project_id = models.SmallIntegerField(verbose_name='项目编号')

    project = models.CharField(max_length=50, verbose_name='项目')

    operator = models.CharField(max_length=50, verbose_name='供应商')

    region = models.CharField(max_length=50, verbose_name='地区')

    memo = models.CharField(max_length=50, verbose_name='内容')

    contract = models.CharField(max_length=50, verbose_name='合同号')

    basic_value = models.FloatField(verbose_name='保底宽带', default=0)

    basic = models.FloatField(verbose_name='保底单价', default=0)

    surplus = models.FloatField(verbose_name='超量单价', default=0)

    cabinet = models.FloatField(verbose_name='机位费用', default=0)

    ip_fee = models.FloatField(verbose_name='IP费用', default=0)

    fees = models.CharField(max_length=50, verbose_name='计费方式', default='basic+surplus*n+cabinet+ip_fee')

    class Meta:
        verbose_name_plural = '宽带分类'
        ordering = ['id','-project_id']

    def __unicode__(self):
        return str(self.id)

# 宽带计费统计 :(
class FlowCount(models.Model):

    id = models.AutoField(primary_key=True, verbose_name='编号')

    name = models.ForeignKey(Item, verbose_name='名称')

    month = models.IntegerField(verbose_name='年月')

    surplus = models.FloatField(verbose_name='当月超量值', default=0)

    predict = models.CharField(max_length=50, verbose_name='预计费用')

    count = models.CharField(max_length=50, verbose_name='计费金额')

    class Meta:
        verbose_name_plural = '宽带计费统计'
        ordering = ['id']

    def __unicode__(self):
        return str(self.id)