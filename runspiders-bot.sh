#!/usr/bin/env bash

if [ -f /home/ecodomen/ecodomen-dev/.env ]; then
  export $(echo $(cat /home/ecodomen/ecodomen-dev/.env | sed 's/#.*//g'| xargs) | envsubst)
fi

source /home/ecodomen/ecodomen-dev/env/bin/activate
cd /home/ecodomen/ecodomen-dev/
pythton3 /home/ecodomen/ecodomen-dev/src/telegram_bot/__main__.py

deactivate