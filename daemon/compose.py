from os import environ as env
import os
import network


def install(website_id, domain, use_https, db_password, files_password, version, \
            username, email):
    with open('compose-template.yaml', 'r') as file:
        data = file.read()

    ip_addr = network.get_webserver_ip(website_id)
    data = data.replace('REPLACEME_IPADDR', ip_addr)
    data = data.replace('REPLACEME_DBPASSWORD', db_password)
    data = data.replace('REPLACEME_PHPMYADMINURI', get_phpmyadmin_uri(domain, use_https))
    data = data.replace('REPLACEME_FILESUSER', "user")
    data = data.replace('REPLACEME_FILESPASSWORD', files_password)
    data = data.replace('REPLACEME_VERSION', version)
    data = data.replace('REPLACEME_HOSTNAME', domain)
    data = data.replace('REPLACEME_USERNAME', username)
    data = data.replace('REPLACEME_EMAIL', email)

    dest_path = f"/{env['ZFS_ROOT']}/{website_id}/docker-compose.yaml"
    with open(dest_path, 'w') as dest_file:
        dest_file.write(data)

    os.system(f"docker-compose -f {dest_path} up -d --remove-orphans")


def uninstall(website_id):
    dest_path = f"/{env['ZFS_ROOT']}/{website_id}/docker-compose.yaml"
    os.system(f"docker-compose -f {dest_path} down")


def get_phpmyadmin_uri(domain, use_https):
    if use_https:
        return f"https://{domain}/phpmyadmin"
    else:
        return f"http://{domain}/phpmyadmin"
