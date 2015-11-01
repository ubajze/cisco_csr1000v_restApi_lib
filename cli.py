import re
import sys
import types
import inspect
import json
import readline

from csr_lib import ConnectionClass
from csr_lib import AuthenticationClass

# Import all modules
from lib.global_object import GlobalClass
api_objects = []
api_objects.append(GlobalClass)

deviceObjects = []


class CliClass(object):

    def __init__(self, dataClass):
        self.dataClass = dataClass
        self.all_methods = self._get_all_methods()

    def get_input_string(self, input_string):
        self.input_string = input_string
        command, arguments = self._interpret_input_string()
        if self._verify_arguments(command, arguments):
            return command, arguments

    def _interpret_input_string(self):
        self.input_string = self.input_string.strip()
        command, arguments = self._search_command(self.input_string)
        if self._search_and_print_help():
            return None, None
        elif self._search_and_exit():
            sys.exit(0)
        elif self._search_connect():
            return 'connect', None
        elif command:
            return command, arguments
        else:
            print "Error: Wrong command"
            print ""

    def _search_and_print_help(self, specific_command=None):
        if 'help' in self.input_string[0:4]:
            all_methods = self._get_all_methods()
            if len(self.input_string) != 4:
                input_string_list = [x for x in self.input_string.split(' ') if x]
                if len(input_string_list) == 2:
                    method_string = input_string_list[1]
                    method_string = re.sub('\(|\)', '', method_string).strip()
                    method_find = False
                    for object_class in all_methods.keys():
                        for method in all_methods[object_class]:
                            if method == method_string:
                                method_find = True
                                method_docstring = eval(object_class.__name__ + '.' + method).__doc__
                                if method_docstring:
                                    print self._format_docstring(method_docstring)
                    if not method_find:
                        print "Method not found."
                else:
                    print "Wrong arguments"
            else:
                print "All methods:"
                for object_class in all_methods.keys():
                    for method in all_methods[object_class]:
                        print object_class.__name__ + ":\t" + method
            return True
        else:
            return False

    def _search_connect(self):
        if self.input_string == 'connect':
            return True

    def _format_docstring(self, docstring):
        docstring_lines = []
        for line in docstring.splitlines():
            docstring_lines.append(line.strip())
        return '\n'.join(docstring_lines[1:-1])

    def _search_and_exit(self):
        if self.input_string == 'exit':
            print "Exiting..."
            return True
        else:
            return False

    def _get_all_methods(self):
        global api_objects
        all_methods = {}
        for api_object in api_objects:
            all_methods[api_object] = []
            for method in api_object.__dict__:
                if isinstance(api_object.__dict__[method], types.FunctionType):
                    if method[0] != '_':
                        all_methods[api_object].append(method)
        return all_methods

    def _search_command(self, input_command):
        search = re.search('\(.*\)$', input_command)
        if search:
            command = input_command[0:search.start()]
            arguments = []
            for argument in search.group(0)[1:-1].split(','):
                arguments.append(argument.strip())
            if arguments[0] == '':
                arguments = None
            for class_object in self.all_methods:
                for method in self.all_methods[class_object]:
                    if method == command:
                        return [class_object, method], arguments
        return None, None

    def _verify_arguments(self, command, arguments):
        return True


class DataClass(object):

    hosts = []

    def __init__(self):
        self.hosts.append({'host': '192.168.35.11',
                           'username': 'cisco',
                           'password': 'cisco',
                           'protocol': 'https',
                           'port': 55443})

    def connect(self):
        for host in self.hosts:
            global deviceObjects
            connectionClass = ConnectionClass(host=host['host'],
                                              port=host['port'],
                                              protocol=host['protocol'])
            authenticationClass = AuthenticationClass(username=host['username'],
                                                      password=host['password'])
            authenticationClass.get_authentication_token(connectionClass)
            deviceObjects.append([connectionClass, authenticationClass])

    def disconnect(self, device):
        pass


def add_device(host, username, password, port=443, protocol='https'):
    connectionClass = ConnectionClass(host, port, protocol)
    authenticationClass = AuthenticationClass(username, password)
    authenticationClass.get_authentication_token(connectionClass)


def send_command(connectionClass, authenticationClass, command=None, arguments=None):
    if command:
        objectInstance = command[0](connectionClass, authenticationClass)
        function = getattr(objectInstance, command[1])
        if arguments:
            arg = []
            kwarg = {}
            for argument in arguments:
                if len(argument.split('=')) == 2:
                    kwarg[argument.split('=')[0]] = argument.split('=')[1]
                else:
                    arg.append(argument)
            function_result = function(*arg, **kwarg)
        else:
            function_result = function()
        if function_result:
            print json.dumps(function_result, indent=4)


if __name__ == "__main__":

    host = None
    port = None
    protocol = None
    username = None
    password = None

    try:
        '''
        hosts = [{'host': None,
                 'username': None,
                 'password': None,
                 'port': None,
                 'protocol': None}]
        '''
        dataClass = DataClass()
        commandObject = CliClass(dataClass)

        while True:
            input_var = raw_input('# ')
            if input_var != "":
                command, arguments = commandObject.get_input_string(input_var)
                if command == 'connect':
                    dataClass.connect()
                elif not command:
                    pass
                else:
                    if not deviceObjects:
                        print "No devices to send the command"
                    else:
                        for device in deviceObjects:
                            print "Device: " + device[0].host
                            print "Command: " + command[1]
                            if arguments:
                                print "Arguments: " + ','.join(arguments)
                            send_command(device[0], device[1], command, arguments)
    except KeyboardInterrupt:
        sys.exit()

