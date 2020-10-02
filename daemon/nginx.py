from os import environ as env
import os
import network


def get_path(website_id):
    return os.path.abspath(f"{env['NGINX_SITES_DIR']}/website_{website_id}.conf")


def install(website_id, website_hostname, use_https):
    ip_addr = network.get_webserver_ip(website_id)

    dest_path = get_path(website_id)

    if use_https:
        with open('nginx-template-https.conf', 'r') as file:
            data = file.read()
            data = data.replace('REPLACEME_ID', website_id)
    else:
        with open('nginx-template.conf', 'r') as file:
            data = file.read()

    data = data.replace('REPLACEME_HOSTNAME', website_hostname)
    data = data.replace('REPLACEME_IPADDR', ip_addr)

    with open(dest_path, 'w') as dest_file:
        dest_file.write(data)

    reload_nginx()


def uninstall(website_id):
    path = get_path(website_id)
    if os.path.exists(path):
        os.remove(path)
        reload_nginx()


def reload_nginx():
    if 'NGINX_RELOAD_COMMAND' in env:
        command = env['NGINX_RELOAD_COMMAND']
        os.system(command)
