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


def get_transportation_cost(travel_info):
    return sum([travel_obj.transportation_cost for travel_obj in travel_info])


def get_compensation_cost(travel_info):
    return sum([travel_obj.compensation_cost() for travel_obj in travel_info])
