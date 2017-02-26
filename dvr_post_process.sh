#!/usr/bin/env bash
infile="$1"
plexDb="/var/lib/plex/Plex Media Server/Plug-in Support/Databases/com.plexapp.plugins.library.db"
grabId=`dirname "$infile"`
grabId=`basename "$grabId"`

plexGrab="PlexGrab.py"

#Get script dir
SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ]; do # resolve $SOURCE until the file is no longer a symlink
  DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
  SOURCE="$(readlink "$SOURCE")"
  [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE" # if $SOURCE was a relative symlink, we need to resolve it relative to the path where the symlink file was located
done
DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"

plexGrab="$DIR/$plexGrab"

function postProcessGrab(){
        sleep 10
        $plexGrab "$plexDb" "$grabId" > $DIR/plexGrab.log
}
postProcessGrab &
