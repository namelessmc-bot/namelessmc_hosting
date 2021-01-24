from os import environ
import mysql.connector
from mysql.connector.errors import DatabaseError

def get_db():
    return mysql.connector.connect(
        host=environ['MYSQL_HOST'],
        port=int(environ['MYSQL_PORT']) if 'MYSQL_PORT' in environ else 3306,
        user=environ['MYSQL_USER'],
        password=environ['MYSQL_PASS']
    )

def run_query(cur, query, ignore_error=False):
    print('Running query', query)
    if ignore_error:
        try:
            cur.execute(query)
        except DatabaseError as error:
            print('Ignoring error', error)
            return False
    else:
        cur.execute(query)

    return True

def change_password(username, password, cur):
    if cur is None:
        existing_cur = False
        conn = get_db()
        cur = conn.cursor()
    else:
        existing_cur = True

    run_query(cur, f'ALTER USER "{username}"@"localhost" IDENTIFIED BY "{password}"')
    run_query(cur, f'ALTER USER "{username}"@"%" IDENTIFIED BY "{password}"')

    if not existing_cur:
        run_query(cur,  'FLUSH PRIVILEGES')
        cur.close()
        conn.close()

def create_user(username, password, database):
    conn = get_db()
    cur = conn.cursor()

    a = run_query(cur, f'CREATE USER "{username}"@"localhost" IDENTIFIED BY "{password}"', True)
    b = run_query(cur, f'CREATE USER "{username}"@"%" IDENTIFIED BY "{password}"', True)
    if not a or not b:
        print('Creating user failed, try changing password')
        change_password(username, password, cur)
    run_query(cur, f'CREATE DATABASE {database}', True)
    run_query(cur, f'GRANT ALL PRIVILEGES ON {database}.* TO "{username}"@"localhost"')
    run_query(cur, f'GRANT ALL PRIVILEGES ON {database}.* TO "{username}"@"%"')
    run_query(cur,  'FLUSH PRIVILEGES')
    cur.close()
    conn.commit()
    conn.close()


def install(website_id, db_password):
    username = 'user_' + str(website_id)
    database = 'site_' + str(website_id)
    create_user(username, db_password, database)


def install_all():
    from db import open_db
    conn = open_db()
    cur = conn.cursor()
    cur.execute("SELECT id,db_password FROM users_website")
    websites = cur.fetchall()
    for website in websites:
        (website_id, db_password) = website
        print('Installing site', website_id)
        install(website_id, db_password)
    cur.close()
    conn.close()

def reset(website_id):
    database = 'site_' + str(website_id)

    conn = get_db()
    cur = conn.cursor()
    run_query(cur, f'DROP DATABASE {database}', True)
    run_query(cur, f'CREATE DATABASE {database}', True)
    cur.close()
    conn.commit()
    conn.close()

def uninstall(website_id):
    username = 'user_' + str(website_id)
    database = 'site_' + str(website_id)

    conn = get_db()
    cur = conn.cursor()
    run_query(cur, f'DROP USER "{username}"@"localhost"', True)
    run_query(cur, f'DROP USER "{username}"@"%"', True)
    run_query(cur, f'DROP DATABASE "{database}"', True)
    run_query(cur,  'FLUSH PRIVILEGES')
    cur.close()
    conn.commit()
    conn.close()
