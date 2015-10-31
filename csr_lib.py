import httplib2
import json
from base64 import b64encode
from lib.rest_api_paths import *


class ConnectionClass(object):

    def __init__(self, host, port=443, protocol='https', disable_ssl_verification=True):
        self.host = host
        self.port = port
        self.protocol = protocol
        self.disable_ssl_verification = disable_ssl_verification
        self.httplib2_object = httplib2.Http(disable_ssl_certificate_validation=self.disable_ssl_verification)

    def rest_api_call(self, path, headers, method='GET', body=''):
        url = self.protocol + '://' + self.host + ':' + str(self.port) + path
        response, content = self.httplib2_object.request(url,
                                                         method=method,
                                                         body=body,
                                                         headers=headers)
        return response, content


class AuthenticationClass(object):

    def __init__(self, username, password):
        self.add_credentials(username, password)

    def add_credentials(self, username, password):
        self.username = username
        self.password = password

    def _encode_credentials(self):
        return b64encode(self.username + ':' + self.password)

    def get_authentication_header(self):
        return 'Basic ' + self._encode_credentials()

    def get_authentication_token(self, connectionClass):
        authorization_header = self.get_authentication_header()
        authentication_headers = {'Authorization': authorization_header,
                                  'Accept': 'application/json'}
        authentication_path = token_services_path
        authenticaiton_method = 'POST'
        response, content = connectionClass.rest_api_call(path=authentication_path,
                                                          headers=authentication_headers,
                                                          method=authenticaiton_method)
        if response['status'] == '200':
            try:
                authentication_data = json.loads(content)
            except:
                raise Exception
            self._create_headers(authentication_data)
            self._save_authentication_data(authentication_data)
            return authentication_data['token-id']
        else:
            raise Exception

    def _create_headers(self, content):
        self.headers = {'X-auth-token': content['token-id'],
                        'Accept': 'application/json'}

    def _save_authentication_data(self, content):
        self.expiry_time = content['expiry-time']
        self.token_id = content['token-id']
        self.link = content['link']

    def get_token_details(self, connectionClass):
        path = '/' + '/'.join(self.link.split('/')[3:])
        response, content = connectionClass.rest_api_call(path=path,
                                                          headers=self.headers)
        if response['status'] == '200':
            try:
                token_details = json.loads(content)
            except:
                raise Exception
            return token_details
        else:
            raise Exception

    def delete_token(self, connectionClass):
        path = '/' + '/'.join(self.link.split('/')[3:])
        method = 'DELETE'
        response, content = connectionClass.rest_api_call(path=path,
                                                          method=method,
                                                          headers=self.headers)
        if response['status'] == '204':
            return
        else:
            raise Exception


