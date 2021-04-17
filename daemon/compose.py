from os import environ as env
import os
import network


autofill_domains = [
    'nlmc-php74.derkad.es',
    'nlmc-php8.derkad.es',
    'demo-1.namedhosting.com',
    'demo-2.namedhosting.com',
    'demo-3.namedhosting.com',
    'demo-4.namedhosting.com',
    'demo-5.namedhosting.com'
]


def install(website_id, domain, use_https, db_password, files_password, version, \
            site_name, username, email):
    with open('compose-template.yaml', 'r') as file:
        data = file.read()

    ip_addr = network.get_webserver_ip(website_id)
    data = data \
        .replace('REPLACEME_SITEID', str(website_id)) \
        .replace('REPLACEME_IPADDR', ip_addr) \
        .replace('REPLACEME_DBPASSWORD', db_password) \
        .replace('REPLACEME_PHPMYADMINURI', get_phpmyadmin_uri(domain, use_https)) \
        .replace('REPLACEME_FILESUSER', "user") \
        .replace('REPLACEME_FILESPASSWORD', files_password) \
        .replace('REPLACEME_VERSION', version) \
        .replace('REPLACEME_HOSTNAME', domain) \
        .replace('REPLACEME_SITENAME', site_name) \
        .replace('REPLACEME_USERNAME', username) \
        .replace('REPLACEME_EMAIL', email) \
        .replace('REPLACEME_DBPASSWORD', db_password if domain in autofill_domains else '') \

    dest_path = f"/{env['ZFS_ROOT']}/{website_id}/docker-compose.yaml"
    with open(dest_path, 'w') as dest_file:
        dest_file.write(data)

    mkdir(f"/{env['ZFS_ROOT']}/{website_id}/web")
    mkdir(f"/{env['ZFS_ROOT']}/{website_id}/certs")

    os.system(f"docker-compose -f {dest_path} up -d --remove-orphans --force-recreate")


def start(website_id):
    compose_file = f"/{env['ZFS_ROOT']}/{website_id}/docker-compose.yaml"
    os.system(f"docker-compose -f {compose_file} start")


def uninstall(website_id):
    dest_path = f"/{env['ZFS_ROOT']}/{website_id}/docker-compose.yaml"
    os.system(f"docker-compose -f {dest_path} down")


def get_phpmyadmin_uri(domain, use_https):
    if use_https:
        return f"https://{domain}/phpmyadmin"
    else:
        return f"http://{domain}/phpmyadmin"

def mkdir(dir_path):
    try:
        print('mkdir', dir_path)
        os.mkdir(dir_path)
    except FileExistsError:
        print('dir already exists')
        pass
