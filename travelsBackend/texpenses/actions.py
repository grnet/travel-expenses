# -*- coding: utf-8 -*-
import logging
from django.conf import settings
from django.core.mail import EmailMessage, get_connection
from django.template.loader import render_to_string
from rest_framework import status
from texpenses.models import Petition
from datetime import timedelta
from django.utils import timezone
from apimas.drf import django_rest
from texpenses.api_conf.endpoint_confs import Configuration
from texpenses.api_conf.spec.spec import spec
import pprint

DATE_FORMAT = '%Y-%m-%d'
SENDER = settings.SERVER_EMAIL
SECRETARY_EMAIL = settings.SECRETARY_EMAIL
CONTROLLER_EMAIL = settings.CONTROLLER_EMAIL
EMAIL_TEMPLATES = {
    'SUBMISSION': ('submission.txt', 'Υποβολή αίτησης μετακίνησης'),
    'CANCELLATION': ('cancellation.txt',
                     'Αναίρεση υποβολής αίτησης μετακίνησης'),
    'PETITION_PRESIDENT_APPROVAL': ('petition_president_approval.txt',
                                    'Έγκριση μετακίνησης από τον Πρόεδρο.'),
    'PETITION_WITHDRAWAL': ('withdrawal.txt',
                            'Απόσυρση αίτησης μετακίνησης.'),
    'CANCEL_PETITION_WITHDRAWAL': ('cancel_withdrawal.txt',
                                   'Ακύρωση απόσυρσης αίτησης μετακίνησης.'),

    'USER_COMPENSATION_SUBMISSION': ('user_compensation_submission.txt',
                                    "Υποβολή αίτησης αποζημίωσης"
                                     " από μετακινούμενο."),

    'USER_COMPENSATION_CANCELLATION': ('user_compensation_cancellation.txt',
                                    "Αναίρεση υποβολής αίτησης αποζημίωσης"
                                     " από μετακινούμενο."),

    'COMPENSATION_PRESIDENT_APPROVAL': ('compensation_president_approval.txt',
                                        'Έγκριση αποζημίωσης από τον Πρόεδρο.'),
    'COMPENSATION_ALERT': ('compensation_alert.txt',
                           'Ενημέρωση σύνταξης αίτησης αποζημίωσης.')
}

logger = logging.getLogger(__name__)


def send_email(subject, template, params, sender, to, bcc=(), cc=(),
               fail_silently=True):
    content = render_to_string(template, params)
    prefix = '<Travel Expenses> '
    try:
        project_name = ' ['+params['project'].encode('utf-8')+']'
        message = EmailMessage(prefix + subject + project_name, content,
                               sender, to=to, bcc=bcc, cc=cc,
                               connection=get_connection()
                               )
        message.send(fail_silently)
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

    travel_info_first = petition.travel_info.first()
    travel_info_last = petition.travel_info.last()
    travel_info = petition.travel_info.all()

    params = {
        'first_name': petition.first_name,
        'last_name': petition.last_name,
        'dse': petition.dse,
        'travel_info': travel_info ,
        'project': petition.project.name,
        'departure_point': travel_info_first.departure_point.name \
        if travel_info_first else None,
        'arrival_point': travel_info_last.arrival_point.name \
        if travel_info_last else None,
        'timezone_arrival': travel_info_last.arrival_point.timezone,
        'timezone_depart': travel_info_first.departure_point.timezone,
        'task_start_date': petition.task_start_date,
        'task_end_date': petition.task_end_date,
        'reason': petition.reason,
        'user_recommendation': petition.user_recommendation,
    }
    cc = (petition.user.email,)
    to = (petition.project.manager.email, SECRETARY_EMAIL)\
        if not inform_controller else (petition.project.manager.email,\
                                   SECRETARY_EMAIL, CONTROLLER_EMAIL)
    if target_user:
        cc = to
        to = (petition.user.email,)

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

    inform_date = (timezone.now() - timedelta(days=1)).strftime(DATE_FORMAT)

    approved_petitions = Petition.objects.filter(
        status=Petition.APPROVED_BY_PRESIDENT, deleted=False,
        compensation_alert=False, withdrawn=False)

    for petition in approved_petitions:
        return_date = petition.travel_info.last().return_date.\
            strftime(DATE_FORMAT)
        if return_date == inform_date:
            if not petition.compensation_alert:
                inform(petition, action='COMPENSATION_ALERT', target_user=True,
                       inform_controller=False)
                petition.compensation_alert = True
                petition.save()


def pythonize_spec(spec):

    petitions = [spec['api']['petition-user-saved'],
                 spec['api']['petition-user-submitted'],
                 spec['api']['petition-secretary-saved'],
                 spec['api']['petition-secretary-submitted'],
                 spec['api']['petition-user-compensations'],
                 spec['api']['petition-secretary-compensations']
                 ]

    petition_base = {}
    travel_info_base = {}

    for idx, petition in enumerate(petitions):
        travel_info = petition['*']['travel_info']
        petition['*']['travel_info'] = {}

        if idx > 0:
           for key in petition_base['*'].keys():
               if petition['*'][key] == petition_base['*'][key]:
                   petition['*'].pop(key, None)
           for key in petition_base.keys():
               if petition[key] == petition_base[key]:
                   petition.pop(key, None)

           for key in travel_info_base['.structarray'].keys():
               if travel_info['.structarray'][key] == \
                       travel_info_base['.structarray'][key]:
                   travel_info['.structarray'].pop(key, None)
           for key in travel_info_base.keys():
               if travel_info[key] == travel_info_base[key]:
                   travel_info.pop(key, None)
        else:
            petition_base = petition
            travel_info_base = travel_info

        petition_file = open('petition'+str(idx)+'.py', 'w')
        travel_info_file = open('travel_info'+str(idx)+'.py', 'w')
        petition_file.write(pprint.pformat(petition, indent=1))
        travel_info_file.write(pprint.pformat(travel_info, indent=1))
        petition_file.close()
        travel_info_file.close()


def load_apimas_urls():

    adapter = django_rest.DjangoRestAdapter()

    configuration = Configuration(spec)
    configuration.configure_spec()

    adapter.construct(spec)
    return adapter.urls.values()
