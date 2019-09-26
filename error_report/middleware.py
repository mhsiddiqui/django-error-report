from __future__ import absolute_import, unicode_literals

import traceback
import sys

from django.views.debug import ExceptionReporter

from error_report.models import Error
from error_report.settings import ERROR_DETAIL_SETTINGS


class ExceptionProcessor(object):
    """
    Middleware that save details of exception that occurs in any app to the database.
    """

    def __init__(self, get_response=None):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_exception(self, request, exception):
        kind, info, data = sys.exc_info()
        if not ERROR_DETAIL_SETTINGS.get('ERROR_DETAIL_ENABLE', True):
            return None
        error = Error.objects.create(
            kind=kind.__name__,
            html=ExceptionReporter(request, kind, info, data).get_traceback_html(),
            path=request.build_absolute_uri(),
            info=info,
            data='\n'.join(traceback.format_exception(kind, info, data)),
        )
        error.save()
