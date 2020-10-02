from os import environ as env
import os
import network
import certs


def get_path(website_id):
    return os.path.abspath(f"{env['NGINX_SITES_DIR']}/website_{website_id}.conf")


def deal_with_certs(website_id, domain):
    if certs.has_certs(website_id, domain):
        certs.copy_certs(website_id, domain) # just in case
        print("Website already has certs")
        return True
    else:
        print("Website does not have certs, generating..")
        certs.get_cert(website_id, domain)
        if certs.has_certs(website_id, domain):
            print("it worked!")
            # epic.
            certs.copy_certs(website_id, domain)
            return True
        else:
            print("it did not work.")
            # :(
            return False


def install(website_id, domain, use_https):
    if use_https:
        # turn off use_https if cert fails
        use_https = deal_with_certs(website_id, domain)


    ip_addr = network.get_webserver_ip(website_id)
    dest_path = get_path(website_id)

    if use_https:
        with open('nginx-template-https.conf', 'r') as file:
            data = file.read()
    else:
        with open('nginx-template.conf', 'r') as file:
            data = file.read()

    data = data.replace('REPLACEME_DOMAIN', domain)
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
