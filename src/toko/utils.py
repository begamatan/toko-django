import logging

from django.core.mail import BadHeaderError, send_mail

# helper
logger = logging.getLogger('django')

def send_email(subject, message, from_email, to_email):
    if subject and message and from_email:
        try:
            send_mail(subject, message, from_email, to_email)
        except BadHeaderError:
            logger.error('Invalid headers found')
        logger.info('Email send')
    else:
        logger.error('Make sure all fields are entered and valid')