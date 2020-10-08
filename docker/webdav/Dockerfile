FROM ubuntu

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y apache2

RUN a2enmod dav && \
    a2enmod dav_fs && \
    echo "Listen 8070" > /etc/apache2/ports.conf && \
    chmod 777 /var/www

COPY apache.conf /etc/apache2/sites-available/000-default.conf
COPY entrypoint.sh /

CMD ["bash", "/entrypoint.sh"]
