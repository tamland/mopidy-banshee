# -*- coding: utf-8 -*-
#
# Copyright 2014 Thomas Amland
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from __future__ import unicode_literals

import os
import sqlite3
from mopidy.models import Track, Artist, Album, Playlist


class BansheeDB(object):

    def __init__(self, database_file, art_dir):
        self.database_file = database_file
        self.art_dir = art_dir

    def get_tracks(self):
        con = sqlite3.connect(self.database_file)
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
        tracks = [self._create_track(row) for row in con.execute(q)]
        con.close()
        return tracks

    def get_playlists(self):
        con = sqlite3.connect(self.database_file)
        con.row_factory = sqlite3.Row
        q = """SELECT PlaylistID, Name FROM CorePlaylists"""
        playlists = [Playlist(uri='banshee:playlist:%d' % int(row[b'PlaylistID']),
                              name=row[b'Name']) for row in con.execute(q)]
        con.close()
        return playlists

    def get_playlist_tracks(self, playlist_id):
        con = sqlite3.connect(self.database_file)
        con.row_factory = sqlite3.Row
        q = """
            SELECT CoreTracks.Title AS TrackName, CoreTracks.Uri,
            CoreTracks.TrackNumber, CoreTracks.Year, CoreTracks.Duration,
            CoreArtists.Name AS ArtistName, CoreAlbums.Title AS AlbumName,
            CoreAlbums.ArtworkID
            FROM CorePlaylistEntries
            LEFT OUTER JOIN CoreTracks ON CoreTracks.TrackID = CorePlaylistEntries.TrackID
            LEFT OUTER JOIN CoreArtists ON CoreArtists.ArtistID = CoreTracks.ArtistID
            LEFT OUTER JOIN CoreAlbums ON CoreAlbums.AlbumID = CoreTracks.AlbumID
            WHERE CorePlaylistEntries.PlaylistID = ?
            """
        tracks = [self._create_track(row) for row in con.execute(q, (playlist_id,))]
        con.close()
        return tracks


    def _create_track(self, row):
        art_id = row[b'ArtworkID']
        images = [os.path.join(self.art_dir, art_id + '.jpg')] if art_id else []
        artist = Artist(name=row[b'ArtistName'],)
        album = Album(
            name=row[b'AlbumName'],
            artists=[artist],
            images=images)
        track = Track(
            name=row[b'TrackName'],
            track_no=row[b'TrackNumber'],
            artists=[artist],
            album=album,
            uri=row[b'Uri'],
            date=unicode(row[b'Year']),
            length=row[b'Duration'])
        return track
