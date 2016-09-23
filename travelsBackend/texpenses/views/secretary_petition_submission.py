from django.core.exceptions import PermissionDenied
from rest_framework import status
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework.reverse import reverse
from texpenses.models import SecretaryPetitionSubmission
from texpenses.actions import inform_on_action

from django.template.loader import get_template
from django.template import RequestContext
from django.http import HttpResponse


from weasyprint import HTML

EXPOSED_METHODS = ['cancel', 'pdf', 'get_queryset']


@detail_route(methods=['post'])
@inform_on_action('CANCELLATION')
def cancel(self, request, pk=None):
    submitted = self.get_object()
    try:
        petition_id = submitted.status_rollback()
        headers = {'location': reverse('secretarypetition-detail',
                                       args=[petition_id])}
        return Response(headers=headers, status=status.HTTP_303_SEE_OTHER)
    except PermissionDenied as e:
        return Response({'detail': e.message},
                        status=status.HTTP_403_FORBIDDEN)


<<<<<<< 2e9c7e2e3f48c2079e96cd5b6667979c20d0c255
@inform_on_action('SUBMISSION')
=======
@detail_route(methods=['get'])
def pdf(self, request, pk=None):
    submitted = self.get_object()

    html_template = get_template('texpenses/base.html')

    rendered_html = html_template.render(
        RequestContext(request, {'petition': submitted})).\
        encode(encoding="UTF-8")

    pdf_file = HTML(string=rendered_html,
                    base_url=request.build_absolute_uri()).write_pdf()

    http_response = HttpResponse(pdf_file, content_type='application/pdf')
    http_response['Content-Disposition'] = 'filename="report.pdf"'

    return http_response


>>>>>>> Implement pdf generation for status 4 petitions (api/petition/secretary/submitted/<id>/pdf/)
def create(self, request, *args, **kwargs):
    return super(self.__class__, self).create(request, *args, **kwargs)


def get_queryset(self):
    return SecretaryPetitionSubmission.objects.all()
