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

import binascii
import os
import re
from io import StringIO

from Acquisition import Implicit
from App.Common import package_home
from DateTime.DateTime import DateTime
from DocumentTemplate import HTML
from DocumentTemplate import File
from DocumentTemplate.html_quote import html_quote
from OFS.role import RoleManager
from OFS.SimpleItem import Item
from Persistence import Persistent
from zExceptions import Redirect


dtml_dir = os.path.join(package_home(globals()), 'dtml')
InvalidParameter = 'Invalid Parameter'


class BaseQuery(Persistent, Item, Implicit, RoleManager):

    _col = None
    _arg = {}
    query_date = DateTime()
    manage_options = ()
    MissingArgumentError = 'Bad Request'

    def query_year(self):
        return self.query_date.year()

    def query_month(self):
        return self.query_date.month()

    def query_day(self):
        return self.query_date.day()

    def quoted_input(self):
        return quotedHTML(self.input_src)

    def quoted_report(self):
        return quotedHTML(self.report_src)

    def _convert(self):
        self._arg = parse(self.arguments_src)

    def _argdata(self, REQUEST):
        r = {}

        try:
            args = self._arg
        except Exception:
            self._convert()
            args = self._arg

        id = self.id
        missing = []

        for name in args.keys():
            idname = f'{id}/{name}'
            try:
                r[name] = REQUEST[idname]
            except Exception:
                try:
                    r[name] = REQUEST[name]
                except Exception:
                    arg = args[name]
                    try:
                        r[name] = arg['default']
                    except Exception:
                        try:
                            if not arg['optional']:
                                missing.append(name)
                        except Exception:
                            missing.append(name)

        # Note: the code above tries to check if an argument of the
        # ZSQL method above has the "optional" flag set (in case the
        # argument is omitted from the ZSQL function call). But there
        # is neither corresponding code inside the parse() function to
        # check for the "optional" parameter nor any documentation.
        # So we omit the check for the optional parameter. There will
        # be probably no code break but there will be hopefully more code
        # to work as supposed to work.

#        if missing:
#            raise self.MissingArgumentError(  \
#                "The following arguments were omitted " \
#                " from the ZSQL method call: %s" % str(missing))
#

        return r


class Searchable(BaseQuery):

    def _searchable_arguments(self):

        try:
            return self._arg
        except Exception:
            self._convert()
            return self._arg

    def _searchable_result_columns(self):
        return self._col

    def manage_testForm(self, REQUEST):
        """Provide testing interface"""
        input_src = default_input_form(self.title_or_id(),
                                       self._searchable_arguments(),
                                       'manage_test')
        return HTML(input_src)(self, REQUEST)

    def manage_test(self, REQUEST):
        """Perform an actual query"""

        result = self(REQUEST)
        report = HTML(custom_default_report(self.id, result))
        return report(*(self, REQUEST), **{self.id: result})

    def index_html(self, URL1):
        """ """
        raise Redirect('%s/manage_testForm' % URL1)


class Composite:

    def _getquery(self, id):

        o = self
        i = 0
        while 1:
            __traceback_info__ = o
            q = getattr(o, id)
            try:
                if hasattr(q, '_searchable_arguments'):
                    try:
                        q = q.__of__(self.aq_parent)
                    except Exception:
                        pass
                    return q
            except Exception:
                pass
            if i > 100:
                raise AttributeError(id)
            i = i + 1
            o = o.aq_parent

    def myQueryIds(self):
        return map(
            lambda k, queries=self.queries:
            {'id': k, 'selected': k in queries},
            self.ZQueryIds())


