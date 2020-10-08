import os

ZFS_ROOT = os.environ['ZFS_ROOT']
NGINX_CERTS_DIR = os.environ['NGINX_CERTS_DIR']


def has_certs(website_id, domain):
    return os.path.exists(f'/{ZFS_ROOT}/{website_id}/certs/live/{domain}/fullchain.pem')


def get_cert(website_id, domain):
    dataset = f'/{ZFS_ROOT}/{website_id}'
    os.system(f'docker run -it --rm -v {dataset}/web:/web -v {dataset}/certs:/etc/letsencrypt certbot/certbot certonly -n --webroot --register-unsafely-without-email --agree-tos -d {domain} --webroot-path /web')


def renew_cert(website_id):
    dataset = f'/{ZFS_ROOT}/{website_id}'
    os.system(f'docker run -it --rm -v {dataset}/web:/web -v {dataset}/certs:/etc/letsencrypt certbot/certbot renew')


def copy_certs(website_id, domain):
    # TODO Is rm necessary?
    os.system(f'rm -f {NGINX_CERTS_DIR}/{domain}.cert')
    os.system(f'rm -f {NGINX_CERTS_DIR}/{domain}.key')
    os.system(f'cp /{ZFS_ROOT}/{website_id}/certs/live/{domain}/fullchain.pem {NGINX_CERTS_DIR}/{domain}.cert')
    os.system(f'cp /{ZFS_ROOT}/{website_id}/certs/live/{domain}/privkey.pem {NGINX_CERTS_DIR}/{domain}.key')
