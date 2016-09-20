# -*- coding: utf-8 -*-
import logging
from django.conf import settings
from django.core.mail import EmailMessage, get_connection
from django.template.loader import render_to_string
from rest_framework import status


SENDER = settings.SERVER_EMAIL
SECRETARY_EMAIL = settings.SECRETARY_EMAIL
EMAIL_TEMPLATES = {
    'SUBMISSION': ('submission.txt', 'Υποβολή αίτησης μετακίνησης'),
    'CANCELLATION': ('cancellation.txt',
                     'Αναίρεση υποβολής αίτησης μετακίνησης')
}

logger = logging.getLogger(__name__)


def send_email(subject, template, params, sender, to, bcc=(), cc=(),
               fail_silently=True):
    content = render_to_string(template, params)
    try:
        EmailMessage(
            subject, content, sender, to=to, bcc=bcc, cc=cc,
            connection=get_connection()).send(fail_silently)
    except Exception as e:
        logger.error(e)


def inform(petition, action):
    """
    Inform about action applied to a specific petition with an informative
    email.

    Recipients of that notification are, user related to that petition,
    secretary and project manager.
    """
    template, subject = EMAIL_TEMPLATES.get(action, (None, None))
    assert template is not None and subject is not None
    # TODO alert in case of invalid action?
    # TODO Add more parameters and template wording.
    travel_info = petition.travel_info.all()[0]
    params = {
        'first_name': petition.first_name,
        'last_name': petition.last_name,
        'dse': petition.dse,
        'project_name': petition.project,
        'departure_point': travel_info.departure_point,
        'arrival_point': travel_info.arrival_point,
        'start_date': petition.task_start_date,
        'end_date': petition.task_end_date,
        'reason': petition.reason,
    }
    cc = (petition.user.email,)
    to = (petition.project.manager_email, SECRETARY_EMAIL)
    send_email(subject, template, params, SENDER, to=to, cc=cc)


def inform_on_action(action):
    def inform_action(func):
        def wrapper(*args, **kwargs):
            instance = args[0].get_object()
            response = func(*args, **kwargs)
            if response.status_code in [status.HTTP_303_SEE_OTHER,
                                        status.HTTP_201_CREATED]:
                inform(instance, action)
            return response
        return wrapper
    return inform_action
