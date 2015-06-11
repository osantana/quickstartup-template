# coding: utf-8


from django.db import migrations

from ..bootstrap import bootstrap_website_pages


class Migration(migrations.Migration):
    dependencies = [
        ('website', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='page',
            old_name='template',
            new_name='template_name',
        ),
        migrations.RunPython(bootstrap_website_pages)
    ]
