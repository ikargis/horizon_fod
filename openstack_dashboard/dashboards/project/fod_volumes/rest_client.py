import json
from logging import debug
from requests.packages import urllib3


class RESTClientInvalidStatus(Exception):
    pass


class RESTClient(object):
    def __init__(self, host, port=None, user=None, password=None):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.connection_pool = urllib3.HTTPConnectionPool(self.host, port=self.port, maxsize=10)

    def call(self, method, url, body={}, allowed_status=(200, 202), headers=None):
        if headers is None:
            headers = {}
        headers['Content-Type'] = 'application/json'
        headers['Accept'] = 'text/plain'

        if self.user is not None:
            # auth_value = '%s:%s' % (self.user, self.password)
            # auth_value = auth_value.encode('base64').strip()
            headers['Authorization'] = self.user #'Basic %s' % auth_value
            print('REST request (method %s; headers %s) to url %s with body %s' % (
         method, headers, self.host+':'+str(self.port) + url, json.dumps(body)))
        try:
            rsp = self.connection_pool.urlopen(method, url, json.dumps(body), headers)
        except Exception as ex:
            raise RESTClientInvalidStatus(ex.message)
        if rsp.status in allowed_status:
            # logger.debug('REST response (status %s) with body: %s' % (rsp.status, rsp.data))
            return rsp.data
            # logger.error('REST invalid response status %s, allowed statuses: %s. Response body: %s' % (
        # rsp.status, allowed_status, rsp.data))
        raise RESTClientInvalidStatus(
            'REST invalid response status %s, allowed statuses: %s.' % (rsp.status, allowed_status))

    def get(self, url, headers=None, body=None, allowed_status=(200,)):
        return self.call(method="GET", url=url, allowed_status=allowed_status, body=body, headers=headers)

    def put(self, url, body, headers=None):
        return self.call(method="PUT", url=url, body=body, headers=headers)

    def post(self, url, body, allowed_status=(200,), headers=None):
        return self.call("POST", url, body, allowed_status, headers)

    def delete(self, url, headers=None):
        return self.call(method="DELETE", url=url, headers=headers)

    def delete_if_needed(self, url, headers=None, allowed_status=(200, 202, 204, 404)):
        return self.call("DELETE", url, {}, allowed_status, headers)
