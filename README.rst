===============================
Mopidy-Banshee
===============================

`Mopidy <http://mopidy.com>`_ extension for playing music from
`Banshee <http://banshee.fm>`_.


Installation
============

Install by running::

    pip install mopidy-banshee


Configuration
=============

Before starting Mopidy, specify the location of the Banshee database file in
your Mopidy configuration::

    [banshee]
    db = some/path/banshee.db

By default the database is loaded from `~/.config/banshee-1/banshee.db`.
