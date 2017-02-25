#!/usr/bin/env bash

grabId="$1"

plexDb="/var/lib/plex/Plex Media Server/Plug-in Support/Databases/com.plexapp.plugins.library.db"
getGrabInfo="./PlexGrab.py"

json=`$getGrabInfo "$plexDb" "$grabId"`

#echo "$json"

filePath=`echo "$json" | jq -r .file_path`

#echo $filePath

if [ -e "$filePath" ]; then
  echo "file exists!"
else
  exit
fi

read -r -d '' html << EOM

EOM
