# Nameless Hosting

## Contributing

You can find the frontend code in `frontend/`. If you're looking for HTML, that's in `users/templates/users` and `main/templates/main`. For instructions on how to easily run a local server to test your changes, see below. The other component of this hosting system is a daemon. Unfortunately, it's hard to contribute to this because you can't really run this on your local machine. At least for right now it has hardcoded strings and closed source components.

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
