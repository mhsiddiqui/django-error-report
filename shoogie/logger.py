import re
import socket
import sys
import traceback

from django         import http
from django.conf    import settings
from django.views   import debug

from . import models, utils


def log_exception(request=None, exc_type=None, exc_val=None, tb=None):
    django_request = None
    if isinstance(request, http.HttpRequest):
        django_request = request

    if tb is None:
        exc_type, exc_val, tb = sys.exc_info()

    reporter = debug.ExceptionReporter(django_request,
                                        exc_type,
                                        exc_val,
                                        Traceback(tb) or None)

    tb_desc = traceback.extract_tb(tb)
    tb_file, tb_line_num, tb_function, tb_text = tb_desc[-1]

    data = {}
    if request is not None:
        data = request_data(request)

    data.update({
        'exception_type' : exc_type.__name__,
        'exception_str'  : str(exc_val),
        'source_file'    : utils.TruncateBeginning(tb_file),
        'source_line_num': tb_line_num,
        'source_function': tb_function,
        'source_text'    : tb_text,
    })

    kwargs = utils.clean_data_for_insert(data, models.ServerError)
    models.ServerError.objects.create(
            issue = '',
            technical_response = get_technical_response(reporter),
            **kwargs
        )

def get_technical_response(reporter):
    try:
        return reporter.get_traceback_html()
    except:
        return """<h1>Unable to generate django debug!</h1>
                  <p>Please report the following error on the <a
                  href="https://bitbucket.org/altaurog/django-shoogie/issues"
                  >django-shoogie bugtracker</a>:</p> <pre>%s</pre>
                  """ % traceback.format_exc()

def request_data(request):
    """
    Get data out of the request object.  Assume nothing
    """
    # Allow a string for convenience
    if isinstance(request, basestring):
        return {'request_path': request}

    data = {}
    try:
        data['hostname'] = request.get_host()
    except:
        data['hostname'] = socket.getfqdn()

    data['request_method'] = getattr(request, 'method', '')
    data['request_path'] = getattr(request, 'path', '')

    try:
        data['query_string'] = request.META.get('QUERY_STRING', '')
    except:
        data['query_string'] = ''

    try:
        data['post_data'] = dict(request.POST)
    except:
        data['post_data'] = ''

    try:
        data['cookie_data'] = request.COOKIES
    except:
        data['cookie_data'] = ''

    try:
        data['session_id'] = request.session.session_key
    except:
        data['session_id'] = ''

    try:
        data['session_data'] = dict(request.session.iteritems())
    except:
        data['session_data'] = ''

    try:
        user = request.user
        if user.is_anonymous():
            user = None
    except:
        user = None

    data['user'] = user
    return data

DEFAULT_EXCLUDE = (
        ('/django/core/handlers/base.py$', '^get_response$'),
        ('/django/template/', 'render'),
    )

def compile_exclude(exclude_desc):
    return map(re.compile, exclude_desc)

class Traceback(object):
    "Wrap a traceback object so we can filter it"
    exclude = None
    def __init__(self, tb):
        if self.exclude is None:
            self.load_config()
        if tb:
            tb = self.get_next(tb)
        self.tb = tb
        if tb:
            self.tb_frame = tb.tb_frame
            self.tb_lineno = tb.tb_lineno
            self.tb_lasti = tb.tb_lasti

    @property
    def tb_next(self):
        return self.__class__(self.tb.tb_next) or None

    def __nonzero__(self):
        return bool(self.tb)

    def get_next(self, tb):
        while tb and self.skip(tb):
            tb = tb.tb_next
        return tb

    def skip(self, tb):
        "Determine if this tb should be skipped or not"
        co = tb.tb_frame.f_code
        filename = co.co_filename
        funcname = co.co_name
        for file_re, func_re in self.exclude:
            if file_re.search(filename) and  func_re.search(funcname):
                return True

    def load_config(self):
        "Load exclude configuration into class if necessary"
        exclude_conf = getattr(settings,
                                'SHOOGIE_TRACEBACK_EXCLUDE',
                                DEFAULT_EXCLUDE)
        Traceback.exclude = map(compile_exclude, exclude_conf)
