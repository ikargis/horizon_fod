import json
from django.http import HttpResponse
import services

__author__ = 'fzhadaev'


def task_status(request, task_id):
    user_id = 'user'  # FIXME:add auth
    response_data = services.get_task(user_id, task_id)
    return HttpResponse(json.dumps(response_data), content_type="application/json")
