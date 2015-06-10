# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(db_index=True, unique=True, max_length=255, verbose_name='email')),
                ('created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='created')),
                ('is_active', models.BooleanField(default=False, verbose_name='active')),
                ('is_staff', models.BooleanField(default=False, verbose_name='staff')),
                ('activation_key', models.CharField(db_index=True, max_length=40, verbose_name='activation key')),
                ('name', models.CharField(max_length=255, blank=True, null=True)),
                ('groups', models.ManyToManyField(blank=True, to='auth.Group', verbose_name='groups', related_name='user_set', related_query_name='user', help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.')),
                ('user_permissions', models.ManyToManyField(blank=True, to='auth.Permission', verbose_name='user permissions', related_name='user_set', related_query_name='user', help_text='Specific permissions for this user.')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
