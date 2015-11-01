custom_error_codes = {
    '1000': 'Banner type not recognized.',
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
        if 'error_code' in content.keys():
            error_code = content['error_code']
        else:
            error_code = str(response['status'])
        if 'error_message' in content.keys():
            error_message = content['error-message']
        if 'detail' in content.keys():
            detail = content['detail']
        return {'error_code': error_code,
                'error_message': error_message,
                'detail': detail}
    else:
        return None
