# -*- coding: utf-8 -*-

from django.template.loader import get_template
from django.template import RequestContext
from django.http import HttpResponse
from django.template import loader, Context
from weasyprint import HTML


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
    return sum([travel_obj.accommodation_cost
                for travel_obj in travel_info])


def get_overnights(travel_info):
    return sum([travel_obj.overnights_num_manual
                for travel_obj in travel_info])


def get_overnights_sum_cost_string(travel_info):
    return '+'.join(["(" + str(travel_info_object.overnights_num_manual) +
                     u' ημέρες x ' +
                     str(travel_info_object.accommodation_cost) + ')'
                     for travel_info_object in travel_info])


def get_compensation_levels_string(travel_info):
    return '+'.join(["(" + str(travel_info_object.compensation_days_manual) +
                     u' ημέρες x ' +
                     str(travel_info_object.compensation_level()) + ')'
                     for travel_info_object in travel_info])


def get_means_of_transport(travel_info):
    return ','.join([travel_obj.get_means_of_transport_display()
                     for travel_obj in travel_info])


def get_transportation_cost(travel_info):
    return sum([travel_obj.transportation_cost
                for travel_obj in travel_info])
