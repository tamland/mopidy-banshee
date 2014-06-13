# -*- coding: utf-8 -*-
#
# Copyright (C) 2014 Thomas Amland
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
from __future__ import unicode_literals

import os
import sqlite3
from functools import partial
from mopidy.models import Track, Artist, Album



def get_tracks(database, art_dir):
    con = sqlite3.connect(database)
    con.row_factory = sqlite3.Row
    q = """
        SELECT CoreTracks.Title AS TrackName, CoreTracks.Uri,
        CoreTracks.TrackNumber, CoreTracks.Year, CoreTracks.Duration,
        CoreArtists.Name AS ArtistName, CoreAlbums.Title AS AlbumName,
        CoreAlbums.ArtworkID
        FROM CoreTracks
        LEFT OUTER JOIN CoreArtists ON CoreArtists.ArtistID = CoreTracks.ArtistID
        LEFT OUTER JOIN CoreAlbums ON CoreAlbums.AlbumID = CoreTracks.AlbumID
        """
    create_track = partial(_create_track, art_dir=art_dir)
    tracks = [create_track(row) for row in con.execute(q)]
    con.close()
    return tracks


def _create_track(row, art_dir):
    art_id = row[b'ArtworkID']
    images = [os.path.join(art_dir, art_id + '.jpg')] if art_id else []
    artist = Artist(name=row[b'ArtistName'],)
    album = Album(
        name=row[b'AlbumName'],
        artists=[artist],
        images=images)
    track = Track(
        name=row[b'TrackName'],
        track_no=int(row[b'TrackNumber']),
        artists=[artist],
        album=album,
        uri=row[b'Uri'],
        date=unicode(row[b'Year']),
        length=row[b'Duration'])
    return track


if __name__ == '__main__':
    t = get_tracks({'artist': ['D1']})
    print(t)