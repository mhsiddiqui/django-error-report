from django.conf.urls import url
from views import error_html

urlpatterns = [
    url(r'^error_html/(?P<error>[0-9]+)/$', error_html, name='error-html-link'),
]
