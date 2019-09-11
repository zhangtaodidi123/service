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
    service = models.CharField(max_length=218, verbose_name='后端节点',null=True)
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



