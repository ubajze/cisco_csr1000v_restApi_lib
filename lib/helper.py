import ipaddr


def check_ip_address(check_string):

    try:
        ipaddr.IPv4Network(check_string)
        return True
    except:
        return False
