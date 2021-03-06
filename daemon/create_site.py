import compose
import db
import zfs
import nginx
import ftp
import sitedb

def get_website_info(website_id):
    with db.open_db() as conn:
        with conn.cursor() as cur:
            query = "SELECT domain,use_https,db_password,files_password,version,www,name,username,email FROM users_website JOIN auth_user ON owner_id = auth_user.id WHERE users_website.id=%s"
            cur.execute(query, (website_id,))
            data = cur.fetchone()
            return data


def run(website_id):
    (domain, use_https, db_password, files_password, version, use_www, site_name, username, email) = get_website_info(website_id)

    zfs.create_website_dataset(website_id)
    sitedb.install(website_id, db_password)
    compose.install(website_id, domain, use_https, db_password, files_password, version, site_name, username, email)
    nginx.install(website_id, domain, use_https, use_www)
    ftp.add_account(website_id, files_password)
