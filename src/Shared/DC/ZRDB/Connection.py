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
"""Generic Database Connection Support"""

try:
    from html import escape # noqa
except ImportError:  # Python 2
    from cgi import escape  # noqa
import sys
from logging import getLogger

from six import StringIO

from AccessControl.class_init import InitializeClass
from AccessControl.Permissions import change_database_connections
from AccessControl.Permissions import open_close_database_connection
from AccessControl.Permissions import test_database_connections
from AccessControl.Permissions import view_management_screens
from AccessControl.SecurityInfo import ClassSecurityInfo
from Acquisition import Implicit
from App.Dialogs import MessageDialog
from App.special_dtml import DTMLFile
from DateTime.DateTime import DateTime
from DocumentTemplate import HTML
from DocumentTemplate.DT_Var import sql_quote
from OFS.role import RoleManager
from OFS.SimpleItem import Item
from Persistence import Persistent
from zExceptions import BadRequest

from . import RDB
from .Aqueduct import custom_default_report
from .Results import Results


LOG = getLogger('ZRDB.Connection')


class Connection(Persistent, RoleManager, Item, Implicit):

    security = ClassSecurityInfo()

    # Specify definitions for tabs:
    manage_options = (({'label': 'Status', 'action': 'manage_main'},
                       {'label': 'Properties', 'action': 'manage_properties'},
                       {'label': 'Test', 'action': 'manage_testForm'})
                      + RoleManager.manage_options + Item.manage_options)

    _v_connected = ''
    connection_string = ''
    # Should the database connection be established when the object
    # is loaded from the ZODB (in __setstate__)?
    connect_on_load = True

    def __init__(self, id, title, connection_string, check=None):
        self.id = str(id)
        self.edit(title, connection_string, check)

    def __setstate__(self, state):
        Persistent.__setstate__(self, state)
        if self.connect_on_load and self.connection_string:
            try:
                self.connect(self.connection_string)
            except Exception:
                LOG.error('Error connecting to relational database.',
                          exc_info=True)

    def title_and_id(self):
        s = Connection.inheritedAttribute('title_and_id')(self)
        if hasattr(self, '_v_connected') and self._v_connected:
            s = '%s, which is connected' % s
        else:
            s = '%s, which is <font color=red>not connected</font>' % s
        return s

    def title_or_id(self):
        s = Connection.inheritedAttribute('title_or_id')(self)
        if hasattr(self, '_v_connected') and self._v_connected:
            s = '%s (connected)' % s
        else:
            s = '%s (<font color=red>not connected</font>)' % s
        return s

    def connected(self):
        return self._v_connected

    def edit(self, title, connection_string, check=1):
        self.title = title
        self.connection_string = connection_string
        if check:
            self.connect(connection_string)

    manage_properties = DTMLFile('dtml/connectionEdit', globals())

    @security.protected(change_database_connections)
    def manage_edit(self, title, connection_string, check=None, REQUEST=None):
        """Change connection
        """
        self.edit(title, connection_string, check)
        if REQUEST is not None:
            esc_id = escape(self.id)
            return MessageDialog(
                title='Edited',
                message='<strong>%s</strong> has been edited.' % esc_id,
                action='./manage_main')

    security.declareProtected(test_database_connections,  # NOQA: D001
                              'manage_testForm')
    manage_testForm = DTMLFile('dtml/connectionTestForm', globals())

    @security.protected(test_database_connections)
    def manage_test(self, query, REQUEST=None):
        """Executes the SQL in parameter 'query' and returns results"""
        dbc = self()  # get our connection
        res = dbc.query(query)

        if isinstance(res, type('')):
            f = StringIO()
            f.write(res)
            f.seek(0)
            result = RDB.File(f)
        else:
            result = Results(res)

        if REQUEST is None:
            return result  # return unadulterated result objects

        if result._searchable_result_columns():
            r = custom_default_report(self.id, result)
        else:
            r = 'This statement returned no results.'

        report = HTML(
            '<html><body bgcolor="#ffffff" link="#000099" vlink="#555555">\n'
            '<dtml-var name="manage_tabs">\n<hr>\n%s\n\n'
            '<hr><h4>SQL Used:</strong><br>\n<pre>\n%s\n</pre>\n<hr>\n'
            '</body></html>'
            % (r, query))

        report = report(*(self, REQUEST), **{self.id: result})

        return report

    security.declareProtected(view_management_screens,  # NOQA: D001
                              'manage_main')
    manage_main = DTMLFile('dtml/connectionStatus', globals())

    @security.protected(open_close_database_connection)
    def manage_close_connection(self, REQUEST=None):
        """Close the connection from the ZMI"""
        msg = ''
        try:
            if hasattr(self, '_v_database_connection'):
                self._v_database_connection.close()
        except Exception as exc:
            LOG.error('Error closing relational database connection.',
                      exc_info=True)
            msg = str(exc)
        self._v_connected = ''
        if REQUEST is not None:
            return self.manage_main(self, REQUEST, manage_tabs_message=msg)

    @security.protected(open_close_database_connection)
    def manage_open_connection(self, REQUEST=None):
        """Open the connection from the ZMI"""
        msg = ''
        try:
            self.connect(self.connection_string)
        except Exception as exc:
            LOG.error('Error opening relational database connection.',
                      exc_info=True)
            msg = str(exc)
        if REQUEST is not None:
            return self.manage_main(self, REQUEST, manage_tabs_message=msg)

    def __call__(self, v=None):
        try:
            return self._v_database_connection
        except AttributeError:
            s = self.connection_string
            if s:
                self.connect(s)
                return self._v_database_connection
            raise BadRequest('The database connection is not connected')

    def connect(self, s):
        self.manage_close_connection()
        DB = self.factory()
        try:
            try:
                self._v_database_connection = DB(s)
            except Exception:
                t, v, tb = sys.exc_info()
                raise BadRequest(
                    '<strong>Error connecting to DB.</strong><br>\n'
                    '<!--\n%s\n%s\n-->\n' % (t, v)).with_traceback(tb)
        finally:
            tb = None
        self._v_connected = DateTime()

        return self

    def sql_quote__(self, v):
        v = sql_quote(v)
        return "'%s'" % v


InitializeClass(Connection)
