# -*- coding: utf-8 -*-
import logging
from django.shortcuts import render, redirect, HttpResponse,render_to_response,HttpResponseRedirect,RequestContext
from django.contrib.auth import logout, login, authenticate
from models import History, Item, FlowCar, FlowCount
import time
import json
from django.db.models import Count, Q, Sum
from django.views.decorators.csrf import csrf_exempt
from func.rdate import day_range, day_rang, month_range
from func.bcdn import count_up, count_yun, count_letv
import csv


logger = logging.getLogger('monitor.views')


# 登入首页
def do_login(request):
    username = request.COOKIES.get('username','')
    if username:
        username = request.session.get('username', 'anybody')
    return render(request, 'login.html', locals())


# 获取cdn监控信息出图
def monitor(request):
    info = {}
    try:
        yun_value_brand,yun_clock_brand = History.objects.get_cdn('yunfan[cdn.brand]')
        yun_value_pass,yun_clock_pass = History.objects.get_cdn('yunfan[cdn.pass]')
        le_value,le_clock = History.objects.get_cdn('letv[cdn.brand]')
        le_value_pass,le_clock_pass = History.objects.get_cdn('letv[cdn.pass]')
        up_value,up_clock = History.objects.get_cdn('upyun[cdn.brand]')
        up_value_pass,up_clock_pass = History.objects.get_cdn('upyun[cdn.pass]')

        info = {
            "yun_brand": yun_value_brand,
            "yun_pass": yun_value_pass,
            "yun_clock": yun_clock_brand,
            "le_value": le_value,
            "le_pass": le_value_pass,
            "le_clock": le_clock,
            "up_value": up_value,
            "up_clock": up_clock,
            "up_pass": up_value_pass
        }
    except Exception as e:
        logger.error(e)

    return render_to_response("monitor.html", info,context_instance = RequestContext(request))


# 获取流量信息出图
def flow(request):
    clock = []
    item_ctc1 = []
    item_ctc2 = []
    item_cuc = []
    item_cmcc = []
    ctc1 = Item.objects.filter(group__name='ctc1').values('name')
    for i in ctc1:
        try:
            name,value,clock = History.objects.get_flow(i['name'])
            info = {
                "name": name,
                "value": value,
                "clock": clock,
            }
            item_ctc1.append(info)
        except Exception as e:
            logger.error(e)

    ctc2 = Item.objects.filter(group__name='ctc2').values('name')
    for i in ctc2:
        try:
            name, value, clock = History.objects.get_flow(i['name'])
            info = {
                "name": name,
                "value": value,
                "clock": clock,
            }
            item_ctc2.append(info)
        except Exception as e:
            logger.error(e)

    cuc = Item.objects.filter(group__name='cuc').values('name')
    for i in cuc:
        try:
            name, value, clock = History.objects.get_flow(i['name'])
            info = {
                "name": name,
                "value": value,
                "clock": clock,
            }
            item_cuc.append(info)
        except Exception as e:
            logger.error(e)

    cmcc = Item.objects.filter(group__name='cm&gw&bg').values('name')
    for i in cmcc:
        try:
            name, value, clock = History.objects.get_flow(i['name'])
            info = {
                "name": name,
                "value": value,
                "clock": clock,
            }
            item_cmcc.append(info)
        except Exception as e:
            logger.error(e)
    # return render(request, 'monitor_flow.html', locals())
    return render(request, 'monitor_flow.html',
                  {'ctc1': item_ctc1,'ctc2':item_ctc2,'cuc':item_cuc, 'cmcc':item_cmcc,'clock': clock} )
    # return render_to_response("monitor_flow.html", info,context_instance = RequestContext(request))

