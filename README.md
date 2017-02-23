# plex-scripts
Various scripts for working with plex

## PlexGrab.py
Python (v2.x) script for getting various information of a recording (aka: 'grab').

### Usage:
`python2 PlexGrab.py <PLEX_DB_PATH> <GRAB_ID>`

## plex-login
Used to log into Plex and retrieve, among other things, an Authentication Token

## plex-api
Used to wrap calls to the Plex Web API (which is largely undocumented).  It internally uses `plex-login` to obtain an authentication token to use, but may use `plex-api -t XXXXXXXXX` to specify the Authentication Token.
