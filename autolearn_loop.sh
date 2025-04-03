
#!/bin/bash

while true
do
  echo "$(date): Veriler çekiliyor..." >> /root/elitegpt/autolearn_log.txt
  python3 /root/elitegpt_autolearn.py
  cp /root/memory_scraped.json /root/elitegpt/memory_dynamic.json
  sleep 30
done
