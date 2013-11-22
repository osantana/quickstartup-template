# coding: utf-8


from datetime import datetime, timedelta
from hashlib import sha512

from django.conf import settings


def get_antispam_tokens():
    date_format = "%Y-%m-%d"

    today = datetime.utcnow().strftime(date_format)
    yesterday = (datetime.utcnow() - timedelta(1)).strftime(date_format)

    secrets = (
        settings.SECRET_KEY + today,
        settings.SECRET_KEY + yesterday,
    )

    return [sha512(secret).hexdigest() for secret in secrets]
