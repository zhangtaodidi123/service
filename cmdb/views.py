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
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.executor.playbook_executor import PlaybookExecutor
from ansible.plugins.callback import CallbackBase
import ansible.constants as C
from ansible import context
from optparse import Values
from ansible.utils.sentinel import Sentinel


class ResultCallback(CallbackBase):
    def __init__(self, *args, **kwargs):
        # super(ResultsCollector, self).__init__(*args, **kwargs)
        self.host_ok = {}
        self.host_unreachable = {}
        self.host_failed = {}

    def v2_runner_on_unreachable(self, result):
        self.host_unreachable[result._host.get_name()] = result

    def v2_runner_on_ok(self, result, *args, **kwargs):
        self.host_ok[result._host.get_name()] = result

    def v2_runner_on_failed(self, result, *args, **kwargs):
        self.host_failed[result._host.get_name()] = result


class AnsibleApi(object):
    def __init__(self):
        self.options = {'verbosity': 0, 'ask_pass': False, 'private_key_file': None, 'remote_user': None,
                        'connection': 'smart', 'timeout': 10, 'ssh_common_args': '', 'sftp_extra_args': '',
                        'scp_extra_args': '', 'ssh_extra_args': '', 'force_handlers': False,
                        'flush_cache': None,
                        'become': False, 'become_method': 'sudo', 'become_user': None, 'become_ask_pass': False,
                        'tags': ['all'], 'skip_tags': [], 'check': False, 'syntax': None, 'diff': False,
                        'inventory': '/etc/ansible/hosts',
                        'listhosts': None, 'subset': None, 'extra_vars': [], 'ask_vault_pass': False,
                        'vault_password_files': [], 'vault_ids': [], 'forks': 5, 'module_path': None,
                        'listtasks': None,
                        'listtags': None, 'step': None, 'start_at_task': None, 'args': ['fake']}
        self.ops = Values(self.options)

        self.loader = DataLoader()
        self.passwords = dict()
        self.results_callback = ResultCallback()
        self.inventory = InventoryManager(loader=self.loader, sources=[self.options['inventory']])
        self.variable_manager = VariableManager(loader=self.loader, inventory=self.inventory)

    def runansible(self, host_list, task_list):

        play_source = dict(
            name="Ansible Play",
            hosts=host_list,
            gather_facts='no',
            tasks=task_list
        )
        play = Play().load(play_source, variable_manager=self.variable_manager, loader=self.loader)

        tqm = None
        try:
            tqm = TaskQueueManager(
                inventory=self.inventory,
                variable_manager=self.variable_manager,
                loader=self.loader,
                # options=self.ops,
                passwords=self.passwords,
                stdout_callback=self.results_callback,
                run_additional_callbacks=C.DEFAULT_LOAD_CALLBACK_PLUGINS,
                run_tree=False,
            )
            result = tqm.run(play)
        finally:
            if tqm is not None:
                tqm.cleanup()
                # shutil.rmtree(C.DEFAULT_LOCAL_TMP, True)

        results_raw = {}
        results_raw['success'] = {}
        results_raw['failed'] = {}
        results_raw['unreachable'] = {}

        for host, result in self.results_callback.host_ok.items():
            results_raw['success'][host] = json.dumps(result._result)

        for host, result in self.results_callback.host_failed.items():
            results_raw['failed'][host] = result._result['msg']

        for host, result in self.results_callback.host_unreachable.items():
            results_raw['unreachable'][host] = result._result['msg']

        print(results_raw)

    def playbookrun(self, playbook_path):

        context._init_global_context(self.ops)

        playbook = PlaybookExecutor(playbooks=playbook_path,
                                    inventory=self.inventory,
                                    variable_manager=self.variable_manager,
                                    loader=self.loader, passwords=self.passwords)
        result = playbook.run()
        return result

    a = AnsibleApi()
    host_list = ['10.25.97.96']
    tasks_list = [
        dict(action=dict(module='command', args='ls')),
    ]
    a.runansible(host_list, tasks_list)
    a.playbookrun(playbook_path=['/etc/ansible/test.yml'])




def index(request):
    return render(request, 'index.html')

def welcome(request):
    return render(request,'welcome.html')



'''获取主机管理页面信息并返回'''
def article(request):


    host_list = Host_table.objects.all()   # 取出所有的主机页面信息
    paginator = Paginator(host_list,20,16)  # 实例化结果集，每页16条数据,少于15条就合并到上一页
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



