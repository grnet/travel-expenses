from django.template.loader import get_template
from django.template import RequestContext
from django.http import HttpResponse
from weasyprint import HTML


class PDFRenderer(object):

    def render_template2pdf(self, request, data, template_path,
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
