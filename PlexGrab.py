#!/usr/bin/env python2

import sqlite3
import urllib 
import urlparse

def jsonEncoder(obj):
    val = {}
    for key in obj.__dict__:
        if not key.startswith("_"):
            val[key] = getattr(obj, key)
    return val


class Plex:
    def __init__(self, db):
        self.db = db
        self.db.row_factory = self._dict_factory

    def _dict_factory(cls, cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    def get_grab(self, grabId):
        grab = Grab(self, grabId)
        return grab

    def get_metadata_item(self, id):
        md = MetadataItem(self, id)
        return md

class MetadataItem:
    def __init__(self, plex, id = None):
        self.__plex=plex

        self.id=0
        self.library_section_id=None
        self.parent_id=None
        self.metadata_type=None
        self.guid=None
        self.media_item_count=0
        self.title=None
        self.title_sort=None
        self.original_title=None
        self.studio=None
        self.rating=0.0
        self.rating_count=None
        self.tagline=None
        self.summary=None
        self.trivia=None
        self.quotes=None
        self.content_rating=None
        self.index=0
        self.absolute_ndex=None
        self.duration=None
        self.user_thumb_url=None
        self.user_art_url=None
        self.user_banner_url=None
        self.user_music_url=None
        self.user_fields=None
        self.tags_genre=None
        self.tags_collection=None
        self.tags_director=None
        self.tags_writer=None
        self.tags_star=None
        self.originally_available_at=None
        self.available_at=None
        self.expires_at=None
        self.refreshed_at=None
        self.year=None
        self.added_at=None
        self.created_at=None
        self.updated_at=None
        self.deleted_at=None
        self.tags_country=None
        self.extra_data=None
        self.hash=None
        self.audienceRating=None
        self.changed_at=0
        self.resources_changed_at=0

        self.children=None

        if id is not None:
            self._get_from_sql(id)
    def get_parent(self):
	if self.parent_id is None:
            return None
	else:
            return MetadataItem(self.__plex, self.parent_id)

    @property
    def children(self):
        if self._children is None:
            self._children=get_children()
        return _children

    def get_children(self):
        results = []
        md = None
        if self.id is not None:
            sql="""
SELECT *
FROM metadata_items
WHERE parent_id = %i
""" % int(self.id)
            cursor=self.__plex.db.cursor()

            for row in cursor.execute(sql):
                md = MetadataItem(self.__plex)
                for key in row:
                    setattr(md, key, row[key])
                results.append(md)

        return results

    def _get_from_sql(self, id):
        sql="""
SELECT *
FROM metadata_items
WHERE id = %i
LIMIT 0,1
""" % int(id)
        cursor=self.__plex.db.cursor()
        cursor.execute(sql)
        data=cursor.fetchone()

        if data is None:
            return

        for key in data:
            setattr(self, key, data[key])

class Grab:
    def __init__(self, plex, id):
        self.__plex=plex
        self.id = id

    def get_info(self):
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

        cursor=self.__plex.db.cursor()
        cursor.execute(sql)
        grabInfo=cursor.fetchone()

        if grabInfo is None:
            return None

        if grabInfo["subscription_data"] is not None:
            subData = urlparse.parse_qs(grabInfo["subscription_data"])
            grabInfo["subscription_data"] = subData

        if grabInfo["grab_data"] is not None:
            grabInfo["grab_data"] = urlparse.parse_qs(grabInfo["grab_data"])
        
        return grabInfo

if __name__ == "__main__":
    import sys

    if (len(sys.argv) < 3):
        print """Usage: %s PLEXDB GRABID""" % sys.argv[0]
        exit(1)
    else:
        import json
        plexDb=sqlite3.connect(sys.argv[1])
        grabId=sys.argv[2]

        plex=Plex(plexDb)
        grab=plex.get_grab(grabId)

        info=grab.get_info()

        print json.dumps(info, default=jsonEncoder)
