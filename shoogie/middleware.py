import logging
import sys
import warnings

from django         import http
from django.conf    import settings
from django.core    import exceptions

from log_handler import DatabaseLogHandler

DEFAULT_IGNORES = (http.Http404, exceptions.PermissionDenied)

class ExceptionLoggingMiddleware(object):
    def __init__(self):
        msg = "ExceptionLoggingMiddleware is deprecated; Remove it and " + \
            "add DatabaseLogHandler to your logging config instead"
        warnings.warn(msg, DeprecationWarning)
        if settings.DEBUG:
            raise exceptions.MiddlewareNotUsed
        self.log_handler = DatabaseLogHandler()

    def process_exception(self, request, _):
        record = logging.makeLogRecord({"exc_info": sys.exc_info(),
                                        "request": request})
        self.log_handler.emit(record)
