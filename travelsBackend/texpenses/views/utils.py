# -*- coding: utf-8 -*-
import pytz
import uuid
from os import path

from django.template.loader import get_template
from django.template import RequestContext
from django.http import HttpResponse
from django.template import loader, Context
from django.conf import settings
from django.core.cache import cache
from weasyprint import HTML
from rest_framework.exceptions import PermissionDenied


def render_template2pdf(request, data, template_path,
                        default_report_name='report.pdf'):

    html_template = get_template(template_path)

    rendered_html = html_template.render(
        RequestContext(request, data)).encode(encoding="UTF-8")
    pdf_file = HTML(string=rendered_html,
                    base_url=request.build_absolute_uri()).write_pdf()

    http_response = HttpResponse(pdf_file, content_type='application/pdf')
    http_response['Content-Disposition'] = 'filename="' +\
        default_report_name + '"'
    return http_response


def render_template2csv(data, template_path, default_report_name='petition',
                        to_file=False):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="' +\
        default_report_name + '".csv"'
    t = loader.get_template(template_path)
    c = Context(data)
    content = t.render(c)
    if to_file:
        return content
    response.write(content)
    return response


def get_compensation_cost(travel_info):
    return sum([travel_obj.compensation_cost()
                for travel_obj in travel_info])


def get_compensation_days(travel_info):
    return sum([travel_obj.compensation_days_manual
                for travel_obj in travel_info])


def get_accommodation_cost(travel_info):
    return sum([travel_obj.overnight_cost()
                for travel_obj in travel_info])


def get_overnights(travel_info):
    return sum([travel_obj.overnights_num_manual
                for travel_obj in travel_info])


def get_overnights_sum_cost_string(travel_info):
    return '+'.join(
        [str(ti.accommodation_total_cost).replace('.', ',') +
        ' ευρώ (' + str(ti.overnights_num_manual)  +
        (' ημέρες)' if ti.overnights_num_manual > 1 else ' ημέρα)')
            for ti in travel_info]
    )


def get_compensation_levels_string(travel_info):
    return '+'.join(
        ['(' + str(ti.compensation_days_manual).replace('.', ',') +
        (' ημέρες x ' if ti.compensation_days_manual > 1 else ' ημέρα x ') +
        str(ti.compensation_cost_single_day()).replace('.', ',') + ')'
            for ti in travel_info]
    )


def get_means_of_transport(travel_info):
    return ','.join([travel_obj.get_means_of_transport_display()
                     for travel_obj in travel_info])


def get_transportation_cost(travel_info):
    return sum([travel_obj.transportation_cost
                for travel_obj in travel_info])

def get_arrival_points(travel_info):
    return ','.join([t.arrival_point.name for t in travel_info])


def get_local_depart_date(travel_obj):
    city = travel_obj.departure_point
    city_timezone = pytz.timezone(city.timezone)
    return travel_obj.depart_date.astimezone(city_timezone)


def get_local_return_date(travel_obj):
    city = travel_obj.arrival_point
    city_timezone = pytz.timezone(city.timezone)
    return travel_obj.return_date.astimezone(city_timezone)


def get_local_task_start_date(petition):
    task_start = petition.task_start_date
    travel_infos = list(petition.travel_info.all())

    # If task starts before, take first city's timezone
    city = travel_infos[0].arrival_point

    for travel in travel_infos:
        if task_start >= travel.depart_date and task_start <= travel.return_date:
            city = travel.arrival_point

    city_timezone = pytz.timezone(city.timezone)
    return petition.task_start_date.astimezone(city_timezone)


def get_local_task_end_date(petition):
    task_end = petition.task_end_date
    travel_infos = list(petition.travel_info.all())

    # If task starts after, take last city's timezone
    city = travel_infos[-1].arrival_point

    for travel in travel_infos:
        if task_end >= travel.depart_date and task_end <= travel.return_date:
            city = travel.arrival_point

    city_timezone = pytz.timezone(city.timezone)
    return petition.task_end_date.astimezone(city_timezone)


def escape(payload):
    if (payload and isinstance(payload, basestring) and
       payload[0] in ('@', '+', '-', '=', '|', '%')):
        payload = payload.replace("|", "\|")
        payload = "'" + payload
    return payload


def write_row(sheet, datarow, row):
    col = 0
    for d in datarow:
        sheet.write(row, col, escape(d))
        col += 1

FILE_TOKEN_TIMEOUT = getattr(settings, 'FILE_TOKEN_TIMEOUT', 60)

def generate_file_token(user, file):
    if not user.is_authenticated():
        raise PermissionDenied()

    token = 'download-' + str(uuid.uuid4())
    file_id = file.pk
    cache.set(token, file_id, FILE_TOKEN_TIMEOUT)
    return token

def consume_file_token(token):
    file_id = cache.get(token)
    if file_id is None:
        raise PermissionDenied()
    cache.delete(token)
    return file_id

def safe_path_join(base, path, sep=path.sep):
    safe_path = sep.join(x for x in path.split(sep) if x and x != '..')
    return base.rstrip(sep) + sep + safe_path

def urljoin(*args):
    return path.join(args[0], *map(lambda x: x.lstrip('/'), args[1:]))