def default_input_form(id, arguments, action='query', tabs=''):
    if arguments:
        items = arguments.items()
        return (
            '{}\n{}{}'.format(
                '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN"'
                ' "http://www.w3.org/TR/REC-html40/loose.dtd">\n'
                '<html lang="en"><head><title>%s Input Data</title></head>\n'
                '<body bgcolor="#FFFFFF" link="#000099" vlink="#555555">\n%s\n'
                '<form action="&dtml-URL2;/&dtml-id;/%s" '
                'method="get">\n'
                '<h2>%s Input Data</h2>\n'
                'Enter query parameters:<br>'
                '<table>\n'
                % (id, tabs, action, id),
                '/n'.join(
                    map(
                        lambda a:
                        ('<tr> <th>%s</th>\n'
                         '     <td><input name="%s"\n'
                         '                size="30" value="%s">'
                         '     </td></tr>'
                         % (html_quote(nicify(a[0])),
                            'type' in a[1]
                             and ('{}:{}'.format(a[0], a[1]['type']))
                             or a[0],
                            'default' in a[1] and a[1]['default'] or '')),
                            items)),
                '\n<tr><td colspan=2 align=center>\n'
                '<input type="SUBMIT" name="SUBMIT" value="Submit Query">\n'
                '<dtml-if HTTP_REFERER>\n'
                '  <input type="SUBMIT" name="SUBMIT" value="Cancel">\n'
                '  <INPUT NAME="CANCEL_ACTION" TYPE="HIDDEN"\n'
                '         VALUE="&dtml-HTTP_REFERER;">\n'
                '</dtml-if>\n'
                '</td></tr>\n</table>\n</form>\n</body>\n</html>\n'))
    else:
        return (
            '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN" '
            '"http://www.w3.org/TR/REC-html40/loose.dtd">\n'
            '<html lang="en"><head><title>%s Input Data</title></head>\n'
            '<body bgcolor="#FFFFFF" link="#000099" vlink="#555555">\n%s\n'
            '<form action="&dtml-URL2;/&dtml-id;/%s" '
            'method="get">\n'
            '<h2>%s Input Data</h2>\n'
            'This query requires no input.<p>\n'
            '<input type="SUBMIT" name="SUBMIT" value="Submit Query">\n'
            '<dtml-if HTTP_REFERER>\n'
            '  <input type="SUBMIT" name="SUBMIT" value="Cancel">\n'
            '  <INPUT NAME="CANCEL_ACTION" TYPE="HIDDEN"\n'
            '         VALUE="&dtml-HTTP_REFERER;">\n'
            '</dtml-if>\n'
            '</td></tr>\n</table>\n</form>\n</body>\n</html>\n'
            % (id, tabs, action, id))


custom_default_report_src = File(
    os.path.join(dtml_dir, 'customDefaultReport.dtml'))
custom_default_zpt_report_src = File(
    os.path.join(dtml_dir, 'customDefaultZPTReport.dtml'))


def custom_default_report(id, result, action='', no_table=0,
                          goofy=re.compile(r'\W').search):

    columns = result._searchable_result_columns()
    __traceback_info__ = columns
    heading = ('<tr>\n%s        </tr>' %
               ''.join(
                   map(lambda c:
                       '          <th>%s</th>\n' %
                       html_quote(nicify(c['name'])),
                       columns)))

    if no_table:
        tr, _tr, td, _td, delim = '<p>', '</p>', '', '', ',\n'
    else:
        tr, _tr, td, _td, delim = '<tr>', '</tr>', '<td>', '</td>', '\n'

    row = []
    for c in columns:
        n = c['name']
        if goofy(n) is not None:
            n = 'expr="_[\'%s]"' % (repr('"' + n)[2:])
        row.append('          %s<dtml-var %s%s html_quote>%s'
                   % (td, n, c['type'] != 's' and ' null=""' or '', _td))

    row = ('     {}\n{}\n        {}'.format(
        tr, delim.join(row), _tr))

    return custom_default_report_src(
        id=id, heading=heading, row=row, action=action, no_table=no_table)


def custom_default_zpt_report(id, result, action='', no_table=0,
                              goofy=re.compile(r'\W').search):

    columns = result._searchable_result_columns()
    __traceback_info__ = columns
    heading = ('<tr>\n%s        </tr>' %
               ''.join(
                   map(lambda c:
                       '          <th>%s</th>\n' %
                       html_quote(nicify(c['name'])),
                       columns)))

    if no_table:
        tr, _tr, td, _td, delim = '<p>', '</p>', '', '', ',\n'
    else:
        tr, _tr, td, _td, delim = '<tr>', '</tr>', '<td>', '</td>', '\n'

    row = []
    for c in columns:
        n = c['name']
        tpl = '          %s<span tal:replace="result/%s">%s goes here</span>%s'
        row.append(tpl % (td, n, n, _td))

    row = ('     {}\n{}\n        {}'.format(
        tr, delim.join(row), _tr))

    return custom_default_zpt_report_src(
        id=id, heading=heading, row=row, action=action, no_table=no_table)


