import os
import db


FTP_COMPOSE_PATH = os.environ['FTP_COMPOSE_PATH']


def add_account(website_id, password):
    username = f'user_{website_id}'
    print(f'Adding sftp config for {username}')
    os.system(f'(echo "{password}"; echo "{password}") | docker-compose -f "{FTP_COMPOSE_PATH}" exec -T ftp pure-pw useradd {username} -f /etc/pure-ftpd/passwd/pureftpd.passwd -m -u 33 -g 33 -d /data/{website_id}/web')


def recreate():
    with db.open_db() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id,files_password FROM users_website")
            websites = cur.fetchall()

    os.system(f'docker-compose -f "{FTP_COMPOSE_PATH}" exec -T ftp rm /etc/pure-ftpd/passwd/pureftpd.passwd')
    for website in websites:
        (website_id, password) = website
        add_account(website_id, password)
