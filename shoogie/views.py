from django.http  import HttpResponse
from django.views.generic import detail

from shoogie import models

class TechnicalResponseView(detail.BaseDetailView):
    queryset = models.ServerError.objects.all()
    def render_to_response(self, context):
        return HttpResponse(context['servererror'].technical_response)

