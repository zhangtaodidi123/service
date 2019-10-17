'''froms 表单python文件'''


from django import forms
from cmdb.models import Host_table


class login_form(forms.Form):
    username = forms.CharField(label='用户名', min_length=2, max_length=5, error_messages={"required": "用户名不能为空"});
    pwd = forms.CharField(label="密码")


## from 表单，编辑模块使用
class ProjectFrom(forms.ModelForm):
    class Meta:
        model = Host_table
        exclude = ("id",)
        widgets = {
            'host_name': forms.TextInput(attrs={'class': 'form-control'}),
            'etc': forms.TextInput(attrs={'class': 'form-control'}),
            'cpu': forms.TextInput(attrs={'class': 'form-control'}),
            'memory': forms.TextInput(attrs={'class': 'form-control'}),
            'disk': forms.TextInput(attrs={'class': 'form-control'}),
            'ip_in': forms.TextInput(attrs={'class': 'form-control'}),
            'ip_out': forms.TextInput(attrs={'class': 'form-control'})
        }

class UserGroup_form(forms.ModelForm):
    class Meta:
        model = Host_table
        exclude = ("id",)
        widgets = {
            'host_name': forms.TextInput(attrs={'class': 'form-control'}),
            'etc': forms.TextInput(attrs={'class': 'form-control'}),
            'cpu': forms.TextInput(attrs={'class': 'form-control'}),
            'memory': forms.TextInput(attrs={'class': 'form-control'}),
            'disk': forms.TextInput(attrs={'class': 'form-control'}),
            'ip_in': forms.TextInput(attrs={'class': 'form-control'}),
            'ip_out': forms.TextInput(attrs={'class': 'form-control'})
        }