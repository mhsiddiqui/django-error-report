import traceback
import sys

from django.conf import settings

from django.views.debug import ExceptionReporter

from error_report.models import Error


class ExceptionProcessor(object):
    """
    Middleware that save details of exception that occurs in any app to the database.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_exception(self, request, exception):
        kind, info, data = sys.exc_info()
        if settings.DEBUG:
            return None
        error = Error.objects.create(
            kind=kind.__name__,
            html=ExceptionReporter(request, kind, info, data).get_traceback_html(),
            path=request.build_absolute_uri(),
            info=info,
            data='\n'.join(traceback.format_exception(kind, info, data)),
        )
        error.save()
