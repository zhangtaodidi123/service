"""
urls

"""
from django.contrib import admin
from django.urls import path
from cmdb.views import index
from cmdb import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/',views.index),
    path('index/welcome.html',views.welcome),
    path('index/article-list.html',views.article),
    path('index/article-list2.html',views.elp),
    path('index/article-list3.html',views.ulb),
    path('search/',views.search),
    path('addhost/',views.addhost),
    path('addulb/',views.addulb),
    path('index/add',views.add),
    path('index/ulb',views.ulb111),
    path('delete/',views.delete_host)
]
