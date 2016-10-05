#!/bin/bash

credentials=`echo -n "$1":"$2"| base64`
plexClientIdentifier="TESTSCRIPTV1"
plexProduct="Test script"
plexVersion="V1"

url="https://plex.tv/users/sign_in.json"

curl -s -X POST -H "Authorization: Basic $credentials" \
             -H "X-Plex-Client-Identifier: $plexClientIdentifier"\
             -H "X-Plex-Product: $plexProduct"\
             -H "X-Plex-Version: $plexVersion"\
             "$url" --output user.json

