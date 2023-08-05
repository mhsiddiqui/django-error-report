# -*- coding: utf-8 -*-
"""Views for django-error-report-2 package."""
from __future__ import absolute_import, unicode_literals

from django.http import HttpResponse

from error_report.models import Error


def error_html(request, error):
    """View that return error html for iframe

    Args:
        request (request): Request object
        error (int): Error id

    Returns:
        HttpResponse: Error html
    """
    return HttpResponse(Error.objects.get(id=error).html)
