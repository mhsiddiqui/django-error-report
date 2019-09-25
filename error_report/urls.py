from __future__ import absolute_import, unicode_literals

try:
    from django.conf.urls import url
except ImportError:
    from django.urls import re_path as url

from error_report.views import error_html

urlpatterns = [
    url(r'^error_html/(?P<error>[0-9]+)/$', error_html, name='error-html-link'),
]
