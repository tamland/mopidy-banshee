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
import logging
import traceback
from mopidy import config, ext
import mopidy
from mopidy.models import Playlist
from pykka import ThreadingActor
from mopidy.backend import LibraryProvider
from mopidy.local import search
import banshee

log = logging.getLogger('banshee')


class Extension(ext.Extension):
    dist_name = 'Mopidy-Banshee'
    ext_name = 'banshee'
    version = '0.1.0'

    def get_default_config(self):
        conf_file = os.path.join(os.path.dirname(__file__), 'ext.conf')
        return config.read(conf_file)

    def get_config_schema(self):
        schema = super(Extension, self).get_config_schema()
        schema['database_file'] = config.String()
        schema['art_dir'] = config.String()
        return schema

    def setup(self, registry):
        registry.add('backend', BansheeBackend)


class BansheeBackend(ThreadingActor, mopidy.backend.Backend):
    uri_schemes = ['banshee']

    def __init__(self, config, audio):
        super(BansheeBackend, self).__init__()
        self.config = config
        database_file = os.path.expanduser(config['banshee']['database_file'])
        art_dir = os.path.expanduser(config['banshee']['art_dir'])
        self.banshee_db = banshee.BansheeDB(database_file, art_dir)
        self.library = BansheeLibraryProvider(self, self.banshee_db)
        self.playlists = BansheePlaylistProvider(self, self.banshee_db)


class BansheeLibraryProvider(LibraryProvider):
    def __init__(self, backend, banshee_db):
        super(BansheeLibraryProvider, self).__init__(backend)
        self._tracks = None
        self.banshee_db = banshee_db

    def find_exact(self, query=None, uris=None):
        try:
            log.debug("banshee::find_exact(%s,%s)" % (repr(query), uris))
            if query is None:
                return None
            if self._tracks is None:
                self._tracks = self.banshee_db.get_tracks()
            return search.find_exact(self._tracks, query, uris)
        except Exception as e:
            traceback.print_exc()
            raise e

    def search(self, query=None, uris=None):
        log.debug("banshee::search(%s,%s)" % (query, uris))
        return self.find_exact(query, uris)

    def lookup(self, uri):
        log.debug("banshee::lookup(%s)" % (uri))
        raise NotImplementedError

    def refresh(self, uri=None):
        log.debug("banshee::refresh(%s)" % (uri))
        raise NotImplementedError


class BansheePlaylistProvider(mopidy.backend.PlaylistsProvider):
    def __init__(self, backend, banshee_db):
        super(BansheePlaylistProvider, self).__init__(backend)
        self.banshee_db = banshee_db
        self._playlists = banshee_db.get_playlists()

    def lookup(self, uri):
        pl_id = int(uri.split(':')[-1])
        tracks = self.banshee_db.get_playlist_tracks(pl_id)
        return Playlist(tracks=tracks)
