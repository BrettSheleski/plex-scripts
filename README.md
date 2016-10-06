# plex-scripts
Bash scripts for working with plex

## plex-login
Used to log into Plex and retrieve, among other things, an Authentication Token

## plex-api
Used to wrap calls to the Plex Web API (which is largely undocumented).  It internally uses `plex-login` to obtain an authentication token to use, but may use `plex-api -t XXXXXXXXX` to specify the Authentication Token.
