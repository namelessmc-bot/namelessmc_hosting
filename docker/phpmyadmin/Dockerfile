FROM phpmyadmin/phpmyadmin

RUN sed -i 's/Listen 80/Listen 8080/g' /etc/apache2/ports.conf

ENV UPLOAD_LIMIT=100M
