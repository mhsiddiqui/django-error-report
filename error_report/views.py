# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.http import HttpResponse

from error_report.models import Error


def error_html(request, error):
    """
    View that return error html for iframe
    :param request: Request object
    :param error: Error id
    :return: Error html
    """
    return HttpResponse(Error.objects.get(id=error).html)
