import logging
import sys
import warnings

from django         import http
from django.core    import exceptions


DEFAULT_IGNORES = (http.Http404, exceptions.PermissionDenied)

class DatabaseLogHandler(logging.Handler):
    def __init__(self):
        super(DatabaseLogHandler, self).__init__()
        self.ignores_processed = False

    def process_ignore_list(self):
        """Defer ignore list evaluation to avoid a circular import of settings
        Only necessary for Django < 1.5"""
        from django.conf import settings
        ignores = getattr(settings, 'SHOOGIE_IGNORE_EXCEPTIONS', None)
        if ignores:
            self.ignores = []
            for exception_path in ignores:
                try:
                    mod, exc = exception_path.rsplit('.', 1)
                    __import__(mod)
                    ignore_mod = sys.modules[mod]
                    ignore_exc = getattr(ignore_mod, exc)
                    self.ignores.append(ignore_exc)
                except (ValueError, ImportError, AttributeError):
                    warnings.warn("Unable to import exception: {}".format(exception_path))
        else:
            self.ignores = DEFAULT_IGNORES
        self.ignores_processed = True

    def emit(self, record):
        if not self.ignores_processed:
            self.process_ignore_list()
        request = getattr(record, 'request', None)
        if request is None:
            request = getattr(record, 'msg', None)
        exc_type, exc_val, tb = getattr(record, 'exc_info', (None, None, None))
        if issubclass(exc_type, self.ignores):
            return
        # Cannot assume db is accessible here
        try:
            # Deferred to avoid circular import of settings (Django < 1.5)
            from . import logger
            logger.log_exception(request, exc_type, exc_val, tb)
        except:
            pass
