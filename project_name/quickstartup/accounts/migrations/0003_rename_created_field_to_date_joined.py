# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_remove_user_activation_key'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='created',
            new_name='date_joined',
        ),
    ]
