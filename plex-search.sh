#!/bin/bash

plexServer="localhost"
plexPort=32400
plexToken=`cat user.json | jq -r .user.authToken`

searchTerm=$1

curl -X GET  -H "X-Plex-Token: aSKm4Dx59sfnEk1kDP8Y"  http://"$plexServer":$plexPort/search?query=searchTerm
