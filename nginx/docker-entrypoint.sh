#!/usr/bin/env bash

export DOLLAR='$'

echo "\
############################## Prepare nginx.conf ##############################\
"

echo "APP_SERVER_UPSTREAM: ${APP_SERVER_UPSTREAM}"
echo "APP_SERVER_SERVICE: ${APP_SERVER_SERVICE}"
echo "APP_SERVER_PORT: ${APP_SERVER_PORT}"

envsubst < /etc/nginx/templates/nginx.conf.template > /etc/nginx/nginx.conf

echo "\
################# Nginx Configuration (/etc/nginx/nginx.conf) ##################\
"

cat /etc/nginx/nginx.conf

nginx -g "daemon off;"
