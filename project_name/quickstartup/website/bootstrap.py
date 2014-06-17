# coding: utf-8


def bootstrap_website_pages(apps, schema_editor=None):
    page_model = apps.get_model("website", "Page")
    pages = [
        {"slug": "", "template": "website/index.html"},
        {"slug": "privacy", "template": "website/privacy.html"},
        {"slug": "terms", "template": "website/terms.html"},
    ]

    for page in pages:
        page_model.objects.get_or_create(**page)
