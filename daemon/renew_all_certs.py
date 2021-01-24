from db import open_db

conn = open_db()
cur = conn.cursor()

cur.execute("SELECT id FROM users_website WHERE use_https='True'")
websites = cur.fetchall()

for website in websites:
    print(f'Adding job for {website}')
    cur.execute("INSERT INTO jobs (type, priority, content, done, running) VALUES (3, 0, %s, false, false)", website)

cur.close()
conn.commit()
conn.close()
