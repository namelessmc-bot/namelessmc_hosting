PREFIX = '10.130'

def get_webserver_ip(website_id):
    # convert to 16-bit binary string
    binary = format(website_id, '016b')
    # split to two 8-bit strings and convert back to decimal
    first = int(binary[:8], 2)
    second = int(binary[8:], 2)
    # format as IP address
    return f'{PREFIX}.{first}.{second}'

