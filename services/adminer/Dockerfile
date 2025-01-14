FROM php-base:7.4

EXPOSE 9000

WORKDIR /home/container

RUN mkdir -p /home/container/
RUN mkdir -p /home/container/adminer

COPY www.conf /etc/php/7.4/fpm/pool.d/

RUN chown -R www-data /home/container/
RUN chmod -R 750 /home/container/

RUN apt-get install curl php7.4-pgsql -y

RUN curl -L https://github.com/vrana/adminer/releases/download/v4.8.1/adminer-4.8.1.php -o \
	/home/container/adminer/index.php

CMD ["php-fpm7.4", "-F"]