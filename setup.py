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

version = '3.0.2'

with open('README.rst') as f:
    README = f.read()

with open('CHANGES.rst') as f:
    CHANGES = f.read()

setup(
    name='Products.ZSQLMethods',
    version=version,
    url='https://github.com/zopefoundation/Products.ZSQLMethods',
    license='ZPL 2.1',
    description="SQL method support for Zope.",
    author='Zope Foundation and Contributors',
    author_email='zope-dev@zope.org',
    long_description=(README + '\n' + CHANGES),
    packages=find_packages('src'),
    namespace_packages=['Products', 'Shared', 'Shared.DC'],
    package_dir={'': 'src'},
    classifiers=[
        "Development Status :: 6 - Mature",
        "Environment :: Web Environment",
        "Framework :: Zope2",
        "License :: OSI Approved :: Zope Public License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Database",
        "Topic :: Database :: Front-Ends",
    ],
    install_requires=[
        'setuptools',
        'six',
        'Zope2 >= 4.0a5',
        'RestrictedPython >= 4.0dev',
        'AccessControl >= 4.0dev',
        'Persistence >= 3.0dev',
        'Acquisition',
        'DateTime',
        'DocumentTemplate',
        'ExtensionClass >= 4.1a1',
        'Missing',
        'Record >= 3.4',
        'transaction',
        'zope.interface',
        'zExceptions',
    ],
    include_package_data=True,
    zip_safe=False,
)
