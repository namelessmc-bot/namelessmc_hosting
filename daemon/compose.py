from os import environ as env
import network

def install(website_id, db_password):
    with open('compose-template.yaml', 'r') as file:
        data = file.read()

    ip_addr = network.get_webserver_ip(website_id)
    data = data.replace('REPLACEME_IPADDR', ip_addr)
    data = data.replace('REPLACEME_DBPASSWORD', db_password)

    dest_path = f"/{env['ZFS_ROOT']}/{website_id}/docker-compose.yaml"
    with open(dest_path, 'w') as dest_file:
        dest_file.write(data)
