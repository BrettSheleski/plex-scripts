#!/bin/bash

read -p "Plex Username: " username
read -s -p "Plex Password: " password

credentials=`echo -n "$username":"$password"| base64`
plexClientIdentifier="TESTSCRIPTV1"
plexProduct="Test script"
plexVersion="V1"

url="https://plex.tv/users/sign_in.json"

json=$(curl -s -X POST -H "Authorization: Basic $credentials" \
                -H "X-Plex-Client-Identifier: $plexClientIdentifier"\
                -H "X-Plex-Product: $plexProduct"\
                -H "X-Plex-Version: $plexVersion"\
                -H "Accept: application/json"\
                "$url")

for i in "$@"
do
case $i in
    -t|--token)
    echo "$json" | jq -r .user.authToken
    shift # past argument=value
    exit
    ;;
esac
done

echo "$json"
