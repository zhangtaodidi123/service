from django.shortcuts import render
from .models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render,render_to_response,HttpResponse,redirect
from cmdb.models import Host_table,project
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger  # 分页用到的几个模块
from  cmdb import  models
from service.forms import ProjectFrom
from  service.forms import UserGroup_form
import json
import shutil
from collections import namedtuple






def index(request):
    return render(request, 'index.html')

def welcome(request):
    return render(request,'welcome.html')



'''获取主机管理页面信息并返回'''
def article(request):


    host_list = Host_table.objects.all()   # 取出所有的主机页面信息
    paginator = Paginator(host_list,16,16)  # 实例化结果集，每页16条数据,少于15条就合并到上一页
    page = request.GET.get('page')          # 接收网页传递过来的 page

    try:
        customer = paginator.page(page)   # 传递给当前的html对象

    except PageNotAnInteger:

        customer = paginator.page(1)
    except EmptyPage:
        customer = paginator.page(paginator.num_pages)
    return render(request,'article-list.html',{"host_list":customer})

def  search(request):
    q = request.GET.get('q','')
    error_msg = ''
    if not q:
        error_msg = '请输入关键字'
        return render(request,'search.html',{'error_msg':error_msg})


    post_list  =  Host_table.objects.filter(ip_in=q)
    return render(request,'search.html',{'error_msg':error_msg,
                                         'post_list':post_list
                                         })

'''主机管理增加页面打开的实现'''
def add(request):
    return render(request,'article-detail.html')

'''添加机器页面逻辑'''
def addhost(request):


    result = {} # 创建一个空字典，以后存在更新状态是否OK

    if request.method == "POST":
        hostname = request.POST.get("hostname",None)
        ip_in = request.POST.get("ipin",None)
        ip_out = request.POST.get("ipout",None)
        mem = request.POST.get("mem",None)
        disk = request.POST.get("disk",None)
        cpu = request.POST.get("cpu",None)



        models.Host_table.objects.create(
            host_name=hostname,
            cpu = cpu,
            memory=mem,
            disk = disk,
            ip_in = ip_in,
            ip_out = ip_out,
            )

        result['statu'] = "success"
        result['host_name'] = hostname
        result['cpu'] = cpu
        result['memory'] = mem
        result['disk'] = disk
        result['ip_in'] = ip_in
        result['ip_out'] = ip_out



    return render(request, "article-detail.html",{"result":result})






def delete_host(request):
    if request.method == 'POST':
        print("welcome to post method")
        ip_in = request.POST.get("ip_in", None)
        print(ip_in)
        name =   Host_table.objects.filter(ip_in=ip_in).first()
        name.delete()



    return render(request,'add_success.html')



'''
elp 主页面

'''
def elp(request):
    host_list = Host_table.objects.all()   # 取出所有的主机页面信息
    paginator = Paginator(host_list,20,11)  # 实例化结果集，每页16条数据,少于15条就合并到上一页
    page = request.GET.get('page')          # 接收网页传递过来的 page

    try:
        customer = paginator.page(page)   # 传递给当前的html对象

    except PageNotAnInteger:

        customer = paginator.page(1)
    except EmptyPage:
        customer = paginator.page(paginator.num_pages)
    return render(request,'article-list2.html',{"host_list":customer})



def ulb(request):
    host_list = ULB.objects.all()   # 取出所有的主机页面信息
    paginator = Paginator(host_list,20,11)  # 实例化结果集，每页16条数据,少于15条就合并到上一页
    page = request.GET.get('page')          # 接收网页传递过来的 page

    try:
        customer = paginator.page(page)   # 传递给当前的html对象

    except PageNotAnInteger:

        customer = paginator.page(1)
    except EmptyPage:
        customer = paginator.page(paginator.num_pages)





    return render(request,'article-list3.html',{'host_list':customer})


'''主机管理增加页面打开的实现'''
def ulb111(request):
    return render(request,'article-detail2.html')


'''添加ULB页面逻辑'''
def addulb(request):


    result = {} # 创建一个空字典，以后存在更新状态是否OK

    if request.method == "POST":
        hostname = request.POST.get("hostname",None)
        ip_in = request.POST.get("ipin",None)
        ip_out = request.POST.get("ipout",None)



        models.ULB.objects.create(
            name=hostname,
            ulb_ip = ip_in,
            comment = ip_out,
            )

        result['statu'] = "success"
        result['host_name'] = hostname

        result['ip_in'] = ip_in
        result['ip_out'] = ip_out



    return render(request, "article-detail2.html",{"result":result})




