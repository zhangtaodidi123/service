'''froms 表单python文件'''


from django import forms



class login_form(forms.Form):
    username = forms.CharField(label='用户名', min_length=2, max_length=5, error_messages={"required": "用户名不能为空"});
    pwd = forms.CharField(label="密码");