# Generated by Django 3.1.3 on 2020-12-16 05:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TVSapp', '0011_task_start_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='start_time',
        ),
    ]