#  主机页面 编辑页面操作
def edithost(request,value):
    result = {}  # 创建一个空字典，以后存在更新状态是否OK


        ####   value
    hostname =  Host_table.objects.filter(host_name=value)
    if request.method == "POST":
        obj_f = Project_form(request.POST, instance=hostname)
        if obj_f.is_valid():
            obj_f.save()
            status = 1
        else:
            status = 2
    else:
        obj_f = Project_form(instance=hostname)



    return render(request, "article-detail.html", {"result": result})


def del_publisher(request):
    pk = request.GET.get('id')
    print(pk)
    obj = models.Host_table.objects.get(ip_in=pk)

    obj.delete()

    return render(request,'article-list.html')


def UserGroup_edit(request, ids):

    obj = Host_table.objects.filter(id=ids)   ## 根据url传递的ids，来查询obj
    return  render(request,'test.html',{'obj':obj})





# 查看disk 目录大小




def gen_disk(request,ids):
    obj = Host_table.objects.filter(id=ids)   ## 根据url传递的ids，来查询obj

    for i in obj:

        ipaddress = i.ip_in  # 获取出对应的IP地址

        ## 执行本地目录的脚本文件:






        ##11、9 张涛更新

        a = AnsibleApi()
        host_list = ['10.25.97.96']
        tasks_list = [
            dict(action=dict(module='command', args='ls')),
        ]
        a.runansible(host_list, tasks_list)
        a.playbookrun(playbook_path=['/etc/ansible/test.yml'])

    return  render(request,'gen.html',{'obj':obj})






def UserGroup_delete(request,ids):
    obj = Host_table.objects.filter(id=ids)   ## 根据url传递的ids，来查询obj

    obj.delete()
    return  render(request,'delete.html',{'obj':obj})


## 清理磁盘所用到的测试函数哦IMPORT
import paramiko
def disk(request,ids):

    id = Host_table.objects.filter(id=ids)  # 获取对应的主机数据库id
    for i in id:
        # ip = i.ip_in    # 获得ip地址
        ip = '192.168.11.57'
        name = 'root'
        passwd = 'zhangtao@123'

        # 连接 linux 机器
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip,22,name,passwd)
        ssh.exec_command('echo "test" >> /data/taotao.txt')
        ssh.close()



    return render(request,'disk.html',{'id':id})

def update(request):
    ##  主机管理的页面更新按钮，远程控制我们的python脚本？

    ip = '192.168.11.57'
    name = 'root'
    passwd = 'zhangtao@123'

    # 连接 linux 机器
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip, 22, name, passwd)

    aaa = ssh.exec_command('/usr/bin/python3  /home/monitor/cmdb/update_host.py')


    return HttpResponse("准备开始更新主机数据，请耐心等待哦")

# ansible web 相关开发

from   service.forms import ProjectFrom  # 导入对应的forms表单

def project_index(request):
    all_project = project.objects.all()  # 查询数据
    return render(request,'project_index.html',{'all_project':all_project})


def ansible(request):
    all_project = project.objects.all()
    return render(request,'ansible.html',{'all_project':all_project})



#####======== test 弹出框:
from django.shortcuts import render

def p1(request):
    return render(request,"p1.html")

def p2(request):
    if request.method == "GET":
        return render(request,"p2.html")
    elif request.method == "POST":
        city =request.POST.get("city")
        print(city)
        return render(request,"popup_response.html",{"city":city})


## 自动化磁盘管理页面
def automation_disk(request):
    host_list = Host_table.objects.all()  # 取出所有的主机页面信息
    paginator = Paginator(host_list, 15, 16)  # 实例化结果集，每页16条数据,少于15条就合并到上一页
    page = request.GET.get('page')  # 接收网页传递过来的 page

    try:
        customer = paginator.page(page)  # 传递给当前的html对象

    except PageNotAnInteger:

        customer = paginator.page(1)
    except EmptyPage:
        customer = paginator.page(paginator.num_pages)
    return render(request, 'automation_disk.html', {"host_list": customer})



