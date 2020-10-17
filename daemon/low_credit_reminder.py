from db import open_db
import mail


conn = open_db()
cur = conn.cursor()
# Select username, email, credit, websites for all users with credit below 20
# and at least one website
# TODO use joins instead of ugly subqueries
cur.execute("SELECT username,email,(SELECT credit FROM users_account WHERE us"
            "ers_account.id = auth_user.id),(SELECT COUNT(id) FROM users_webs"
            "ite WHERE owner_id = auth_user.id GROUP BY owner_id) AS websites"
            " FROM auth_user GROUP BY auth_user.id HAVING (SELECT COUNT(id) F"
            "ROM users_website WHERE owner_id = auth_user.id GROUP BY owner_i"
            "d) > 0 AND (SELECT credit FROM users_account WHERE users_account"
            ".id = auth_user.id) < 20")
users = cur.fetchall()
cur.close()
conn.close()


for user in users:
    (username, email, credit, websites) = user

    with open('low-credit-reminder.txt', 'r') as email_file:
        email_content = email_file.read()

    days_left = int(credit / websites)

    email_content = email_content\
            .replace('{username}', username)\
            .replace('{credit}', str(credit))\
            .replace('{websites}', str(websites))\
            .replace('{days_left}', str(days_left))

    mail.send(email, 'Named hosting - Keep your websites online', email_content)