def flow_count(request):

    timeStamp = time.time()
    timeArray = time.localtime(timeStamp)
    date = request.GET.get('month','')
    if date == 'now':
        month = str(int(time.strftime("%Y%m", timeArray)))
    else:
        month = str(int(time.strftime("%Y%m", timeArray)) - 1)
    item_list = []
    try:
        category = FlowCar.objects.all()
        for c in category:
            money = {}
            try:
                if date == 'now':
                    money = FlowCount.objects.values('predict').get(month=month, name=c.name)
                else:
                    money = FlowCount.objects.values('count').get(month=month, name=c.name)
            except Exception as e:
                money['count'] = '尚未统计'
                money['surplus'] = 0
            if date == 'now':
                item = {
                    "name": c.name,
                    "region": c.region,
                    "operator": c.operator,
                    "fees": c.fees,
                    "month": month,
                    "money": money['predict']
                }
            else:
                item = {
                    "name": c.name,
                    "region": c.region,
                    "operator": c.operator,
                    "fees": c.fees,
                    "month": month,
                    "money": money['count']
                }
            item_list.append(item)
    except Exception as e:
        logger.error(e)
    return render(request, 'monitor_count.html',{'all': item_list})

def flow_count_history(request):
    timeStamp = time.time()
    timeArray = time.localtime(timeStamp)
    month = str(int(time.strftime("%Y%m", timeArray)) - 1)
    item_list = []
    try:
        category = FlowCar.objects.all()
        for c in category:
            money = FlowCount.objects.values('count').filter(~Q(month=month),name=c.name)
            item = {
                "name": c.name,
                "region": c.region,
                "operator": c.operator,
                "fees": c.fees,
                "month": month,
                "money": money['count']
            }
            item_list.append(item)
    except Exception as e:
        print e
        logger.error(e)
    return render(request, 'monitor_count.html',{'all': item_list})


def flow_detail(request):
    name = request.GET.get('name', "")
    day = request.GET.get('day', "")
    print day
    value = clock = []
    try:
        if day != '':
            today,tomorrow = day_range(day)
        else:
            today,tomorrow = day_rang(time.time())
        value,clock = History.objects.get_day(name=name,today=today,tomorrow=tomorrow)
    except Exception as e:
        logger.error(e)
    return render(request, 'monitor_detail.html',{'name': name,'value': value,'clock':clock})


# 所有节点流量
def all_node(request):
    info = {}
    # select sum(add_value) from monitor_history where add_value is not null group by his_clock limit 10;
    try:
        value,clock = History.objects.group_by_all()
        info = {
            'value' : value,
            'clock' : clock
        }
    except Exception as e:
        logger.error(e)
    return render_to_response("monitor_all_node.html", info,context_instance = RequestContext(request))


def host(request):
    return render(request, 'host_manage.html')


