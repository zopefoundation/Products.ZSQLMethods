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

from AccessControl.SecurityManagement import newSecurityManager
from AccessControl.SecurityManagement import noSecurityManager
from AccessControl.users import system
from OFS.Folder import Folder
from Products.ZSQLMethods.SQL import manage_addZSQLMethod


QUERY = """\
SELECT *
FROM users
WHERE <dtml-sqltest user_id type="string">"""


class TestSearch(unittest.TestCase):

    def setUp(self):
        from ..Connection import Connection

        newSecurityManager(None, system)
        self.root = Folder('testing')
        self.root._setObject('testconn',
                             Connection('testconn', '', 'conn_string'))
        for x in ('1', '2', '3'):
            zsql_id = 'zsql_%s' % x
            manage_addZSQLMethod(self.root, zsql_id, '', 'testconn',
                                 'user_id', QUERY)
            # Initialize variables
            zsql_meth = getattr(self.root, zsql_id)
            zsql_meth.manage_edit('', 'testconn', 'user_id', QUERY)
            zsql_meth._col = ({'name': 'user_id', 'type': 'string'},)

    def tearDown(self):
        noSecurityManager()

    def test_dtml_interface(self):
        from ..Search import manage_addZSearch

        manage_addZSearch(self.root,
                          'report1',
                          'Report 1',
                          '0',
                          'search1',
                          'Search 1',
                          'dtml_methods',
                          queries=['zsql_1', 'zsql_2', 'zsql_3'])

        self.assertEqual(set(self.root.objectIds(['DTML Method'])),
                         {'report1', 'search1'})

    def test_zpt_interface(self):
        from ..Search import manage_addZSearch

        manage_addZSearch(self.root,
                          'report1',
                          'Report 1',
                          '0',
                          'search1',
                          'Search 1',
                          'page_templates',
                          queries=['zsql_1', 'zsql_2', 'zsql_3'])

        self.assertEqual(set(self.root.objectIds(['Page Template'])),
                         {'report1', 'search1'})
