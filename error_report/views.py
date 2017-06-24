from django.http import HttpResponse
from django.views.generic import detail

from models import ServerError


class TechnicalResponseView(detail.BaseDetailView):
    queryset = ServerError.objects.all()

    def render_to_response(self, context):
        return HttpResponse(context['servererror'].technical_response)
