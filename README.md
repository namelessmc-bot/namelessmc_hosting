## Development environment

Install:

```sh
apt install python3-django python3-django-crispy-forms
or
pip3 install django django-crispy-forms
cd frontend
chmod +x manage.py
./manage.py makemigrations
./manage.py migrate
```

Run:

```sh
./manage.py runserver
```

Webserver will run on localhost:8000. It will automatically reload when source code changes!
