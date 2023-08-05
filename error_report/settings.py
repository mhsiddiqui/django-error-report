"""Settings for django-error-report-2 package."""
from django.conf import settings

ERROR_DETAIL_SETTINGS = getattr(settings, "ERROR_DETAIL_SETTINGS", {})
