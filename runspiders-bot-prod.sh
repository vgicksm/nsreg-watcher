#!/usr/bin/env bash

if [ -f /home/ecodomen/ecodomen-dev/.env ]; then
  export $(echo $(cat /home/ecodomen/ecodomen-prod/.env | sed 's/#.*//g'| xargs) | envsubst)
fi

source /home/ecodomen/ecodomen-prod/env/bin/activate
cd /home/ecodomen/ecodomen-prod/
python3 /home/ecodomen/ecodomen-prod/src/telegram_bot/__main__.py

deactivate