# !/bin/bash

IPADDR='127.0.0.1'
PORT='8003'

RESCRAPE=$(curl -location --request 'POST' "http://$IPADDR:$PORT/runner/web_scrape")

echo $ADMIN1