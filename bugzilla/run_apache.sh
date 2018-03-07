#!/bin/bash

sed -i "s/%MYSQL_ROOT_PASSWORD%/${MYSQL_ROOT_PASSWORD}/g" ./localconfig 
sed -i "s/%MYSQL_USER%/$MYSQL_USER/g" ./localconfig 
sed -i "s/%MYSQL_HOST%/$MYSQL_HOST/g" ./localconfig 
sed -i "s/%MYSQL_DB%/$MYSQL_DB/g" ./localconfig 

echo "\$answer{'ADMIN_EMAIL'} = '$ADMIN_EMAIL';" > ./localdata
echo "\$answer{'ADMIN_PASSWORD'} = '$ADMIN_PASSWORD';" >> ./localdata
echo "\$answer{'ADMIN_REALNAME'} = '$ADMIN_REALNAME';" >> ./localdata
echo "\$answer{'SMTP_SERVER'} = '$SMTP_SERVER';" >> ./localdata
echo "\$answer{'NO_PAUSE'} = 1;" >> ./localdata

set |grep '_PORT_' |tr  '=' ' ' |sed 's/^/SetEnv /' > /etc/apache2/conf-enabled/docker-vars.conf
set |grep '_ENV_' |tr  '=' ' ' |sed 's/^/SetEnv /' >> /etc/apache2/conf-enabled/docker-vars.conf
set |grep 'SERVER_NAME' |tr  '=' ' ' |sed 's/^/SetEnv /' >> /etc/apache2/conf-enabled/docker-vars.conf

set |grep '_PORT_'  |sed 's/^/export /'>> /etc/apache2/envvars

echo "export SERVER_NAME=$SERVERNAME" >> /etc/apache2/envvars

echo "ServerName $SERVER_NAME" >> /etc/apache2/conf-enabled/servername.conf

echo "running checksetup"
#./checksetup.pl localdata


/etc/init.d/apache2 start && \
tail -F /var/log/apache2/*log

#service rsyslog start && \
#service postfix start && \
#tail -F /var/log/mail.log
