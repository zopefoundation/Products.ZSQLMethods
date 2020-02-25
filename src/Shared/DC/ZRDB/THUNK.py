##############################################################################
#
# Copyright (c) 2002 Zope Foundation and Contributors.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE
#
##############################################################################

import logging

from six.moves._thread import allocate_lock

from transaction.interfaces import IDataManager
from transaction.interfaces import TransactionFailedError
from zope.interface import implementer

from .TM import TM


LOG = logging.getLogger('Products.ZSQLMethods')
thunk_lock = allocate_lock()


@implementer(IDataManager)
class THUNKED_TM(TM):
    """A big heavy hammer for handling non-thread safe DAs
    """

    def _register(self):
        if not self._registered:
            thunk_lock.acquire()

            try:
                self.transaction_manager.get().join(self)
            except TransactionFailedError:
                LOG.error('Failed to join transaction: ', exc_info=True)
                # No need to raise here, the transaction is already
                # broken as a whole
            except ValueError:
                LOG.error('Failed to join transaction: ', exc_info=True)
                # Raising here, the transaction is in an invalid state
                raise
            else:
                self._begin()
                self._registered = 1
            finally:
                thunk_lock.release()

    def tpc_finish(self, *ignored):
        if self._registered:
            try:
                self._finish()
            finally:
                thunk_lock.release()
                self._registered = 0

    def abort(self, *ignored):
        if self._registered:
            try:
                self._abort()
            finally:
                thunk_lock.release()
                self._registered = 0
