from django.template.loader import get_template
from django.template import RequestContext
from django.http import HttpResponse
from weasyprint import HTML


def pdf(request):
    html_template = get_template('texpenses/base.html')

    mylist = {'shit1', 'shit2', 'shit3'}

    rendered_html = html_template.render(
        RequestContext(request, {'data': mylist})).encode(encoding="UTF-8")

    # pdf_file = HTML(string=rendered_html).write_pdf()

    # http_response = HttpResponse(pdf_file, content_type='application/pdf')
    # http_response['Content-Disposition'] = 'filename="report.pdf"'

    # return http_response
    return HttpResponse(rendered_html)
