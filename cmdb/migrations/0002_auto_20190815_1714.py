# Generated by Django 2.2.4 on 2019-08-15 09:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cmdb', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='host_table',
            name='create_date',
        ),
        migrations.RemoveField(
            model_name='host_table',
            name='update_date',
        ),
    ]