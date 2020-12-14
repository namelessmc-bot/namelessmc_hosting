import compose

from db import open_db

conn = open_db()
cur = conn.cursor()

cur.execute("SELECT id FROM users_website")
websites = cur.fetchall()

for website in websites:
    (website_id,) = website
    print(f'Shutting down website {website_id}')
    compose.uninstall(website_id)

cur.close()
conn.commit()
conn.close()
