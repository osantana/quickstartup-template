# coding: utf-8


from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('slug', models.SlugField(blank=True, unique=True, max_length=255,
                                          help_text='URL Path. Example: about for /about/')),
                ('template',
                 models.CharField(help_text='Template filename. Example: website/about.html', max_length=255)),
                ('login_required', models.BooleanField(default=False)),
            ],
        ),
    ]
