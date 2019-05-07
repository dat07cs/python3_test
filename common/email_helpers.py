import logging

from django.conf import settings
from django.core.mail import EmailMessage


_logger = logging.getLogger('main')


def send_email(subject, content, files, recipients, email_server=settings.SERVER_EMAIL):
    msg = EmailMessage(subject, content, email_server, recipients)
    for filename in files:
        with open(filename, 'rb') as f:
            data = f.read()
        msg.attach(filename.split("/")[-1], data)
    if getattr(settings, 'SEND_EMAIL', True) is False:
        _logger.info('email sent | %s | %s | %s | %s |', subject, recipients, content, files)
        return 1
    else:
        return msg.send()
