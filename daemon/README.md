# Daemon

Install:

```sh
apt install install python3-pyzfs python3-psycopg2
or
pip3 install pyzfs psycopg2
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
export NGINX_RELOAD_COMMAND="" # optional

python3 daemon.py
```
