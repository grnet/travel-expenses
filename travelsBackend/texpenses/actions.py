# -*- coding: utf-8 -*-
import logging
from django.conf import settings
from django.core.mail import EmailMessage, get_connection
from django.template.loader import render_to_string
from rest_framework import status
from texpenses.models import Petition
from datetime import datetime


DATE_FORMAT = '%Y-%m-%d'
SENDER = settings.SERVER_EMAIL
SECRETARY_EMAIL = settings.SECRETARY_EMAIL
CONTROLLER_EMAIL = settings.CONTROLLER_EMAIL
EMAIL_TEMPLATES = {
    'SUBMISSION': ('submission.txt', 'Υποβολή αίτησης μετακίνησης'),
    'CANCELLATION': ('cancellation.txt',
                     'Αναίρεση υποβολής αίτησης μετακίνησης'),
    'PETITION_PRESIDENT_APPROVAL': ('petition_president_approval.txt',
                                    'Έγκριση μετακίνησης απο τον πρόεδρο.'),

    'USER_COMPENSATION_SUBMISSION': ('user_compensation_submission.txt',
                                    "Υποβολή αίτησης αποζημίωσης"
                                     " από μετακινούμενο."),

    'USER_COMPENSATION_CANCELLATION': ('user_compensation_cancellation.txt',
                                    "Αναίρεση υποβολής αίτησης αποζημίωσης"
                                     " από μετακινούμενο."),

    'COMPENSATION_PRESIDENT_APPROVAL': ('compensation_president_approval.txt',
                                    'Έγκριση αποζημίωσης απο τον πρόεδρο.'),
    'COMPENSATION_ALERT': ('compensation_alert.txt',
                           'Ενημέρωση σύνταξης αίτησης αποζημίωσης.')
}

logger = logging.getLogger(__name__)


def send_email(subject, template, params, sender, to, bcc=(), cc=(),
               fail_silently=True):
    content = render_to_string(template, params)
    prefix = '<Travel Expenses> '
    try:
        EmailMessage(
            prefix + subject, content, sender, to=to, bcc=bcc, cc=cc,
            connection=get_connection()).send(fail_silently)
    except Exception as e:
        logger.error(e)


def inform(petition, action, target_user, inform_controller):
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
    # We take the first `travel_info` object, because multiple destinations
    # are not supported at the moment.
    travel_info = petition.travel_info.all()[0]
    params = {
        'first_name': petition.first_name,
        'last_name': petition.last_name,
        'dse': petition.dse,
        'project_name': petition.project,
        'departure_point': travel_info.departure_point,
        'arrival_point': travel_info.arrival_point,
        'start_date': str(petition.task_start_date),
        'end_date': str(petition.task_end_date),
        'reason': petition.reason,
    }
    cc = (petition.user.email,)
    to = (petition.project.manager_email, SECRETARY_EMAIL)\
        if not inform_controller else (petition.project.manager_email,\
                                   SECRETARY_EMAIL,CONTROLLER_EMAIL)
    if target_user:
        cc = to
        to = (petition.user.email,)
    print subject,template,params,SENDER,to,cc

    send_email(subject, template, params, SENDER, to=to, cc=cc)


def inform_on_action(action, target_user=False, inform_controller=False):
    def inform_action(func):
        def wrapper(*args, **kwargs):
            obj = args[0]
            if obj.kwargs:
                instance = obj.get_object()
            response = func(*args, **kwargs)
            if response.status_code in [status.HTTP_303_SEE_OTHER,
                                        status.HTTP_201_CREATED,
                                        status.HTTP_200_OK]:
                if not obj.kwargs:
                    instance = Petition.objects.get(id=response.data['id'])
                inform(instance, action, target_user, inform_controller)
            return response
        return wrapper
    return inform_action


def compensation_alert():

    now = datetime.now().strftime(DATE_FORMAT)

    approved_petitions = Petition.objects.filter(status=\
                                               Petition.APPROVED_BY_PRESIDENT,\
                                                 compensation_alert=False)
    for petition in approved_petitions:
        travel_info = petition.travel_info.all()[0]
        return_date = travel_info.return_date.strftime(DATE_FORMAT)
        if return_date == now:
            inform(petition, action='COMPENSATION_ALERT', target_user=True,inform_controller=False)
            petition.compensation_alert = True
            petition.save()

