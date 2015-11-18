import json

custom_error_codes = {
    '1000': 'Banner type not recognized.',
    '1001': 'pw_type must be an integer',
    '1002': 'pw_type not 0 or 7',
    '1003': 'Privilege must be an integer.',
    '1004': 'Privilege not in expected range 0-15.',
    '1005': 'Host is not in IP form.',
}

def response_status(response, content):
    error_codes = ['400', '404', '405']
    service_error_codes = ['500', '503']
    if response['status'] == '401':
        return {'error_code': '401',
                'error_message': 'Unauthorized',
                'detail': 'The user is not authorized to invoke the request due to invalid authentication parameters, or lack of authority.'}
    elif response['status'] in error_codes or response['status'] in service_error_codes:
        error_code = ''
        error_message = ''
        detail = ''
        try:
            content_dict = json.loads(content)
        except:
            content_dict = None
        if content_dict:
            if 'error-code' in content_dict.keys():
                error_code = content_dict['error-code']
            else:
                error_code = str(response['status'])
            if 'error-message' in content_dict.keys():
                error_message = content_dict['error-message']
            if 'detail' in content_dict.keys():
                detail = content_dict['detail']
            return {'error_code': error_code,
                    'error_message': error_message,
                    'detail': detail}
        else:
            error_code = str(response['status'])
            return {'error_code': error_code,
                    'error_message': error_message,
                    'detail': detail}
    else:
        return None
