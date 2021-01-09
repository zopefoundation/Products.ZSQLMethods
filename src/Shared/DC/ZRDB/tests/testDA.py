##############################################################################
#
# Copyright (c) 2010 Zope Foundation and Contributors.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE
#
##############################################################################

import unittest

from Testing.makerequest import makerequest


class TestTM(unittest.TestCase):

    def _getTargetClass(self):
        from ..DA import DA
        return DA

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_instantiation(self):
        da = self._makeOne('test_id', 'Test Title', 'conn_id',
                           'foo bar', '<dtml-var bar>')
        self.assertEqual(da.getId(), 'test_id')
        self.assertEqual(da.title, 'Test Title')
        self.assertEqual(da.connection_id, 'conn_id')
        self.assertEqual(da.arguments_src, 'foo bar')
        self.assertEqual(da.src, '<dtml-var bar>')

    def test_manage_edit(self):
        da = self._makeOne('test_id', 'Test Title', 'conn_id',
                           'foo bar', '<dtml-var bar>')
        da.manage_edit('New Title', 'conn_2', 'bar baz', '<dtml-var baz>')
        self.assertEqual(da.getId(), 'test_id')
        self.assertEqual(da.title, 'New Title')
        self.assertEqual(da.connection_id, 'conn_2')
        self.assertEqual(da.arguments_src, 'bar baz')
        self.assertEqual(da.src, '<dtml-var baz>')

    def test_manage_advanced(self):
        klass = self._getTargetClass()
        da = self._makeOne('test_id', 'Test Title', 'conn_id',
                           'foo bar', '<dtml-var bar>')

        # Check defaults
        self.assertEqual(da.max_rows_, klass.max_rows_)
        self.assertEqual(da.max_cache_, klass.max_cache_)
        self.assertEqual(da.cache_time_, klass.cache_time_)
        self.assertEqual(da.class_name_, klass.class_name_)
        self.assertEqual(da.class_file_, klass.class_file_)
        self.assertEqual(da.allow_simple_one_argument_traversal,
                         klass.allow_simple_one_argument_traversal)
        self.assertEqual(da.template_class, klass.template_class)
        self.assertEqual(da.connection_hook, klass.connection_hook)

        da.manage_advanced(5, 50, 10, 'MyRecord', 'ZSQLMethods.TestRecord',
                           direct=True, connection_hook='foo')
        self.assertEqual(da.max_rows_, 5)
        self.assertEqual(da.max_cache_, 50)
        self.assertEqual(da.cache_time_, 10)
        self.assertEqual(da.class_name_, 'MyRecord')
        self.assertEqual(da.class_file_, 'ZSQLMethods.TestRecord')
        self.assertEqual(da.allow_simple_one_argument_traversal, True)
        self.assertEqual(da.template_class, klass.template_class)
        self.assertEqual(da.connection_hook, 'foo')

    def test_manage_DAVget(self):
        da = makerequest(self._makeOne('test_id', 'Test Title', 'conn_id',
                                       'foo bar', '<dtml-var bar>'))
        self.assertEqual(da.manage_DAVget(), DEFAULT_DAV_SOURCE)

        da.manage_edit('New Title', 'conn_2', 'bar baz', '<dtml-var baz>')
        da.manage_advanced(5, 50, 10, 'MyRecord', 'ZSQLMethods.TestRecord',
                           direct=True, connection_hook='foo')
        self.assertEqual(da.manage_DAVget(), CHANGED_DAV_SOURCE)

    def test_PUT(self):
        klass = self._getTargetClass()
        da = makerequest(self._makeOne('test_id', 'Test Title', 'conn_id',
                                       'foo bar', '<dtml-var bar>'))

        da.REQUEST.set('BODY', CHANGED_DAV_SOURCE)
        da.PUT(da.REQUEST, da.REQUEST.RESPONSE)
        self.assertEqual(da.getId(), 'test_id')
        self.assertEqual(da.title, 'New Title')
        self.assertEqual(da.connection_id, 'conn_2')
        self.assertEqual(da.arguments_src, 'bar baz')
        self.assertEqual(da.src, '<dtml-var baz>\n')
        self.assertEqual(da.max_rows_, 5)
        self.assertEqual(da.max_cache_, 50)
        self.assertEqual(da.cache_time_, 10)
        self.assertEqual(da.class_name_, 'MyRecord')
        self.assertEqual(da.class_file_, 'ZSQLMethods.TestRecord')
        self.assertEqual(da.allow_simple_one_argument_traversal, True)
        self.assertEqual(da.template_class, klass.template_class)
        self.assertEqual(da.connection_hook, 'foo')

    def test_repr(self):
        da = self._makeOne('test_id', 'Test Title', 'conn_id',
                           'foo bar', '<dtml-var bar>')
        self.assertEqual(da.__repr__(), '<DA at test_id>')


DEFAULT_DAV_SOURCE = """\
<dtml-comment>
# vi:syntax=sql
title : Test Title
connection id : conn_id
arguments : foo bar
max_rows : 1000
max_cache : 100
cache_time : 0
class_name : 
class_file : 
connection_hook : 
allow_simple_one_argument_traversal : 
</dtml-comment>
<dtml-var bar>
"""  # NOQA: W291

CHANGED_DAV_SOURCE = """\
<dtml-comment>
# vi:syntax=sql
title : New Title
connection id : conn_2
arguments : bar baz
max_rows : 5
max_cache : 50
cache_time : 10
class_name : MyRecord
class_file : ZSQLMethods.TestRecord
connection_hook : foo
allow_simple_one_argument_traversal : True
</dtml-comment>
<dtml-var baz>
"""
