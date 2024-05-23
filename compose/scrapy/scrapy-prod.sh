#!/usr/bin/env bash
sleep 10

if [ -f /home/ecodomen/ecodomen-prod/.env ]; then
  export $(echo $(cat /home/ecodomen/ecodomen-prod/.env | sed 's/#.*//g'| xargs) | envsubst)
fi

. /home/ecodomen/ecodomen-prod/env/bin/activate

ERROR_LOG="$(cd "$(dirname "logs/grabber_errors.log")"; pwd)/$(basename "logs/grabber_errors.log")"
LOG_LEVEL=ERROR
DATE=$(date +”%d-%b-%Y_%H:%M”)

echo "truncating error file:  $ERROR_LOG"
echo '---SPLIT---' >> $ERROR_LOG

cd /home/ecodomen/ecodomen-prod/src/grabber/nsreg

scrapy crawl monitor --logfile $ERROR_LOG --loglevel $LOG_LEVEL
scrapy list | awk '$1 != "monitor" {print $1}' | xargs -n 1 scrapy crawl --logfile $ERROR_LOG --loglevel $LOG_LEVEL

deactivate
cd ../../..
