"""
urls

"""
from django.contrib import admin
from django.urls import path,re_path
from cmdb.views import index
from cmdb import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/',views.index),
    path('index/welcome.html',views.welcome),
    path('index/ansible.html',views.ansible),
    path('ansible.html',views.ansible),
    path('index/article-list.html',views.article),
    path('index/article-list2.html',views.elp),
    path('index/article-list3.html',views.ulb),
    path('index/automation_disk.html',views.automation_disk),
    path('search/',views.search),
    path('addhost/',views.addhost),
    path('addulb/',views.addulb),
    path('index/add',views.add),
    path('index/ulb',views.ulb111),
    path('delete/',views.delete_host),
    path('del_publisher/',views.del_publisher),
    path('index/del_publisher',views.del_publisher),
    re_path('UserGroup/edit/(?P<ids>\d+)/$', views.UserGroup_edit, name='UserGroup_edit'),
    re_path('/cat/gen_disk/(?P<ids>\d+)/$', views.gen_disk, name='gen_disk'),
    re_path('UserGroup/delete/(?P<ids>\d+)/$', views.UserGroup_delete, name='UserGroup_delete'),
    re_path('UserGroup/disk/(?P<ids>\d+)/$', views.disk, name='disk'),
    path('UserGroup/update', views.update, name='update'),
    path('project/index/', views.project_index, name='project_index'),
    path('p1',views.p1),
    path('p2.html',views.p2),


]
