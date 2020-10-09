import os


ZFS_ROOT = os.environ['ZFS_ROOT']
NGINX_CERTS_DIR = os.environ['NGINX_CERTS_DIR']


def generate_certs(website_id, domain, use_www):
    if has_certs(website_id, domain, use_www):
        copy_certs(website_id, domain) # just in case
        print("Website already has certs")
        return True

    print("Website does not have certs, generating..")
    get_cert(website_id, domain, use_www)

    if has_certs(website_id, domain, use_www):
        print("it worked!")
        # epic.
        copy_certs(website_id, domain)
        return True

    print("it did not work.")
    # :(
    return False


def has_certs(website_id, domain, use_www):
    # TODO Somehow check if cert is valid for www.
    return os.path.exists(f'/{ZFS_ROOT}/{website_id}/certs/live/{domain}/fullchain.pem')


def get_cert(website_id, domain, use_www):
    dataset = f'/{ZFS_ROOT}/{website_id}'
    domains = f'-d {domain} -d www.{domain}' if use_www else f'-d {domain}'
    os.system(f'docker run -it --rm -v {dataset}/web:/web -v {dataset}/certs:/etc/letsencrypt certbot/certbot certonly -n --webroot --register-unsafely-without-email --agree-tos {domains} --webroot-path /web')


def renew_cert(website_id):
    dataset = f'/{ZFS_ROOT}/{website_id}'
    os.system(f'docker run -it --rm -v {dataset}/web:/web -v {dataset}/certs:/etc/letsencrypt certbot/certbot renew')


def copy_certs(website_id, domain):
    # TODO Is rm necessary?
    os.system(f'rm -f {NGINX_CERTS_DIR}/{domain}.cert')
    os.system(f'rm -f {NGINX_CERTS_DIR}/{domain}.key')
    os.system(f'cp /{ZFS_ROOT}/{website_id}/certs/live/{domain}/fullchain.pem {NGINX_CERTS_DIR}/{domain}.cert')
    os.system(f'cp /{ZFS_ROOT}/{website_id}/certs/live/{domain}/privkey.pem {NGINX_CERTS_DIR}/{domain}.key')
