import os
import db

ZFS_ROOT = os.environ['ZFS_ROOT']


def startup():
    print('Making sure all websites are mounted in SFTP directory..')
    with db.open_db() as conn:
        with conn.cursor() as cur:
            query = "SELECT id,domain FROM users_website"
            cur.execute(query)
            websites = cur.fetchall()
            for website in websites:
                (website_id, domain) = website
                setup(website_id, domain)

    generate_users_config()


def setup(website_id, domain):
    mountpoint = f'/ssd/container/namelessmc/proxy/sftp_mounts/{domain}/web'
    web_dir = f'/{ZFS_ROOT}/{website_id}/web'
    os.system(f'mkdir -p "{mountpoint}"')
    print(f'Mounting {web_dir} to {mountpoint}')
    os.system(f'mount --bind "{web_dir}" "{mountpoint}"')


def remove(domain):
    sftp_dir = f'/ssd/container/namelessmc/proxy/sftp_mounts/{domain}'
    mountpoint = f'{sftp_dir}/web'
    print(f'Unmounting {mountpoint}')
    os.system(f'umount "{mountpoint}"')
    os.system(f'rm -rf "{sftp_dir}"')


def generate_users_config():
    print("Generating SFTP users config")
    data = ""
    with db.open_db() as conn:
        with conn.cursor() as cur:
            query = "SELECT domain,sftp_password FROM users_website"
            cur.execute(query)
            websites = cur.fetchall()
            for website in websites:
                (domain, sftp_password) = website
                data += f"{domain}:{sftp_password}:33:33\n"

    print(data)

    dest_path = '/ssd/container/namelessmc/proxy/sftp_users.conf'
    with open(dest_path, 'w') as dest_file:
        dest_file.write(data)
