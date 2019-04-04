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

import pickle
from unittest import TestCase
from unittest import TestSuite
from unittest import makeSuite


class TestArgs(TestCase):

    def _getTargetClass(self):
        from Shared.DC.ZRDB.Aqueduct import Args
        return Args

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_unpickle_old(self):
        # ZSQL Methods created under Zope 2 used an Args class that did not
        # subclass ``object``. Their pickled instances do not load under
        # the newer Args class without code changes.
        old_pickle = (b"(iShared.DC.ZRDB.Aqueduct\nArgs\np0\n(dp1\nS'_data'\n"
                      b"p2\n(dp3\nS'arg1'\np4\n(dp5\nS'default'\np6\nS'n/a'\n"
                      b"p7\nsS'type'\np8\nS'string'\np9\nsssS'_keys'\np10\n"
                      b'(lp11\ng4\nasb.')
        args = pickle.loads(old_pickle)
        self.assertIn('arg1', args)
        self.assertDictEqual(args['arg1'],
                             {'default': 'n/a', 'type': 'string'})

    def test_args_missing(self):
        args = self._makeOne()
        self.assertEqual(len(args), 0)
        self.assertEqual(list(args.items()), [])

    def test_args_invalid(self):
        args = self._makeOne('foo')
        self.assertEqual(list(args.items()), [])

    def test_args_correct(self):
        args = self._makeOne({'arg1': {'type': 'string'}}, ['arg1'])
        self.assertEqual(len(args), 1)

    def test_dict_getters(self):
        args = self._makeOne({'arg1': {'type': 'string', 'default': 'n/a'}},
                             ['arg1'])
        self.assertIn('arg1', args)
        self.assertTrue(args.has_key('arg1'))  # NOQA: flake8: W601
        self.assertDictEqual(args['arg1'],
                             {'default': 'n/a', 'type': 'string'})
        self.assertEqual(args.keys(), ['arg1'])
        self.assertEqual(list(args.values()),
                         [{'type': 'string', 'default': 'n/a'}])
        self.assertEqual(list(args.items()),
                         [('arg1', {'default': 'n/a', 'type': 'string'})])

    def test__setitem__(self):
        args = self._makeOne()
        args['arg2'] = {'type': 'int'}
        self.assertEqual(len(args), 1)
        self.assertIn('arg2', args)
        self.assertDictEqual(args['arg2'], {'type': 'int'})

    def test__delitem__(self):
        args = self._makeOne()
        args['arg2'] = {'type': 'int'}
        self.assertEqual(len(args), 1)

        self.assertRaises(KeyError, args.__delitem__, 'unknown')

        del args['arg2']
        self.assertEqual(len(args), 0)


def test_suite():
    return TestSuite((makeSuite(TestArgs),))
