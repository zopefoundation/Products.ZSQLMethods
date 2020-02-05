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


class ConnectionTests(unittest.TestCase):

    def _getTargetClass(self):
        from Shared.DC.ZRDB.Connection import Connection
        return Connection

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_connect_on_load(self):

        class _Connection(self._getTargetClass()):

            def connect(self, connection_string):
                setattr(self, '_connected_to', connection_string)

        conn1 = _Connection('conn1', '', 'conn string 1')
        conn1.__setstate__(None)
        self.assertEqual(conn1._connected_to, 'conn string 1')

        conn2 = _Connection('conn2', '', 'conn string 2')
        conn2.connect_on_load = False
        conn2.__setstate__(None)
        self.assertFalse(hasattr(conn2, '_connected_to'))

    def test_sql_quote___miss(self):
        TO_QUOTE = 'no quoting required'
        conn = self._makeOne('conn', '', 'conn string')
        self.assertEqual(conn.sql_quote__(TO_QUOTE), "'%s'" % TO_QUOTE)

    def test_sql_quote___embedded_apostrophe(self):
        TO_QUOTE = "w'embedded apostrophe"
        conn = self._makeOne('conn', '', 'conn string')
        self.assertEqual(conn.sql_quote__(TO_QUOTE),
                         "'w''embedded apostrophe'")

    def test_sql_quote___embedded_backslash(self):
        TO_QUOTE = 'embedded \\backslash'
        conn = self._makeOne('conn', '', 'conn string')
        self.assertEqual(conn.sql_quote__(TO_QUOTE),
                         "'embedded \\backslash'")
        # Show for good measure that the seeming two backslashes
        # are really one, when you look at the raw string.
        self.assertEqual(conn.sql_quote__(TO_QUOTE),
                         r"'embedded \backslash'")

    def test_sql_quote___embedded_double_quote(self):
        # As it turns out, escaping double quotes will break
        # some servers, notably PostgreSQL, so we no longer do that.
        TO_QUOTE = 'embedded "double quote'
        conn = self._makeOne('conn', '', 'conn string')
        self.assertEqual(conn.sql_quote__(TO_QUOTE),
                         "'embedded \"double quote'")

    def test_sql_quote___embedded_null(self):
        TO_QUOTE = "w'embedded apostrophe and \x00null"
        conn = self._makeOne('conn', '', 'conn string')
        self.assertEqual(conn.sql_quote__(TO_QUOTE),
                         "'w''embedded apostrophe and null'")

        # This is another version of a nul character.
        TO_QUOTE = 'embedded other \x1anull'
        conn = self._makeOne('conn', '', 'conn string')
        self.assertEqual(conn.sql_quote__(TO_QUOTE),
                         "'embedded other null'")

    def test_sql_quote___embedded_carriage_return(self):
        TO_QUOTE = "w'embedded carriage\rreturn"
        conn = self._makeOne('conn', '', 'conn string')
        self.assertEqual(conn.sql_quote__(TO_QUOTE),
                         "'w''embedded carriagereturn'")


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(ConnectionTests))
    return suite
