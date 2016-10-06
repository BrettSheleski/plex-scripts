#!/bin/bash

plexServer="localhost"
plexPort=32400
plexToken=""
format="xml"
accept="text/xml"

while [[ $# -gt 1 ]]
do
key="$1"
case $key in
    -s|--server)
    plexServer="$2"
    shift
    ;;
    -p|--port)
    plexPort="$2"
    shift
    ;;
    -t|--token)
    plexToken="$2"
    shift
    ;;
    -f|--format)
    format="$2"
    shift
    ;;
esac
shift # past argument or value
done

if [ -z $plexToken ]; then
    plexToken=$(./plex-login.sh -t)
fi


case "$format" in
    json)
    accept="application/json"
    ;;

    xml)
    accept="text/xml"
    ;;

    *)
    echo "unknown format: $format, using xml"
    accept="text/xml"
    ;;
esac

path=$1

if [[ "$path" == "/"* ]]; then
  path=${path:1}
fi

url="http://$plexServer:$plexPort/$path"

curl -X GET -H "X-Plex-Token: $plexToken" -H "Accept: $accept" "$url"