# 报表导出
def export(request):
    timeStamp = time.time()
    timeArray = time.localtime(timeStamp)
    month = str(int(time.strftime("%Y%m", timeArray)))
    print type(month)
    response = HttpResponse(content_type='text/csv')
    try:
        date = request.GET.get('date', 'none')
        filename = 'attachment; filename={0}宽带数据.csv'.format(date)
        response['Content-Disposition'] = filename
        writer = csv.writer(response)
        category = FlowCar.objects.all().order_by('project_id','operator')
        s1=s2=s3=s4=0
        item_list1 = []
        item_list2 = []
        item_list3 = []
        item_list4 = []
        writer.writerow(['项目', '供应商', '日期', '内容', '主合同号', '金额(元)', '保底价', '超量单价', '月超量', '机位费', 'IP'])
        for c in category:
            if c.project == '自建CDN':
                s1 = 0
                money = {}
                try:
                    money = FlowCount.objects.values('count','surplus','predict').get(month=date, name=c.name)
                except Exception as e:
                    print e
                    logger.error(e)

                    if month == date:
                        money['predict'] = 0
                    else:
                        money['count'] = 0
                    money['surplus'] = 0
                if month == date:
                    item = [c.project, c.operator, date, c.memo, c.contract,
                            money['predict'], c.basic, c.surplus, money['surplus'], c.cabinet, c.ip_fee]
                else:
                    item = [c.project, c.operator, date, c.memo, c.contract,
                            money['count'], c.basic, c.surplus, money['surplus'], c.cabinet, c.ip_fee]
                item_list1.append(item)
                print item_list1


            if c.project == '商用CDN':
                s2 = 0
                money = {}
                try:
                    money = FlowCount.objects.values('count','surplus','predict').get(month=date, name=c.name)
                except Exception as e:
                    logger.error(e)
                    if month == date:
                        money['predict'] = 0
                    else:
                        money['count'] = 0
                    money['surplus'] = 0
                if month == date:
                    item = [c.project, c.operator, date, c.memo, c.contract,
                            money['predict'], c.basic, c.surplus, money['surplus'], c.cabinet, c.ip_fee]
                else:
                    item = [c.project, c.operator, date, c.memo, c.contract,
                            money['count'], c.basic, c.surplus, money['surplus'], c.cabinet, c.ip_fee]
                item_list2.append(item)


            if c.project == '源节点':
                s3 = 0
                money = {}
                try:
                    money = FlowCount.objects.values('count','surplus','predict').get(month=date, name=c.name)
                except Exception as e:
                    logger.error(e)
                    if month == date:
                        money['predict'] = 0
                    else:
                        money['count'] = 0
                    money['surplus'] = 0
                if month == date:
                    item = [c.project, c.operator, date, c.memo, c.contract,
                            money['predict'], c.basic, c.surplus, money['surplus'], c.cabinet, c.ip_fee]
                else:
                    item = [c.project, c.operator, date, c.memo, c.contract,
                            money['count'], c.basic, c.surplus, money['surplus'], c.cabinet, c.ip_fee]
                item_list3.append(item)


            if c.project == '其他':
                s4 = 0
                money = {}
                item_list4 = []
                try:
                    money = FlowCount.objects.values('count','surplus','predict').get(month=date, name=c.name)
                except Exception as e:
                    logger.error(e)
                    if month == date:
                        money['predict'] = 0
                    else:
                        money['count'] = 0
                    money['surplus'] = 0
                if month == date:
                    item = [c.project, c.operator, date, c.memo, c.contract,
                            money['predict'], c.basic, c.surplus, money['surplus'], c.cabinet, c.ip_fee]
                else:
                    item = [c.project, c.operator, date, c.memo, c.contract,
                            money['count'], c.basic, c.surplus, money['surplus'], c.cabinet, c.ip_fee]
                item_list4.append(item)

        for i in item_list1:
            s1 += float(i[5])
            writer.writerow(i)
        writer.writerow(['小计', '', '', '', '', s1, '', '', '', '', '' ])
        for i in item_list2:
            s2 += float(i[5])
            writer.writerow(i)
        writer.writerow(['小计', '', '', '', '', s2, '', '', '', '', ''])
        for i in item_list3:
            s3 += float(i[5])
            writer.writerow(i)
        writer.writerow(['小计', '', '', '', '', s3, '', '', '', '', ''])
        for i in item_list4:
            s4 += float(i[5])
            writer.writerow(i)
        writer.writerow(['小计', '', '', '', '', s4, '', '', '', '', ''])

        writer.writerow(['总计', '', '', '', '', s1+s2+s3+s4, '', '', '', '', ''])

    except Exception as e:
        logger.error(e)
    return response


