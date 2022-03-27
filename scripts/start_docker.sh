#!/bin/sh

# wait for the service to be ready
(while true; do
  if curl -sL --fail http://localhost:8020 -o /dev/null; then
    sleep 1
    open http://localhost
    break
  else
    sleep 1
  fi
done) &

# start the container stack
docker-compose up 