# Daemon

Install:

```sh
apt install install python3-psycopg2 python3-mysql.connector
or
pip3 install psycopg2 mysql.connector
```

Run:

```sh
export DB_HOST=""
export DB_NAME=""
export DB_USER=""
export DB_PASS=""
export DB_PORT=""
export ZFS_ROOT=""
export NGINX_SITES_DIR=""
export NGINX_CERTS_DIR=""
export NGINX_RELOAD_COMMAND="" # optional
export FTP_COMPOSE_PATH=""
export MYSQL_HOST=""
export MYSQL_PORT="" # optional, default 3306
export MYSQL_USER=""
export MYSQL_PASS=""

python3 daemon.py
```