def detypify(arg):
    idx = arg.find(':')
    if idx > 0:
        arg = arg[:idx]
    return arg


def decode(input, output):
    while 1:
        line = input.readline()
        if not line:
            break
        s = binascii.a2b_base64(line[:-1])
        output.write(s)


def decodestring(s):
    f = StringIO(s)
    g = StringIO()
    decode(f, g)
    return g.getvalue()


class Args:

    def __init__(self, data=None, keys=None):
        self._data = data or {}
        self._keys = keys or []

    def items(self):
        return map(lambda k, d=self._data: (k, d[k]), self._keys)

    def values(self):
        return map(lambda k, d=self._data: d[k], self._keys)

    def keys(self):
        return list(self._keys)

    def has_key(self, key):
        return key in self._data

    def __contains__(self, key):
        return key in self._data

    def __getitem__(self, key):
        return self._data[key]

    def __setitem__(self, key, v):
        self._data[key] = v

    def __delitem__(self, key):
        del self._data[key]

    def __len__(self):
        return len(self._data)


def parse(text,
          result=None,
          keys=None,
          unparmre=re.compile(
              r'([\000- ]*([^\000- ="]+))'),
          parmre=re.compile(
              r'([\000- ]*([^\000- ="]+)=([^\000- ="]+))'),
          qparmre=re.compile(
              r'([\000- ]*([^\000- ="]+)="([^"]*)")'),
          ):

    if result is None:
        result = {}
        keys = []

    __traceback_info__ = text

    mo = parmre.match(text)

    if mo:
        name = mo.group(2)
        value = {'default': mo.group(3)}
        group_len = len(mo.group(1))

    else:
        mo = qparmre.match(text)

        if mo:
            name = mo.group(2)
            value = {'default': mo.group(3)}
            group_len = len(mo.group(1))

        else:
            mo = unparmre.match(text)

            if mo:
                name = mo.group(2)
                value = {}
                group_len = len(mo.group(1))
            else:
                if not text or not text.strip():
                    return Args(result, keys)
                raise InvalidParameter(text)

    lt = name.find(':')
    if lt > 0:
        value['type'] = name[lt + 1:]
        name = name[:lt]

    result[name] = value
    keys.append(name)

    return parse(text[group_len:], result, keys)


def quotedHTML(text,
               character_entities=(
                   ('&', '&amp;'),
                   ('<', '&lt;'),
                   ('>', '&gt;'),
                   ('"', '&quot;'))):

    for char, name in character_entities:
        text = text.replace(char, name)

    return text


def nicify(name):
    name = name.strip().replace('_', ' ')
    return name[:1].upper() + name[1:]


def decapitate(html, RESPONSE=None,
               header_re=re.compile(
                   r'(('
                   r'[^\000- <>:]+:[^\n]*\n'
                   r'|'
                   r'[ \011]+[^\000- ][^\n]*\n'
                   r')+)[ \t]*\n([\000-\377]+)'),  # please kill me now
               space_re=re.compile(r'([ \t]+)'),
               name_re=re.compile(r'([^\000- <>:]+):([^\n]*)'),
               ):

    mo = header_re.match(html)
    if mo is None:
        return html

    headers, html = mo.group(1, 3)

    headers = headers.split('\n')

    i = 1
    while i < len(headers):
        if not headers[i]:
            del headers[i]
        else:
            mo = space_re.match(headers[i])
            if mo:
                headers[i - 1] = '{} {}'.format(
                    headers[i - 1], headers[i][len(mo.group(1)):])
                del headers[i]
            else:
                i = i + 1

    for i in range(len(headers)):
        mo = name_re.match(headers[i])
        if mo:
            k, v = mo.group(1, 2)
            v = v.strip()
        else:
            raise ValueError('Invalid Header (%d): %s ' % (i, headers[i]))
        RESPONSE.setHeader(k, v)

    return html


def delimited_output(results, REQUEST, RESPONSE):
    delim = REQUEST['output-delimiter']
    try:
        output_type = REQUEST['output-type']
    except Exception:
        output_type = 'text/plain'

    RESPONSE.setHeader('content-type', output_type)
    return '{}\n{}\n'.format(
        delim.join(results.names()),
        '\n'.join(map(lambda row, delim=delim:
                  delim.join(map(str, row)),
                  results)),
    )
