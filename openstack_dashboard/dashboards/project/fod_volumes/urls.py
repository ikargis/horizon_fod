__author__ = 'fzhadaev'


from django.conf.urls import patterns, url

from openstack_dashboard.dashboards.project.fod_volumes import views

urlpatterns = patterns('',
    url(r'^$', views.IndexView.as_view(), name='index'),
    #url(r'^ts/(?P<task_id>[a-zA-Z0-9-_]+)/$', api.task_status, name='task_status'),
    # url(r'^(?P<volume_id>\w+)/$', volumes.views.detail, name='detail')
)
