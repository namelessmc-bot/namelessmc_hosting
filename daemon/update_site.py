import compose
import db
import nginx


def get_website_info(website_id):
    with db.open_db() as conn:
        with conn.cursor() as cur:
            query = "SELECT domain,use_https,db_password,files_password,version,www FROM users_website WHERE id=%s"
            cur.execute(query, (website_id,))
            data = cur.fetchone()
            return data


def run(website_id):
    data = get_website_info(website_id)
    if data is None:
        print(f'Skip updating website, {website_id} no longer exists')
        return

    (domain, use_https, db_password, files_password, version, use_www) = data
    compose.install(website_id, domain, use_https, db_password, files_password, version)
    nginx.install(website_id, domain, use_https, use_www)
