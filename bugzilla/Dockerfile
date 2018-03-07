FROM ubuntu:14.04
MAINTAINER shree dee <dee@labizbille.com>

EXPOSE 80

RUN echo "1.565.1" > .lts-version-number

RUN apt-get update && apt-get install -y wget git curl zip vim
RUN apt-get update && apt-get install -y \
	apache2 php5 perl libapache2-mod-perl2 php5-mysql libdbd-mysql-perl libdatetime-format-builder-perl libemail-abstract-perl libemail-send-perl \
	libemail-simple-perl libemail-mime-perl libtemplate-perl libmath-random-isaac-perl libgd-text-perl libgd-graph-perl libxml-twig-perl libchart-perl \
	libnet-ldapapi-perl libtemplate-plugin-gd-perl  libfile-slurp-perl libhtml-scrubber-perl libhtml-formattext-withlinks-perl libjson-rpc-perl libjson-xs-perl \
	libnet-ldap-perl libauthen-radius-perl libencode-detect-perl libfile-mimeinfo-perl libio-stringy-perl libdaemon-generic-perl


RUN apt-get update && apt-get install -y php5-intl imagemagick


RUN usermod -U www-data && chsh -s /bin/bash www-data

#RUN echo 'ServerName ${SERVER_NAME}' >> /etc/apache2/conf-enabled/servername.conf

COPY enable-var-www-html-htaccess.conf /etc/apache2/conf-enabled/
RUN a2enmod rewrite cgi perl headers

VOLUME "/var/log"


ENV SERVER_NAME docker-apache-php


RUN apt-get update && apt-get install -y \
        perl libapache2-mod-perl2 php5-mysql libdbd-mysql-perl libdatetime-format-builder-perl libemail-abstract-perl libemail-send-perl libemail-simple-perl \
		libemail-mime-perl libtemplate-perl libmath-random-isaac-perl libgd-text-perl libgd-graph-perl libxml-twig-perl libchart-perl libnet-ldapapi-perl libtemplate-plugin-gd-perl  \
		libfile-slurp-perl libhtml-scrubber-perl libhtml-formattext-withlinks-perl libjson-rpc-perl libjson-xs-perl \
		libnet-ldap-perl libauthen-radius-perl libencode-detect-perl libfile-mimeinfo-perl libio-stringy-perl libdaemon-generic-perl

#RUN apt-get install -y mysql-client

#RUN apt-get install -y gcc make

#COPY config/php.ini /usr/local/etc/php/

WORKDIR /var/www

#get bugzilla, extract it, remove the current html folder and install bugzilla in it
ADD https://ftp.mozilla.org/pub/mozilla.org/webtools/bugzilla-4.4.13.tar.gz ./
RUN tar zxvf bugzilla-4.4.13.tar.gz  \
	&& rm bugzilla-4.4.13.tar.gz && rm -r html && mv bugzilla-4.4.13 html

ENV MYSQL_ROOT_PASSWORD ''
ENV MYSQL_USER root
ENV MYSQL_HOST mysql-galera
ENV MYSQL_DB bugsdb

ENV ADMIN_EMAIL noreply@admin.com
ENV ADMIN_PASSWORD admin12345
ENV ADMIN_REALNAME bugsAdmin
ENV URLBASE ''
ENV SMTP_SERVER ''

COPY run_apache.sh /var/www/

COPY initdb.pl /var/www/

WORKDIR /var/www/html

COPY config/localconfig ./
COPY src/ ./

CMD ["/var/www/run_apache.sh"]

