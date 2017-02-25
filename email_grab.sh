#!/usr/bin/env bash

grabId="$1"

plexDb="/var/lib/plex/Plex Media Server/Plug-in Support/Databases/com.plexapp.plugins.library.db"
getGrabInfo="./PlexGrab.py"

json=`$getGrabInfo "$plexDb" "$grabId"`

escapeHtml()
{
	sed 's/&/\&amp;/g; s/</\&lt;/g; s/>/\&gt;/g; s/"/\&quot;/g; s/'"'"'/\&#39;/g'
}

seriesTitle=`echo "$json" | jq -r .series_title | escapeHtml`
seasonNumber=`echo "$json" | jq -r .season_number | escapeHtml`
episodeNumber=`echo "$json" | jq -r .episode_number | escapeHtml`
episodeTitle=`echo "$json" | jq -r .episode_title | escapeHtml`
episodeSummary=`echo "$json" | jq -r .episode_summary | escapeHtml`

read -r -d '' html << EOM
<html>
<body>

<h1>$seriesTitle</h1>
<h2>Season $seasonNumber</h2>
<h3>Episode $episodeNumber</h3>
<div>$episodeTitle</div>
<p>$episodeSummary</p>
</body>
</html>
EOM

echo "$html"
