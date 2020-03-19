##############################################################################
#
# Copyright (c) 2005 Zope Foundation and Contributors.
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

from six.moves import UserDict


def _sql_quote(v):
    return '"%s"' % v


class FauxMultiDict(UserDict):

    def getitem(self, key, call):
        if key == 'sql_quote__':
            return _sql_quote

        v = self[key]
        if v is not None:
            if call and callable(v):
                v = v()
        return v


class SQLTestTests(unittest.TestCase):

    def _getTargetClass(self):
        from Shared.DC.ZRDB.sqltest import SQLTest
        return SQLTest

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_string(self):
        tested = self._makeOne('foo type="string"')
        self.assertEqual(tested.render(FauxMultiDict(foo='FOO')),
                         'foo = "FOO"')

    def test_string_binary(self):
        tested = self._makeOne('foo type="string"')
        self.assertEqual(tested.render(FauxMultiDict(foo=b'FOO')),
                         'foo = "FOO"')

    def test_int(self):
        tested = self._makeOne('foo type="int"')

        for valid in (100, 100.00, '100', b'100'):
            self.assertEqual(tested.render(FauxMultiDict(foo=valid)),
                             'foo = 100')

        for invalid in ('', b'', None):
            self.assertRaises(ValueError,
                              tested.render,
                              FauxMultiDict(foo=invalid))

    def test_float(self):
        tested = self._makeOne('foo type="float"')

        for valid in (100, 100.0, '100.0', b'100.0'):
            self.assertEqual(tested.render(FauxMultiDict(foo=valid)),
                             'foo = 100.0')

        for invalid in ('', b'', None):
            self.assertRaises(ValueError,
                              tested.render,
                              FauxMultiDict(foo=invalid))


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(SQLTestTests))
    return suite
