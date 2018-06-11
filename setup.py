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

version = '3.0.3'

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
        "Framework :: Zope :: 4",
        "License :: OSI Approved :: Zope Public License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Database",
        "Topic :: Database :: Front-Ends",
    ],
    install_requires=[
        'setuptools',
        'six',
        'Zope >= 4.0b5',
        'Missing',
        'Record',
    ],
    include_package_data=True,
    zip_safe=False,
)
