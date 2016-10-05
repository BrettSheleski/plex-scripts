#!/bin/bash

plexServer="localhost"
plexPort=32400
plexToken=`cat user.json | jq -r .user.authToken`

searchTerm=$1

curl -X GET  -H "X-Plex-Token: $plexToken"  http://"$plexServer":$plexPort/search?query=$searchTerm
