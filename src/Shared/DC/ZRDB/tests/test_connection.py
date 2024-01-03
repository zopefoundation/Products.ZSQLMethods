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
from zExceptions import BadRequest


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

    def test_connect_error(self):
        # It raises a BadRequest exception. This is a regression test for
        # https://github.com/zopefoundation/Products.ZSQLMethods/issues/41

        class FakeFactory:

            def __call__(self, s):
                raise RuntimeError

        conn = self._makeOne('conn1', '', 'conn string 1')
        conn.factory = FakeFactory
        with self.assertRaises(BadRequest) as err:
            conn.connect('conn1')
        self.assertTrue(str(err.exception).startswith(
            '<strong>Error connecting to DB.'))

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

    def _makeDbFactory(self):
        class FakeDB:
            def query(self, sql):
                return """\
                foo<mark3r>foo2\tbar
                2i\tt
                1\ta<xyz>b
                3\t7<15\
                """

        class FakeFactory:
            def __call__(self, s):
                return FakeDB()
        return FakeFactory

    def test_manage_test_html_quote(self):
        # test the Connection.manage_test() method for html quoting

        conn = self._makeOne('conn', '', 'conn string')
        conn = makerequest(conn)

        conn.factory = self._makeDbFactory()

        # do not render management screen
        conn.manage_tabs = ''

        # we need a REQUEST arg to do the rendering
        report = conn.manage_test('select<m4rker>', REQUEST={})

        # check html quoting in result table header
        idx = report.find('mark3r')
        idx0 = report.rfind('<th>', 0, idx)
        idx1 = report.find('</th>', idx) + 5

        th_expected = '<th>foo&lt;mark3r&gt;foo2</th>'
        self.assertEqual(report[idx0:idx1].lower(), th_expected)

        # check html quoting in result table data
        idx = report.find('xyz')
        idx0 = report.rfind('<td>', 0, idx)
        idx1 = report.find('</td>', idx) + 5

        td_expected = '<td>a&lt;xyz&gt;b</td>'
        self.assertEqual(report[idx0:idx1], td_expected)

        # check html quoting in "sql used:"
        idx = report.find('m4rker')
        idx0 = report.rfind('<pre>', 0, idx)
        idx1 = report.find('</pre>', idx) + 6

        pre_expected = '<pre>\nselect&lt;m4rker&gt;\n</pre>'
        self.assertEqual(report[idx0:idx1], pre_expected)


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(
        unittest.defaultTestLoader.loadTestsFromTestCase(ConnectionTests))
    return suite
