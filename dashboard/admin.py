import lemon

from django.contrib.admin.models import LogEntry
from django.utils.translation import ugettext_lazy as _

from .base import dashboard, Widget


class DashboardAdmin(lemon.AppAdmin):

    dashboard = dashboard

    @property
    def urls(self):
        return self.dashboard.get_urls(self), 'dashboard', 'dashboard'


class AdminSite(lemon.AdminSite):

    index_template = 'admin/custom_dashboard_index.html'

    def __init__(self, dashboard, name=None, app_name='admin'):
        super(AdminSite, self).__init__(name, app_name)
        self.dashboard = dashboard
        self.register_app('dashboard', DashboardAdmin, dashboard=dashboard)

    def index(self, request, extra_context=None):
        context = {'dashboard': self.dashboard}
        context.update(extra_context or {})
        return super(AdminSite, self).index(request, context)


class LogWidget(Widget):

    title = _(u"Admin log")
    description = _(u"Log of your last fifteen actions in admin.")
    template = 'dashboard/log.html'

    def get_log(self, user, limit=15):
        qs = LogEntry.objects.select_related('content_type', 'user')
        return qs.filter(user=user)[:limit]

    def get_context_data(self, context):
        return {'log': self.get_log(context['user'])}


class AppsWidget(Widget):

    title = _(u"Apps")
    description = _(u"Simple navigation in admin through apps' models.")
    template = 'dashboard/apps.html'


dashboard.register(LogWidget)
dashboard.register(AppsWidget)
lemon.site.register_app('dashboard', DashboardAdmin)
