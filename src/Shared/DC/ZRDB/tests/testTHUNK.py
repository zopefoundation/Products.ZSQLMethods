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

from unittest import TestCase
from unittest import TestSuite
from unittest import makeSuite


class TestTM(TestCase):

    def _getTargetClass(self):
        from ..THUNK import THUNKED_TM
        return THUNKED_TM

    def _makeOne(self):
        return self._getTargetClass()()

    def test_conformance(self):
        from transaction.interfaces import IDataManager
        from zope.interface.verify import verifyObject
        tm = self._makeOne()
        verifyObject(IDataManager, tm)

    def test__register(self):
        tm = self._makeOne()
        self.assertFalse(tm._registered)

        tm._register()
        self.assertTrue(tm._registered)

        # Registering again won't break anything
        tm._register()
        self.assertTrue(tm._registered)

    def test_sortKey(self):
        tm = self._makeOne()
        # the default Transaction Manager should have .sortKey() of '1' for
        # backward compatibility. It must be a string according to the
        # ITransactionManager interface.
        self.assertEqual(tm.sortKey(), '1')

        # but the sortKey() should be adjustable
        tm.setSortKey('2')
        self.assertEqual(tm.sortKey(), '2')

        tm.setSortKey([])
        self.assertEqual(tm.sortKey(), '[]')


def test_suite():
    return TestSuite((makeSuite(TestTM),))
