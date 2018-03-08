FROM jfloff/alpine-python:2.7-slim
MAINTAINER shree dee <dee@labizbille.com>

RUN apk update \
	&& apk add mysql-client 

ENV MYSQL_ROOT_PASSWORD ''
ENV MYSQL_USER root
ENV MYSQL_HOST mysql-galera
ENV MYSQL_DB ''

ENV S3_BUCKET ''
ENV S3_ACCESSID ''
ENV S3_ACCESSKEY ''

#used to dnote this backup, is used as prefix for s3 storage and discoverservice
ENV BACKUP_NAME ''

ENV DISCOVERYURL ''

# by default backup every 6 hours
ENV BACKUP_INTERVAL 6

RUN /entrypoint.sh \
  -p requests \
  -p simplejson \
  -p boto \
&& echo

COPY backup.py .
RUN chmod +x backup.py


RUN echo "1.0.3" > /myVersion
CMD ["/backup.py"]