# 当月预算计费 上月自动计费
def auto_count(request):
    timeStamp = time.time()
    timeArray = time.localtime(timeStamp)
    last = True
    date = request.GET.get('month','')
    if date == 'last':
        month = str(int(time.strftime("%Y%m", timeArray)) -1)
        f_day = '{0}{1}'.format(month, '01')
        l_day = '{0}{1}'.format(str(int(time.strftime("%Y%m", timeArray))), '01')
    else:
        last = False
        month = str(int(time.strftime("%Y%m", timeArray)))
        f_day = '{0}{1}'.format(month, '01')
        l_day = str(int(time.strftime("%Y%m%d", timeArray)))
    count1 = count2 = count3 =count4 = 0
    a, b = month_range(month)
    type1 = '自建CDN'
    type2 = '源节点'
    type3 = '商用CDN'
    items = Item.objects.filter(Q(item_type=type1) | Q(item_type=type2))
    try:
        for i in items:
            value,clock = History.objects.get_day(name=i.name,today=a,tomorrow=b)
            e = value[-432]
            # e= 0
            try:
                flow = FlowCar.objects.get(name=i)
                add = 0
                if flow.basic_value < e :
                    try:
                        f =FlowCount.objects.get(name=i,month=month)
                        add = e-flow.basic_value
                        if f:
                            f.surplus = add
                            f.save()
                    except Exception as e:
                        print e
                        logger.error(e)
                        try:
                            fc = FlowCount(name=i, month=month, surplus=add, predict=0, count=0)
                            fc.save()
                        except Exception as e:
                            print e
                            logger.error(e)
                else:
                    try:
                        f =FlowCount.objects.get(name=i,month=month)
                        if f:
                            f.surplus = 0
                            f.save()
                    except Exception as e:
                        logger.error(e)
                        try:
                            fc = FlowCount(name=i, month=month, surplus=0, predict=0, count=0)
                            fc.save()
                        except Exception as e:
                            print e
                            logger.error(e)
            except Exception as e:
                print e
                logger.error(e)

        bi = Item.objects.filter(Q(item_type=type3))
        try:
            for b in bi:
                try:
                    f = FlowCount.objects.get(name=b, month=month)
                    if b.name=='upyunvod':
                        f.surplus = count_up(f_day, l_day)
                        f.save()
                    elif b.name=='upyun':
                        f.surplus = count_up(f_day, l_day,vod=False)
                        f.save()
                    elif b.name=='yunfan':
                        f.surplus = count_yun(f_day, l_day)
                        f.save()
                    elif b.name=='letv':
                        f.surplus = count_letv(f_day, l_day)
                        f.save()
                except Exception as e:
                    if b.name=='upyunvod':
                        up_flow  = count_up(f_day, l_day)
                        up = FlowCount(name=b, month=month, surplus=up_flow, predict=0, count=0)
                        up.save()
                    if b.name == 'upyun':
                        up_flow = count_up(f_day, l_day,vod=False)
                        up = FlowCount(name=b, month=month, surplus=up_flow, predict=0, count=0)
                        up.save()
                    if b.name == 'yunfan':
                        up_flow = count_yun(f_day, l_day)
                        up = FlowCount(name=b, month=month, surplus=up_flow, predict=0, count=0)
                        up.save()
                    if b.name == 'letv':
                        up_flow = count_letv(f_day, l_day)
                        up = FlowCount(name=b, month=month, surplus=up_flow, predict=0, count=0)
                        up.save()
        except Exception as e:
            print e

        category = FlowCar.objects.all()

        for c in category:
            f = c.fees.split('+')
            for i in f:
                if i == 'basic':
                    count1 = c.basic
                elif i == 'surplus*n':
                    count2 = c.surplus
                elif i == 'cabinet':
                    count3 = c.cabinet
                elif i == 'ip_fee':
                    count4 = c.ip_fee
            try:
                money = FlowCount.objects.get(month=month, name=c.name)
                if last:
                    money.count = count1 + count2*money.surplus + count3 + count4
                else:
                    money.predict = count1 + count2*money.surplus + count3 + count4
                money.save()
            except Exception as e:
                print e
                logger.error(e)
    except Exception as e:
        print e
        logger.error(e)
    return HttpResponseRedirect('/monitor/flow/count')


# 项目管理
def p_manage(request):
    return render(request, 'monitor_p_manage.html')


# url监控
def url_monitor(request):
    pass


# 流程测试
def process_test(request):
    pass


# 注销动作
def test(request):
    return render(request, 'monitor.html')
    # del req.session['username']  # 删除session
    # return HttpResponse('logout ok!')



