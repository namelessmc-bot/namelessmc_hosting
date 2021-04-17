from db import open_db

conn = open_db()
cur = conn.cursor()

cur.execute("SELECT id FROM users_website")
websites = cur.fetchall()

for website in websites:
    cur.execute("INSERT INTO jobs (type, priority, content, done, running) VALUES (5, 2, %s, false, false)", website)

cur.close()
conn.commit()
conn.close()
