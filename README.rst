caliload
========

Copyright 2011 Brendan Kidwell <brendan@glump.net>

``caliload`` is a wrapper script for various Calibre command line tools that allows you to add and update books from an offline library.

The idea is that you can manage an ebook library *outside* of Calibre and use tools like Dropbox to synchronize the external file-based library, but still have the benefit of Calibre's ebook-reader syncing, conversion, and metadata editing tools.

Additionally, since Calibre doesn't provide an easy way to push metadata from the Calibre database to content files registered in Calibre, ``caliload`` provides this with the ``db_push_meta`` command.

In order to create an ID for the book outside of Calibre (since the book may be loaded into more than one Calibre database) ``caliload`` uses a custom Dublin Core metadata ``identifier`` element with the schema name ``caliload`` and a UUID for a value

*Note:* ``caliload`` only works on ``epub`` and ``pdf`` files at the moment. Furthermore, any files beginning with "_" (underscore) are ignored; this way you can keep original unmodified copies side-by-side with your working copies.

Requirements
------------

* Python 2.7+
* Calibre

Installation
------------

Currently no installation script or package.

* Unzip the `caliload` folder from the distribution archive to a convenient place like `~/Apps`.
* Make a symlink `~/bin/caliload` pointing to `~/Apps/caliload/caliload.py`.

Example Usage
-------------

::

   mkdir ~/Ebooks
   cd ~/Ebooks
   mkdir "Carroll - Alice in Wonderland"
   cd "Carroll - Alice in Wonderland"
   wget http://example.com/alice.epub
   caliload db_add  # load epub file
   
   # Use Calibre to edit the the new record, set tags, etc.
   # Then come back here.
   
   caliload db_meta_pull  # push metadata from database to all other
                          # copies of content and metadata

See the ``--help`` option for more details.