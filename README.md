# docker_bugzilla_sqlcluster
a docker stack with bugzilla, testopia and galera cluster


the container backs up the data to s3 every 6 hours
to restore the database:
download the backup C:\tmp\restorebugs and rename to bugs.sql

docker run -it --rm --network bugzilladocker_default -v C:\tmp\restorebugs:/dbdata  alpine /bin/sh

cd /dbdata
apk add --no-cache mysql-client
mysql -u root -h  mysql-galera -pa3JRlcIJaJ7sPLmkzudG
show databases;
drop database bugsdb;
create database bugsdb;
use bugsdb;
source bugs.sql;



