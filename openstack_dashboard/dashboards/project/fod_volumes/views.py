# Create your views here.
from time import sleep
from django.http import HttpResponse, Http404
from django.template import loader, RequestContext
from rest_client import RESTClientInvalidStatus
import services

from openstack_dashboard.dashboards.project.fod_volumes \
    import tables as project_tables
from horizon import tables


class IndexView(tables.DataTableView):
    table_class = project_tables.FodVolumesTable
    template_name = 'project/fod_volumes/index.html'

    def __init__(self, *args, **kwargs):
        super(IndexView, self).__init__(*args, **kwargs)
        self._more = False

    def has_more_data(self, table):
        return self._more

    def get_data(self):
        request = self.request
        task_id = None
        user_id = 'user'  # FIXME:add auth
        if not task_id:
            task_id = services.push_task(user_id, 'list')
        while True:
            sleep(1)
            task_status = services.get_task(user_id, task_id)
            if task_status['state'] == 'complete':
                break
            if task_status['state'] == 'failure':
                raise Http404('Task status is failure')
        try:
            volumes_list = services.get_list_by_task_id(user_id, task_id)
            fod_volumes = []
            id = 0
            for volume in volumes_list:
                fod_volumes.append(FodVolume(volume, id))
                id += 1
        except RESTClientInvalidStatus as ex:
            raise Http404('No such task number')
        return fod_volumes


class FodVolume(object):
    def __init__(self, volume, id):
        super(FodVolume, self).__init__()
        self.name = volume['name']
        self.capacity = volume['capacity']
        self.secure = volume['secure']
        self.sector_size = volume['sector_size']
        self.user_label = volume['user_label']
        self.id = id
        self.restore_points = ""
        point_id = 0
        for point in volume['restore_points']:
            self.restore_points += point + " "#.append(RestorePoint(point, point_id))
            point_id += 1


class RestorePoint(object):
    def __init__(self, point, id):
        super(RestorePoint, self).__init__()
        self.point = point
        self.id = id

    def __str__(self):
        return self.point



