import json
from rest_api_paths import *


class GlobalClass(object):

    '''
    GlobalClass:
    @args:
    -connectionClass
    -authenticationClass
    '''

    def __init__(self, connectionClass, authenticationClass):
        self.connectionClass = connectionClass
        self.authenticationClass = authenticationClass

    def get_banner(self, banner_type=None):

        '''
        get_banner:
        @args:
        -banner_type:   The type of banner, options: motd, login, exec, default: None
        @returns:
        -banner dictionary:     Keys: motd, login, exec
        '''

        if banner_type:
            banner_type_options = ['motd', 'login', 'exec']
            if banner_type not in banner_type_options:
                print "Banner type not recognized."
                raise Exception
        path = global_banner_path
        headers = self.authenticationClass.headers
        response, content = self.connectionClass.rest_api_call(path=path,
                                                               headers=headers)
        if response['status'] == '200':
            try:
                banner_data = json.loads(content)
            except:
                raise Exception
            if banner_type:
                return_data = {banner_type: banner_data[banner_type]}
            else:
                return_data = {'motd': banner_data['motd'],
                               'login': banner_data['login'],
                               'exec': banner_data['exec']}
            return return_data
        elif response['status'] == '401':
            print "Authentication failed"
        else:
            raise Exception

    def put_banner(self, banner_type, banner):

        '''
        put_banner:
        @args:
        -banner_type:   The type of banner, options: motd, login, exec
        -banner:    The banner string
        @returns:
        '''

        banner_type_options = ['motd', 'login', 'exec']
        if banner_type not in banner_type_options:
            print "Banner type not recognized."
            raise Exception
        path = global_banner_path
        headers = self.authenticationClass.headers
        headers['Content-Type'] = 'application/json'
        banner_dict = {banner_type: banner}
        method = 'PUT'
        body = json.dumps(banner_dict)
        response, content = self.connectionClass.rest_api_call(path=path,
                                                               method=method,
                                                               headers=headers,
                                                               body=body)
        if response['status'] == '401':
            print "Authentication failed"
        elif response['status'] != '204':
            raise Exception

    def get_hostname(self):

        '''
        get_hostname:
        @args:
        @returns:
        -hostname dictionary:     Keys: hostname
        '''

        path = global_hostname_path
        headers = self.authenticationClass.headers
        response, content = self.connectionClass.rest_api_call(path=path,
                                                               headers=headers)
        if response['status'] == '200':
            try:
                hostname_data = json.loads(content)
            except:
                raise Exception
            return_data = {'hostname': hostname_data['host-name']}
            return return_data
        elif response['status'] == '401':
            print "Authentication failed"
        else:
            raise Exception

    def put_hostname(self, hostname):

        '''
        put_hostname:
        @args:
        -hostname:  The hostname string
        @returns:
        '''

        path = global_hostname_path
        headers = self.authenticationClass.headers
        headers['Content-Type'] = 'application/json'
        hostname_dict = {'host-name': hostname}
        method = 'PUT'
        body = json.dumps(hostname_dict)
        response, content = self.connectionClass.rest_api_call(path=path,
                                                               method=method,
                                                               headers=headers,
                                                               body=body)
        if response['status'] == '401':
            print "Authentication failed"
        elif response['status'] != '204':
            raise Exception

    def get_domain_name(self):

        '''
        get_domain_name:
        @args:
        @returns:
        -domain_name dictionary:     Keys: domain_name
        '''

        path = global_domain_name_path
        headers = self.authenticationClass.headers
        response, content = self.connectionClass.rest_api_call(path=path,
                                                               headers=headers)
        if response['status'] == '200':
            try:
                domain_name_data = json.loads(content)
            except:
                raise Exception
            return_data = {'domain_name': domain_name_data['domain-name']}
            return return_data
        elif response['status'] == '401':
            print "Authentication failed"
        else:
            raise Exception

    def put_domain_name(self, domain_name):

        '''
        put_hostname:
        @args:
        -domain_name:  The domain_name string
        @returns:
        '''

        path = global_domain_name_path
        headers = self.authenticationClass.headers
        headers['Content-Type'] = 'application/json'
        domain_name_dict = {'domain-name': domain_name}
        method = 'PUT'
        body = json.dumps(domain_name_dict)
        response, content = self.connectionClass.rest_api_call(path=path,
                                                               method=method,
                                                               headers=headers,
                                                               body=body)
        if response['status'] == '401':
            print "Authentication failed"
        elif response['status'] != '204':
            raise Exception

    def get_local_users(self, user=None):

        '''
        get_local_users:
        @args:
        -user:  The username, default: None
        @returns:
        -local_user dictionary:     Keys: ...
        '''

        path = global_local_users_path
        if user:
            path = path + '/' + str(user)
        print path
        print user
        headers = self.authenticationClass.headers
        response, content = self.connectionClass.rest_api_call(path=path,
                                                               headers=headers)


# "users": [{"username": "uros", "privilege": 15, "kind": "object#local-user", "pw-type": 0}]}
        print response
        print content
        if response['status'] == '200':
            try:
                local_users_data = json.loads(content)
            except:
                raise Exception
            # print local_users_data['users']
            return_data = {'users': local_users_data['users']}
            return return_data
        elif response['status'] == '401':
            print "Authentication failed"
        else:
            raise Exception

    def post_local_users(self, username, password=None, pw_type=None, privilege=15):

        '''
        post_local_users:
        @args:
        -username:  The username string
        -password:  The password string, Default: None
        -pw_type:   The password type, options: 0, 7, Default: None
        -privilege: The privilege level of the user, options: 0-15, default: 15
        @returns:
        '''

        path = global_local_users_path
        headers = self.authenticationClass.headers
        headers['Content-Type'] = 'application/json'
        method = 'POST'
        local_users_dict = {'username': username}

        if password:
            local_users_dict['password'] = password

        if pw_type:
            try:
                int(pw_type)
                is_integer = True
            except:
                print "pw_type must be an integer"
                is_integer = False
                raise
            if is_integer:
                if int(pw_type) in [0, 7]:
                    local_users_dict['pw-type'] = str(pw_type)

        if privilege:
            try:
                int(privilege)
                is_integer = True
            except:
                print "privilege must be an integer"
                is_integer = False
                raise
            if is_integer:
                if int(privilege) in range(0, 16):
                    local_users_dict['privilege'] = int(privilege)
                else:
                    print "privilege not in expected range 0-15"
                    raise

        body = json.dumps(local_users_dict)

        response, content = self.connectionClass.rest_api_call(path=path,
                                                               method=method,
                                                               headers=headers,
                                                               body=body)
        if response['status'] == '401':
            print "Authentication failed"
        elif response['status'] != '201':
            raise Exception




# Local users

# /api/v1/global/local-users  Y Y N N
# /api/v1/global/local-users/{username} Y Y Y Y







