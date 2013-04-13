# coding: utf-8


import os
import re
import email.charset

from hashlib import sha512
from datetime import datetime, timedelta
from email.mime.image import MIMEImage

from django.conf import settings
from django.core.mail import SafeMIMEMultipart, SafeMIMEText
from django.template import loader


INLINE_SCHEME = re.compile(r' src="inline://(?P<path>.*?)" ?', re.MULTILINE)

DEFAULT_CHARSET = "utf-8"

email.charset.add_charset(DEFAULT_CHARSET, email.charset.SHORTEST, None, None)


class HTMLMessage(object):
    def __init__(self, from_, to_, subject_template, text_template_name, html_template_name, context):
        self.from_ = from_
        self.to_ = to_

        subject = loader.render_to_string(subject_template, context)
        self.subject = ''.join(subject.splitlines())

        context.update({"subject": subject})
        self.context = context

        self.text = loader.render_to_string(text_template_name, context)
        self.html = loader.render_to_string(html_template_name, context)

    def message(self):
        mail = SafeMIMEMultipart("related")
        mail.preamble = "This is a multi-part message in MIME format."

        mail["Subject"] = self.subject
        mail["From"] = self.from_
        mail["To"] = self.to_

        paths = []

        def repl(match):
            paths.append(match.group("path"))
            return ' src="cid:image-%05d" ' % (len(paths),)

        html = re.sub(INLINE_SCHEME, repl, self.html)

        alternative = SafeMIMEMultipart("alternative")
        alternative.attach(SafeMIMEText(self.text, "plain", charset=DEFAULT_CHARSET))
        alternative.attach(SafeMIMEText(html, "html", charset=DEFAULT_CHARSET))
        mail.attach(alternative)

        for index, path in enumerate(paths):
            if path.startswith(settings.STATIC_URL):
                path = path[len(settings.STATIC_URL):]

            path = os.path.join(settings.STATIC_ROOT, path)

            with open(path, "rb") as fp:
                image = MIMEImage(fp.read())

            image.add_header('Content-ID', '<image-%05d>' % (index + 1))
            mail.attach(image)

        return mail


def get_anticaptcha_tokens():
    date_format = "%Y-%m-%d"

    today = datetime.utcnow().strftime(date_format)
    yesterday = (datetime.utcnow() - timedelta(1)).strftime(date_format)

    secrets = (
        settings.SECRET_KEY + today,
        settings.SECRET_KEY + yesterday,
    )

    return [sha512(secret).hexdigest() for secret in secrets]
