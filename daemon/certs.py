import os
import db


ZFS_ROOT = os.environ['ZFS_ROOT']
NGINX_CERTS_DIR = os.environ['NGINX_CERTS_DIR']


def generate_certs(website_id, domain, use_www):
    print("Generating certs...", 'website_id', website_id, 'domain', domain, 'www', use_www)

    domains = [domain]
    if use_www:
        domains.append('www.' + domain)

    for domain in domains:
        if has_certs(website_id, domain):
            copy_certs(website_id, domain) # just in case
            print("cert already exists for domain", domain)
            continue

        print('Generating cert for', domain)

        run_certbot(website_id, domain)

        if has_certs(website_id, domain):
            print("it worked!")
            # epic.
            copy_certs(website_id, domain)
        else:
            print("it did not work.")
            # No need to try other domain if present, this way we don't run into API limits as quickly
            return False

    print('certificate created for all domains')
    return True


def has_certs(website_id, domain):
    return = os.path.exists(f'/{ZFS_ROOT}/{website_id}/certs/live/{domain}/fullchain.pem')


def run_certbot(website_id, domain):
    dataset = f'/{ZFS_ROOT}/{website_id}'
    command = f'docker run -it --rm -v {dataset}/web:/web -v {dataset}/certs:/etc/letsencrypt certbot/certbot certonly -n --webroot --register-unsafely-without-email --agree-tos -d {domain} --webroot-path /web'
    print('running certbot command:', command)
    os.system(command)


def renew_cert(website_id):
    print('Renewing cert')

    with db.open_db() as conn:
        with conn.cursor() as cur:
            query = "SELECT domain,www FROM users_website WHERE id=%s"
            cur.execute(query, (website_id,))
            website_info = cur.fetchone()

    if not website_info:
        print('Failed to retrieve website information for site ' + website_id)
        return

    (domain, use_www) = website_info

    domains = [domain]
    if use_www:
        domains.append('www.' + domain)

    for domain in domains:
        print('checking', domain)

        if not has_certs(website_id, domain):
            print('no certificate exists for this domain. attempt to generate first..')
            run_certbot(website_id, domain)

        if not has_certs(website_id, domain):
            print('certificate still doesn\'t exist, ABORT!')
            return

    print('running certbot renew')
    dataset = f'/{ZFS_ROOT}/{website_id}'
    os.system(f'docker run -it --rm -v {dataset}/web:/web -v {dataset}/certs:/etc/letsencrypt certbot/certbot renew')

    for domain in domains:
        copy_certs(website_id, domain)


def copy_certs(website_id, domain):
    print('copy cert', domain)
    # TODO Is rm necessary?
    os.system(f'rm -f {NGINX_CERTS_DIR}/{domain}.cert')
    os.system(f'rm -f {NGINX_CERTS_DIR}/{domain}.key')
    os.system(f'cp /{ZFS_ROOT}/{website_id}/certs/live/{domain}/fullchain.pem {NGINX_CERTS_DIR}/{domain}.cert')
    os.system(f'cp /{ZFS_ROOT}/{website_id}/certs/live/{domain}/privkey.pem {NGINX_CERTS_DIR}/{domain}.key')
