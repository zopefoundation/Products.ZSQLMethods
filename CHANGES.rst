Changelog
=========

3.2 (2020-02-11)
----------------

- Fix support for editing ZSQL Methods via WebDAV
  (`#22 <https://github.com/zopefoundation/Products.ZSQLMethods/issues/22>`_)


3.1 (2020-02-09)
----------------

- Pull in WebDAV support from Zope and pin Zope to 4.2.1 or higher


3.0.13 (2020-02-04)
-------------------

- Pin ``DocumentTemplate`` 3.2.2 for less quoting, it is to database-specific


3.0.12 (2020-02-03)
-------------------

- Depend on ``DocumentTemplate`` 3.2.1+ to no longer escape ``"``


3.0.11 (2020-01-31)
-------------------

- Depend on ``DocumentTemplate`` 3.1+ to do SQL quoting.


3.0.10 (2020-01-29)
-------------------

- remove Zope Help System fossils so the product works with Zope 5


3.0.9 (2019-11-22)
------------------

- fix ImportError under Zope 5 due to moved dependencies
  (`#19 <https://github.com/zopefoundation/Products.ZSQLMethods/pull/19>`_)


3.0.8 (2019-08-05)
------------------

- show rendered SQL output even if an exception occurred
  (`#15 <https://github.com/zopefoundation/Products.ZSQLMethods/issues/15>`_)

- fix sqltest behavior with bytes inputs
  (`#14 <https://github.com/zopefoundation/Products.ZSQLMethods/issues/14>`_)


3.0.7 (2019-04-26)
------------------

- compatibility fixes for better unicode support in DocumentTemplate


3.0.6 (2019-04-03)
------------------

- fix failing unpickling of older Z SQL Methods instances
  (`#12 <https://github.com/zopefoundation/Products.ZSQLMethods/issues/12>`_)

- improve usability and add Zope 4 compatibility for connection forms

- improve general usability of the ZSQL Method edit and test forms

- enable the fancy editor for the ZSQL Method edit form

- sanitize ``tox`` and ``flake8`` configurations, reach ``flake8`` compliance


3.0.5 (2019-03-29)
------------------

- Fix all ZMI forms for ZSQL Methods for Zope 4
  (`#11 <https://github.com/zopefoundation/Products.ZSQLMethods/issues/11>`_)


3.0.4 (2019-02-17)
------------------

- Specify supported Python versions using ``python_requires`` in setup.py
  (`Zope#481 <https://github.com/zopefoundation/Zope/issues/481>`_)

- Added support for Python 3.7 and 3.8


3.0.3 (2018-06-11)
------------------

- Fix long-standing bug of setting an ``int`` as return value
  for the transaction manager's ``sortKey`` method. It must be a string.

- PEP-8 compliance

- clean out all ``install_requires`` that are already required by ``Zope``

- only claim to support Python versions supported by Zope itself


3.0.2 (2018-03-16)
------------------

- Add flake8 code checking

- Add test coverage computation.

- Various small Python 3 compatibility changes.


3.0.1 (2017-10-18)
------------------

- Fix syntax error in `Shared/DC/ZRDB/dbi_db.py`.

- More PEP8 compliance.


3.0.0 (2017-05-23)
------------------

- added tox configuration

- Python 3 compatibility


3.0.0b1 (2017-05-03)
--------------------

- Target use with Zope 4:  no longer support 2.13.x.

- Make webdav from ZServer optional
  [dataflake]

2.13.5 (2016-11-10)
-------------------

- Strip ``NUL`` bytes when quoting SQL string literals.

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
