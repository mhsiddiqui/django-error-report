from django.db      import models
"""
Based on http://stackoverflow.com/questions/7130985/#answer-7579467

"""

try:
    from django.conf import settings
    USER = settings.AUTH_USER_MODEL
except AttributeError:
    from django.contrib.auth.models import User
    USER = User

class ServerError(models.Model):
    timestamp       = models.DateTimeField(auto_now_add=True)

    # http request information
    hostname        = models.CharField(max_length=64)
    request_method  = models.CharField(max_length=10)
    request_path    = models.CharField(max_length=1024)
    query_string    = models.TextField(blank=True)
    post_data       = models.TextField(blank=True)
    cookie_data     = models.TextField(blank=True)
    session_id      = models.CharField(max_length=64)
    session_data    = models.TextField(blank=True)
    user            = models.ForeignKey(USER, blank=True, null=True)

    # traceback
    exception_type  = models.CharField(max_length=128)
    exception_str   = models.TextField()
    source_file     = models.CharField(max_length=256)
    source_line_num = models.IntegerField()
    source_function = models.CharField(max_length=128)
    source_text     = models.CharField(max_length=256)

    # django's error page
    technical_response = models.TextField()

    # extra
    issue           = models.CharField(max_length=256, blank=True)
    resolved        = models.BooleanField(default=False)

    def __unicode__(self):
        return '%s %s%s' % (self.timestamp.strftime('%Y-%b-%d %H:%M'),
                                self.hostname, self.request_path)


