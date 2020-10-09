from os import environ as env
import os
import network
from certs import generate_certs
from db import open_db

def get_path(website_id):
    return os.path.abspath(f"{env['NGINX_SITES_DIR']}/website_{website_id}.conf")


def install(website_id, domain, use_https, use_www):
    if use_https:
        # turn off use_https if cert fails
        worked = generate_certs(website_id, domain, use_www)
        if not worked:
            use_https = False
            with open_db() as conn:
                with conn.cursor() as cur:
                    query = "UPDATE users_website SET use_https = FALSE WHERE id=%s"
                    cur.execute(query, (website_id,))

    ip_addr = network.get_webserver_ip(website_id)
    dest_path = get_path(website_id)

    if use_https:
        with open('nginx-template-https.conf', 'r') as file:
            data = file.read()
    else:
        with open('nginx-template.conf', 'r') as file:
            data = file.read()

    # www. can be added here safely without checking use_www
    data = data.replace('REPLACEME_DOMAIN', f'{domain} www.{domain}')
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
