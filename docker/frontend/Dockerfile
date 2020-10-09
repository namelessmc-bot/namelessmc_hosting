FROM python:3

RUN pip install django django-crispy-forms gunicorn psycopg2 django-paypal

ADD app/ /app

WORKDIR /app

RUN chmod +x manage.py

ENV PROD=true
CMD bash -c "./manage.py makemigrations && ./manage.py migrate && ./manage.py collectstatic --no-input && gunicorn --bind 0.0.0.0:80 namelessmc_hosting.wsgi"
