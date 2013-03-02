Changelog
=========

2.13.5 (unreleased)
-------------------

- Fixed a bug which might occur on Windows when two cache entries have been
  stored without `time.time()` having changed and the cache gets purged
  afterwards.

2.13.4 (2011-07-03)
-------------------

- Copy code from `App.Extensions` to keep compatibility with Zope 2.14.

2.13.3 (2010-08-31)
-------------------

- LP #142501: Only connect upon ZODB load if a new flag ``connect_on_load``
  has been set to a true value (which is its default for backwards
  compatibility).

- LP #142689: Actually use SQL connection titles in the list of
  connections returned by SQL.SQLConnectionIDs.

2.13.2 (2010-07-09)
-------------------

- Actually establish Zope 2.12 compatibility by dealing with all cases of
  moved classes and functions.

2.13.1 (2010-07-09)
-------------------

- Made compatible with Zope 2.12.9.

2.13.0 (2010-07-09)
-------------------

- Released as separate package.
