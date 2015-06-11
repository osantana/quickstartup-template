# coding: utf-8


def bootstrap_website_pages(apps, schema_editor=None):
    page_model = apps.get_model("website", "Page")
    pages = [
        {"slug": "", "template_name": "website/index.html"},
        {"slug": "privacy", "template_name": "website/privacy.html"},
        {"slug": "terms", "template_name": "website/terms.html"},
    ]

    for page in pages:
        page_model.objects.get_or_create(**page)
