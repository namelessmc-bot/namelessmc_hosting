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

    template = read_template(use_https, use_www)
    template = template.replace('REPLACEME_DOMAIN', domain)
    template = template.replace('REPLACEME_IPADDR', ip_addr)

    write_config(website_id, template)


def read_template(use_https, use_www):
    if use_https and use_www:
        name = 'www-https'
    elif use_https and not use_www:
        name = 'https'
    elif not use_https and use_www:
        name = 'www-http'
    else:
        name = 'http'
    with open(f'nginx-template-{name}.conf', 'r') as file:
        return file.read()


def write_config(website_id, template):
    dest_path = get_path(website_id)
    with open(dest_path, 'w') as dest_file:
        dest_file.write(template)

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
