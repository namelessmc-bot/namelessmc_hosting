import requests
import db
from requests.exceptions import RequestException, ReadTimeout


def get_website_info(website_id):
    with db.open_db() as conn:
        with conn.cursor() as cur:
            query = "SELECT domain,use_https,www FROM users_website WHERE id=%s"
            cur.execute(query, (website_id,))
            data = cur.fetchone()
            return data


def ping(website_id):
    info = get_website_info(website_id)
    if not info:
        print("Skipping ping, site doesn't exist")
        return
    (domain, use_https, www) = info
    _ping(website_id, domain, use_https, www)


def _ping(website_id, domain, use_https, www):

    url = \
        ('https://' if use_https else 'http://') + \
        ('www.' if www else '') + \
        domain + \
        '/named_hosting_magic'

    print(f'Pinging url {url}')
    try:
        response = requests.get(url, timeout=5, stream=True)
        content = response.raw.read(10+1, decode_content=True)
        if len(content) > 10:
            print('Website is not working, response too long')
            _signal_broken(website_id)
            return
    except (RequestException, ReadTimeout):
        print('Website is not working, ConnectionError')
        _signal_broken(website_id)
        return

    if content == b'yes':
        print('Website is working')
        _signal_working(website_id)
        return
    else:
        print(f'Website is not working, received {content}')
        _signal_broken(website_id)
        return


def _signal_broken(website_id):
    with db.open_db() as conn:
        with conn.cursor() as cur:
            query = "SELECT down_since FROM users_website WHERE id=%s"
            cur.execute(query, (website_id,))
            (down_since, ) = cur.fetchone()
            if down_since is None:
                query = "UPDATE users_website SET down_since = now() WHERE id=%s"
                cur.execute(query, (website_id,))
                print('Marked as down')
            else:
                # print('Not setting down time, site was already down')
                pass


def _signal_working(website_id):
    with db.open_db() as conn:
        with conn.cursor() as cur:
            query = "UPDATE users_website SET down_since = NULL WHERE id=%s"
            cur.execute(query, (website_id,))
