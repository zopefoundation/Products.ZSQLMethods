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

__version__ = '3.0.0.dev0'

with open('README.rst') as f:
    README = f.read()

with open('CHANGES.rst') as f:
    CHANGES = f.read()

setup(
    name='Products.ZSQLMethods',
    version=__version__,
    url='http://pypi.python.org/pypi/Products.ZSQLMethods',
    license='ZPL 2.1',
    description="SQL method support for Zope 2.",
    author='Zope Foundation and Contributors',
    author_email='zope-dev@zope.org',
    long_description=(README + '\n' + CHANGES),
    packages=find_packages('src'),
    namespace_packages=['Products', 'Shared', 'Shared.DC'],
    package_dir={'': 'src'},
    install_requires=[
        'setuptools',
        'six',
        'Zope2 >= 4.0dev',
        'RestrictedPython >= 4.0dev',
        'AccessControl >= 4.0dev',
        'Persistence >= 3.0dev',
        'Acquisition',
        'DateTime',
        'DocumentTemplate',
        'ExtensionClass >= 4.1a1',
        'Missing',
        'Record',
        'transaction',
        'zope.interface',
        'zExceptions',
    ],
    include_package_data=True,
    zip_safe=False,
)
