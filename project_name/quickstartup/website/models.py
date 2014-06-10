# coding: utf-8


from django.db import models
from django.utils.translation import ugettext_lazy as _


class Page(models.Model):
    slug = models.SlugField(max_length=255, blank=True, help_text=_("URL Path. Example: about for /about/"))
    variation = models.PositiveIntegerField(default=0, help_text=_("A/B test variation"))
    template = models.CharField(max_length=255, help_text=_("Template filename. Example: website/about.html"))
    login_required = models.BooleanField(default=False)

    class Meta:
        unique_together = (("slug", "variation"),)
        index_together = (("slug", "variation"),)

    @property
    def path(self):
        return "/{}/".format(self.slug) if self.slug else "/"

    def __repr__(self):
        return "<Page: {}?v={}>".format(self.path, self.variation)

    def get_absolute_url(self):
        return self.path
