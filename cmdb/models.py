from django.db import models

#!/bin/env python
# -*- coding:utf-8 -*-

from django.db import models

# Create your models here.

'''数据中心机房管理'''
class DataCenter(models.Model):
    '''机房区域'''
    name = models.CharField(max_length=32, verbose_name='机房区域')
    manufactory_choices = (
        (0, 'UCloud'),
        (1, 'Aliyun'),
        (2, '渔人码头26F'),
        (3, '渔人码头27F')

    )
    manufactory = models.SmallIntegerField(choices=manufactory_choices, default=0, verbose_name='云服务商')
    address = models.CharField(max_length=128, verbose_name='机房地址', null=True, blank=True)
    project_name = models.CharField(max_length=32, verbose_name='所属项目')
    email = models.CharField(max_length=32, verbose_name='邮箱', null=True, blank=True)
    mobile = models.CharField(max_length=16, verbose_name='联系方式', null=True, blank=True)
    comment = models.TextField(max_length=256, verbose_name='备注', null=True, blank=True)

    class Meta:
        unique_together = (('name', 'project_name'),)
        verbose_name = '机房区域'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s -- %s' % (self.project_name, self.name)

class EIP(models.Model):
    name = models.CharField(max_length=32, verbose_name='EIP名称')
    ip_address = models.GenericIPAddressField(protocol='ipv4', verbose_name='IP地址', unique=True)
    bandwidth = models.CharField(max_length=16, verbose_name='带宽(MB)')
    band_status_choices =  models.CharField(max_length=16, verbose_name='绑定状态',null=True)
    data_center = models.ForeignKey('DataCenter', verbose_name='机房区域', on_delete=models.SET_NULL, null=True, blank=True)
    comment = models.CharField(max_length=256, verbose_name='备注', null=True, blank=True)

    class Meta:
        verbose_name = 'EIP'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.ip_address


class ULB(models.Model):
    name = models.CharField(max_length=32, verbose_name='ULB名称')
    ulb_ip = models.GenericIPAddressField(protocol='ipv4', verbose_name='基础网络', unique=True)
    service1 = models.CharField(max_length=218, verbose_name='后端节点1',null=True)
    service2 = models.CharField(max_length=218, verbose_name='后端节点2',null=True)
    service3 = models.CharField(max_length=218, verbose_name='后端节点3',null=True)
    service4 = models.CharField(max_length=218, verbose_name='后端节点4',null=True)
    service5 = models.CharField(max_length=218, verbose_name='后端节点4',null=True)
    comment = models.CharField(max_length=128, verbose_name='备注', null=True, blank=True)

    class Meta:
        verbose_name = 'ULB'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


'''主机管理部分'''
class Host_table(models.Model):
    host_name = models.CharField(max_length=32, verbose_name='主机名称')
    etc = models.CharField(max_length=64, verbose_name='操作系统',null=True)
    cpu = models.CharField(max_length=8, verbose_name='CPU核数')
    memory = models.CharField(max_length=8, verbose_name='内存大小(MB)')
    disk = models.CharField(max_length=16, verbose_name='磁盘大小(GB)')
    ip_in = models.GenericIPAddressField(protocol='ipv4', verbose_name='内网IP', unique=True)
    ip_out = models.GenericIPAddressField(protocol='ipv4', verbose_name='外网IP', null=True, blank=True)
    status_choices = models.CharField(max_length=32, verbose_name='状态',null=True)

    comment = models.TextField(max_length=256, verbose_name='备注', null=True, blank=True)
    # create_date = models.DateTimeField(auto_now_add=True, blank=True)
    # update_date = models.DateTimeField(auto_now=True, blank=True)
    class Meta:
        verbose_name = '主机信息'
        verbose_name_plural = verbose_name
    def __unicode__(self):
        return  self.title




## ansible web 自动化部分
ONLINE_STATUS = (
    (str(0), u"停用"),
    (str(1), u"激活"),
)


# Create your models here.
class history(models.Model):
    login_user = models.CharField(u"登录用户", max_length=50)
    src_ip = models.CharField(u"来源ip", max_length=50)
    task_name = models.CharField(u"任务类型", max_length=50, default="none")
    time_task_start = models.DateTimeField(u'开始时间', null=True)
    time_task_finished = models.DateTimeField(u'结束时间', auto_now_add=True, null=True)
    cmd_object = models.CharField(u"操作对象", max_length=50, null=True)
    cmd = models.CharField(u"执行命令", max_length=200)
    cmd_result = models.CharField(u"命令结果", max_length=10)
    cmd_detail = models.CharField(u"结果详情", max_length=5000, null=True, blank=True)

    def __unicode__(self):
        return self.cmd_result

    class Meta:
        ordering = ['-id']


class project(models.Model):
    name = models.CharField(u"项目名", max_length=50)
    path = models.CharField(u"项目路径", max_length=50)
    online_status = models.CharField(u"激活状态", choices=ONLINE_STATUS, max_length=30, null=True, blank=True)

    def __unicode__(self):
        return self.name


class job(models.Model):
    name = models.CharField(max_length=50, verbose_name=u"作业名", unique=True)
    playbook = models.CharField(u"playbook", max_length=100, null=True, blank=True)
    project = models.ForeignKey(project, verbose_name=u"所属项目", on_delete=models.SET_NULL, null=True, blank=True)
    online_status = models.CharField(u"激活状态", choices=ONLINE_STATUS, max_length=30, null=True, blank=True)

    def __unicode__(self):
        return self.name


class extravars(models.Model):
    name = models.CharField(max_length=50, verbose_name=u"变量组名", unique=True)
    vars = models.CharField(u"配置参数", max_length=150, null=True, blank=True)
    job = models.ForeignKey(job, verbose_name=u"所属作业", on_delete=models.SET_NULL, null=True, blank=True)
    online_status = models.CharField(u"激活状态", choices=ONLINE_STATUS, max_length=30, null=True, blank=True)

    def __unicode__(self):
        return self.name





