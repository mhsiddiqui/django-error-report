from django.contrib import admin
from django.contrib.admin.views.main import ChangeList
try:
    from django.conf.urls import patterns, url
except ImportError:
    from django.conf.urls.defaults import patterns, url
from django.core.urlresolvers import reverse
from django.http import HttpResponse

from . import models, utils, views

def get_name(user):
    return user.get_full_name() or user.username

class Truncate(object):
    max_length = 50
    def __init__(self, attrname, max_length=None):
        self.attrname = attrname
        self.__name__ = attrname
        if max_length is not None:
            self.max_length = max_length

    def __call__(self, instance):
        val = getattr(instance, self.attrname, '')
        return utils.truncate(val, self.max_length)

class FasterChangeList(ChangeList):
    "Defers large fields we don't use"
    defer_fields = (
                'post_data',
                'cookie_data',
                'session_data',
                'technical_response',
            )
    # get_query_set() was renamed to get_queryset() in Django 1.6
    def get_queryset(self, *args, **kwargs):
        changelist = super(FasterChangeList, self)
        if hasattr(changelist, 'get_queryset'):
            qset = changelist.get_queryset(*args, **kwargs)
        else:
            qset = changelist.get_query_set(*args, **kwargs)
        return qset.defer(*self.defer_fields)

    get_query_set = get_queryset

class ServerErrorAdmin(admin.ModelAdmin):
    list_display = (Truncate('exception_type', 40),
                    Truncate('exception_str', 80),
                    'path_link',
                    'error_date_format',
                    'user_link',
                    'technicalresponse_link',
                    'resolved',)
    date_hierarchy = 'timestamp'
    search_fields  = ('request_path', 'exception_type', 'exception_str', 'source_file', 'source_function', 'source_text')
    actions = ('get_email_list', 'resolve_servererror', 'unresolve_servererror')

    exclude = ('technical_response',)
    readonly_fields = (
            'timestamp',
            'hostname',
            'request_method',
            'request_path',
            'query_string',
            'post_data',
            'cookie_data',
            'session_id',
            'session_data',
            'user',
            'exception_type',
            'exception_str',
            'source_file',
            'source_line_num',
            'source_function',
            'source_text',
        )
    # queryset() was renamed to get_queryset() in Django 1.6
    def get_queryset(self, request):
        model_admin = super(ServerErrorAdmin, self)
        if hasattr(model_admin, 'get_queryset'):
            qset = model_admin.get_queryset(request)
        else:
            qset = model_admin.queryset(request)
        return qset.select_related('user')

    queryset = get_queryset

    def get_changelist(self, request, **kwargs):
        return FasterChangeList

    def error_date_format(self, instance):
        return instance.timestamp.strftime('%Y-%b-%d %H:%M')
    error_date_format.admin_order_field = 'timestamp'
    error_date_format.short_description = 'timestamp'

    get_request_path = Truncate('request_path', 40)
    def path_link(self, instance):
        request_path = self.get_request_path(instance)
        if 'GET' != instance.request_method:
            if instance.request_method:
                return u'%s (%s)' % (request_path, instance.request_method)
            else:
                return request_path
        url = u'http://%s%s?%s' % (instance.hostname, instance.request_path, instance.query_string)
        return u'<a href="{0}" title="{0}">{1}</a>'.format(url, request_path)
    path_link.admin_order_field = 'request_path'
    path_link.allow_tags = True
    path_link.short_description = 'path'

    def user_link(self, instance):
        if not instance.user:
            return u'(None)'
        user = instance.user
        url = reverse('admin:auth_user_change', args=(user.id,))
        templ = u'<a href="{url}" title="{name}">{username}</a>'
        return templ.format(url=url, username=user.username, name=get_name(user))
    user_link.admin_order_field = 'user'
    user_link.allow_tags = True
    user_link.short_description = 'user'

    def get_email_list(self, request, queryset):
        emails = set()
        for se in queryset.select_related('user'):
            user = se.user
            if user and user.email:
                name = get_name(user)
                emails.add('"%s" <%s>' % (name, user.email))
        return HttpResponse(',\n'.join(emails), mimetype='text/plain')
    get_email_list.short_description = 'Get user email addresses for selected errors'

    def technicalresponse_link(self, instance):
        tr_url = reverse('admin:shoogie_technicalresponse', kwargs={'pk':instance.pk})
        return '<a href="%s"><b>debug</b></a>' % tr_url
    technicalresponse_link.allow_tags = True
    technicalresponse_link.short_description = 'Debug'

    def resolve_servererror(self, request, queryset):
        update_count = queryset.update(resolved=True)
        plural = 's' if update_count != 1 else ''
        self.message_user(request, "Marked %d error%s as resolved" % (update_count, plural))
    resolve_servererror.short_description = "Mark selected errors as resolved"

    def unresolve_servererror(self, request, queryset):
        update_count = queryset.update(resolved=False)
        plural = 's' if update_count != 1 else ''
        self.message_user(request, "Marked %d error%s as not resolved" % (update_count, plural))
    unresolve_servererror.short_description = "Mark selected errors as NOT resolved"

    def get_urls(self):
        myview = views.TechnicalResponseView.as_view()
        myurls = patterns('',
            url(r'(?P<pk>\d+)/technicalresponse/$',
                self.admin_site.admin_view(myview, cacheable=True),
                name='shoogie_technicalresponse',
            ),
        )
        return myurls + super(ServerErrorAdmin, self).get_urls()

admin.site.register(models.ServerError, ServerErrorAdmin)
