import rest_client
import json

__author__ = 'fzhadaev'

HOST = "172.18.78.12"
PORT = 8888
BASE_URL = "/fod/api/v1/"
SESSIONS = 'sessions'
ACCOUNTS = 'accounts'
TASKS = 'tasks'

USER_SESSIONS = {}


class UserSession:
    rest_client = None
    session_id = None
    account_id = None

    def __init__(self, user_id):
        self.rest_client = rest_client.RESTClient(HOST, PORT, user_id)
        self.session_id = get_new_session_id(self.rest_client)
        self.account_id = get_account_id(self.rest_client, self.session_id)


def get_user_session(user_id):
    if user_id not in USER_SESSIONS:
        USER_SESSIONS[user_id] = UserSession(user_id)
    return USER_SESSIONS[user_id]


def get_new_session_id(client):
    response = json.loads(client.put(BASE_URL + SESSIONS, None, None))
    return response['session_id']


def get_session_status(client):
    response = json.loads(client.get(BASE_URL + SESSIONS, None, None))
    return response['status']


def get_new_account_id(client, session_id):
    body = {'session_id': session_id, 'info': {
        "host": "172.18.16.178",
        "port": 8080,
        "region": "",
        "secure": False,
        "type": "CT_SWIFT"
    }, 'credentials': {
        "public_key": "system:root",
        "private_key": "testpass"
    }}

    response = json.loads(client.put(BASE_URL + ACCOUNTS, body=body))
    return response['account_id']


def get_account_id(client, session_id):
    try:
        response = json.loads(client.get(BASE_URL + ACCOUNTS, {'session_id': session_id}))
    except rest_client.RESTClientInvalidStatus as ex:
        return get_new_account_id(client, session_id)
    return response['account_id']


def push_task(user_id, action):
    user_session = get_user_session(user_id)
    body = {'session_id': user_session.session_id,
            'account_id': user_session.account_id,
            'action': action}
    response = json.loads(user_session.rest_client.put(BASE_URL + TASKS, body=body))
    return response['task']


def get_task(user_id, task_id):
    user_session = get_user_session(user_id)
    body = {'session_id': user_session.session_id,
            'task_id': task_id}
    return json.loads(user_session.rest_client.get(BASE_URL + TASKS, body=body))


def get_list_by_task_id(user_id, task_id):
    response = get_task(user_id, task_id)
    return response['list']
