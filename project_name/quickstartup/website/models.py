# coding: utf-8


from django.db import models
from django.template import loader
from django.utils.translation import ugettext_lazy as _


class Page(models.Model):
    slug = models.SlugField(max_length=255, blank=True, unique=True, db_index=True,
                            help_text=_("URL Path. Example: about for /about/"))
    template_name = models.CharField(max_length=255, help_text=_("Template filename. Example: website/about.html"))
    login_required = models.BooleanField(default=False)

    @property
    def path(self):
        return "/{}/".format(self.slug) if self.slug else "/"

    def __str__(self):
        return self.path

    def __repr__(self):
        return "<Page: {}>".format(self.path)

    def get_absolute_url(self):
        return self.path

    @property
    def template(self):
        return loader.get_template(self.template_name)
