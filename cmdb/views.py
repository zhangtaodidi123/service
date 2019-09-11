from django.shortcuts import render
from .models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render,render_to_response,HttpResponse
from cmdb.models import Host_table
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger  # 分页用到的几个模块
from  cmdb import  models


def index(request):
    return render(request, 'index.html')

def welcome(request):
    return render(request,'welcome.html')



'''获取主机管理页面信息并返回'''
def article(request):


    host_list = Host_table.objects.all()   # 取出所有的主机页面信息
    paginator = Paginator(host_list,16,11)  # 实例化结果集，每页16条数据,少于15条就合并到上一页
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
    paginator = Paginator(host_list,16,11)  # 实例化结果集，每页16条数据,少于15条就合并到上一页
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
    paginator = Paginator(host_list,16,11)  # 实例化结果集，每页16条数据,少于15条就合并到上一页
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


