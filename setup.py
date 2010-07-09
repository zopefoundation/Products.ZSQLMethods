##############################################################################
#
# Copyright (c) 2010 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################

from setuptools import setup, find_packages

setup(name='Products.ZSQLMethods',
      version = '2.13.0',
      url='http://pypi.python.org/pypi/Products.ZSQLMethods',
      license='ZPL 2.1',
      description="SQL method support for Zope 2.",
      author='Zope Foundation and Contributors',
      author_email='zope-dev@zope.org',
      long_description=open('README.txt').read() + '\n' +
                       open('CHANGES.txt').read(),
      packages=find_packages('src'),
      namespace_packages=['Products', 'Shared', 'Shared.DC'],
      package_dir={'': 'src'},
      install_requires=[
        'setuptools',
        'AccessControl',
        'Acquisition',
        'DateTime',
        'DocumentTemplate',
        'ExtensionClass',
        'Missing',
        'Persistence',
        'Record',
        'transaction',
        'zExceptions',
        'ZODB3',
        'zope.interface',
        'Zope2 >= 2.13.0a1',
      ],
      include_package_data=True,
      zip_safe=False,
      )
