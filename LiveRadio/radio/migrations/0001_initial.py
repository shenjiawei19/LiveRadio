# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-08-16 08:32
from __future__ import unicode_literals

import django.contrib.auth.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0007_alter_validators_add_error_messages'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=30, unique=True, validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username. This value may contain only letters, numbers and @/./+/-/_ characters.')], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=30, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='\u7528\u6237\u7f16\u53f7')),
                ('level', models.IntegerField(default=0, verbose_name='\u7528\u6237\u6743\u9650')),
                ('is_delete', models.IntegerField(default=0, verbose_name='\u5220\u9664\u6807\u5fd7\u4f4d')),
            ],
            options={
                'ordering': ['-id'],
                'verbose_name_plural': '\u7528\u6237',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='\u8282\u70b9\u7c7b\u7f16\u53f7')),
                ('name', models.CharField(max_length=30, verbose_name='\u5206\u7c7b\u540d\u79f0')),
            ],
            options={
                'ordering': ['id'],
                'verbose_name_plural': '\u8282\u70b9\u7c7b\u578b',
            },
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='\u7528\u6237\u7ec4\u7f16\u53f7')),
                ('name', models.CharField(max_length=30, verbose_name='\u7528\u6237\u7ec4\u5206\u7c7b')),
            ],
            options={
                'ordering': ['id'],
                'verbose_name_plural': '\u7528\u6237\u7ec4',
            },
        ),
        migrations.CreateModel(
            name='Node',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='\u8282\u70b9\u7f16\u53f7')),
                ('name', models.CharField(blank=True, max_length=30, unique=True, verbose_name='\u8282\u70b9\u540d')),
                ('node_status', models.IntegerField(default=0, verbose_name='\u8282\u70b9\u72b6\u6001')),
                ('node_info', models.CharField(blank=True, max_length=20, null=True, verbose_name='\u72b6\u6001\u63cf\u8ff0')),
                ('is_delete', models.IntegerField(default=0, verbose_name='\u5220\u9664\u6807\u5fd7\u4f4d')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='radio.Category', verbose_name='\u5206\u7c7b\u540d\u79f0')),
            ],
            options={
                'ordering': ['id'],
                'verbose_name_plural': '\u8282\u70b9',
            },
        ),
        migrations.CreateModel(
            name='Node_detail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.URLField(blank=True, null=True, verbose_name='\u8282\u70b9\u5730\u5740')),
                ('channel', models.IntegerField(blank=True, null=True, verbose_name='\u9891\u9053\u53f7')),
                ('node_status', models.IntegerField(default=0, verbose_name='\u8282\u70b9\u72b6\u6001')),
                ('ip_info', models.CharField(blank=True, max_length=20, null=True, verbose_name='\u72b6\u6001\u63cf\u8ff0')),
                ('is_delete', models.IntegerField(default=0, verbose_name='\u5220\u9664\u6807\u5fd7\u4f4d')),
                ('method', models.CharField(max_length=200, verbose_name='\u91cd\u542f\u65b9\u5f0f')),
                ('node_name', models.ForeignKey(max_length=30, on_delete=django.db.models.deletion.CASCADE, to='radio.Node', verbose_name='\u8282\u70b9\u540d')),
            ],
            options={
                'verbose_name_plural': '\u8282\u70b9\u8be6\u60c5',
            },
        ),
        migrations.CreateModel(
            name='Op_log',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='\u64cd\u4f5c\u5e8f\u53f7')),
                ('op_name', models.CharField(max_length=200, verbose_name='\u64cd\u4f5c\u4eba\u5458')),
                ('op_detail', models.CharField(blank=True, max_length=200, null=True, verbose_name='\u64cd\u4f5c\u8be6\u60c5')),
                ('op_time', models.DateTimeField(auto_now_add=True, verbose_name='\u64cd\u4f5c\u65f6\u95f4')),
            ],
            options={
                'verbose_name_plural': '\u64cd\u4f5c\u8bb0\u5f55',
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='\u4efb\u52a1\u7f16\u53f7')),
                ('title', models.CharField(max_length=50, unique=True, verbose_name='\u4efb\u52a1\u6807\u9898')),
                ('description', models.CharField(max_length=200, verbose_name='\u4efb\u52a1\u63cf\u8ff0')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('start_time', models.DateTimeField(verbose_name='\u5f00\u59cb\u65f6\u95f4')),
                ('update_time', models.DateTimeField(auto_now_add=True, verbose_name='\u4fee\u6539\u65f6\u95f4')),
                ('finish_time', models.DateTimeField(verbose_name='\u5b8c\u6210\u65f6\u95f4')),
                ('channel', models.IntegerField(verbose_name='\u9891\u9053\u53f7')),
                ('task_status', models.IntegerField(default=0, verbose_name='\u72b6\u6001')),
                ('is_delete', models.IntegerField(default=0, verbose_name='\u5220\u9664\u6807\u5fd7\u4f4d')),
            ],
            options={
                'ordering': ['id'],
                'verbose_name_plural': '\u76f4\u64ad\u4efb\u52a1',
            },
        ),
        migrations.AddField(
            model_name='user',
            name='group',
            field=models.ForeignKey(blank=True, max_length=30, null=True, on_delete=django.db.models.deletion.CASCADE, to='radio.Group', verbose_name='\u7528\u6237\u6240\u5c5e\u7ec4'),
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
    ]
