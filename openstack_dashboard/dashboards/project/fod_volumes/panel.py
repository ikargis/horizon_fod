from django.utils.translation import ugettext_lazy as _  # noqa

import horizon

from openstack_dashboard.dashboards.project import dashboard


class FODVolumes(horizon.Panel):
    name = _("FOD Volumes")
    slug = 'fod_volumes'


dashboard.Project.register(FODVolumes)

