from horizon import tables
from django.utils.translation import ugettext_lazy as _  # noqa


class UpdateRow(tables.Row):
    ajax = True

    def get_data(self, request, obj_id):
        return []


class FodVolumesFilterAction(tables.FilterAction):

    def filter(self, table, fod_volumes, filter_string):
        """Naive case-insensitive search."""
        q = filter_string.lower()
        return [fod_volume for fod_volume in fod_volumes
                if q in fod_volume.name.lower()]


class FodVolumesTable(tables.DataTable):
    user_label = tables.Column("user_label", verbose_name="User Label")
    name = tables.Column("name",
                         verbose_name="Name")
    capacity = tables.Column("capacity", verbose_name="Capacity")
    secure = tables.Column("secure", verbose_name="Secure")
    sector_size = tables.Column("sector_size", verbose_name="Sector size")
    restore_points = tables.Column("restore_points", verbose_name="Restore Points")

    class Meta:
        name = "fod_volumes"
        verbose_name = _("Fod Volumes")
        table_actions = (FodVolumesFilterAction,)