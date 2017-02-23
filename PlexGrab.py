#!/usr/bin/env python2

import sqlite3
import urllib 
import urlparse

def dict_factory(cursor, row):
	d = {}
	for idx, col in enumerate(cursor.description):
		d[col[0]] = row[idx]
	return d

class PlexGrab:
	def __init__(self, dbPath, id):
		self.id = id
		self.db = sqlite3.connect(dbPath)
		self.db.row_factory = dict_factory

	def getInfo(self):
		sql="""SELECT
series.title AS 'series_title',
season.'index' AS 'season_number',
episode.'index' AS 'episode_number',
episode.title AS 'episode_title',
episode.summary AS 'episode_summary',
p.file AS 'file_path',
grab.uuid AS 'grab_id',
grab.extra_data AS 'grab_data',
subscription.extra_data AS 'subscription_data'
FROM media_grabs as grab
INNER JOIN metadata_items AS episode
    ON grab.metadata_item_id = episode.id
INNER JOIN metadata_items AS season
    ON episode.parent_id = season.id
INNER JOIN metadata_items AS series
    ON season.parent_id = series.id
INNER JOIN media_items AS m
    ON episode.id = m.metadata_item_id
INNER JOIN media_parts AS p
    ON m.id = p.media_item_id
LEFT OUTER JOIN media_subscriptions AS subscription
    ON grab.media_subscription_id = subscription.id
WHERE 1=1
AND grab.uuid='%s'
LIMIT 0,1
""" % self.id

		cursor=self.db.cursor()
		cursor.execute(sql)
		grabInfo=cursor.fetchone()
		if grabInfo["subscription_data"] is not None:
			grabInfo["subscription_data"] = urlparse.parse_qs(grabInfo["subscription_data"])

		if grabInfo["grab_data"] is not None:
			grabInfo["grab_data"] = urlparse.parse_qs(grabInfo["grab_data"])
		
		return grabInfo

if __name__ == "__main__":
	import sys

	if (len(sys.argv) < 3):
		print "specify path to Plex DB as well as grab ID"
	else:
		import json
		plexDb=sys.argv[1]
		grabId=sys.argv[2]
		grab=PlexGrab(plexDb, grabId)

		info=grab.getInfo()

		print json.dumps(info)
