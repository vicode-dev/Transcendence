FROM debian:bookworm

RUN apt-get update -y && apt-get upgrade -y \
	&& apt-get -y install lsb-release apt-transport-https ca-certificates wget -y \
	&& wget -O /etc/apt/trusted.gpg.d/php.gpg https://packages.sury.org/php/apt.gpg \
	&& echo "deb https://packages.sury.org/php/ $(lsb_release -sc) main" | tee /etc/apt/sources.list.d/php.list \
	&& apt-get update -y \
	&& mkdir -p /run/php && chown -R www-data:www-data /run/php
