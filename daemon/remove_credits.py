import db

conn = db.open_db()
cur = conn.cursor()
cur.execute("SELECT owner_id, COUNT(id), (SELECT credit FROM users_account WHERE user_id=owner_id), (SELECT username FROM auth_user WHERE id=owner_id) FROM users_website GROUP BY owner_id")
users = cur.fetchall()
print(users)
for user in users:
    (user_id, website_count, credit, username) = user
    print(f'Removing credits for {username}: {credit} - {website_count}')
    new_credit = credit - website_count

    if new_credit < 0:
        new_credit = 0
        # TODO suspend websites

    cur.execute("UPDATE users_account SET credit=%s WHERE user_id=%s", (new_credit, user_id))
    conn.commit()

cur.close()
conn.close()
