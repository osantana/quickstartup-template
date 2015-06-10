# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('status', models.CharField(default='N', verbose_name='status', choices=[('N', 'New'), ('O', 'Ongoing'), ('R', 'Resolved'), ('C', 'Closed'), ('I', 'Invalid')], max_length=1)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('email', models.EmailField(max_length=255, verbose_name='email')),
                ('phone', models.CharField(max_length=100, verbose_name='phone', blank=True)),
                ('message', models.TextField(verbose_name='message')),
            ],
        ),
    ]
