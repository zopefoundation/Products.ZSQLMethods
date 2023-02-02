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

from setuptools import find_packages
from setuptools import setup


with open('README.rst') as f:
    README = f.read()

with open('CHANGES.rst') as f:
    CHANGES = f.read()

setup(
    name='Products.ZSQLMethods',
    version='4.0',
    url='https://github.com/zopefoundation/Products.ZSQLMethods',
    project_urls={
        'Issue Tracker': ('https://github.com/zopefoundation'
                          '/Products.ZSQLMethods/issues'),
        'Sources': 'https://github.com/zopefoundation/Products.ZSQLMethods',
    },
    license='ZPL 2.1',
    description='SQL method support for Zope.',
    author='Zope Foundation and Contributors',
    author_email='zope-dev@zope.dev',
    long_description=(README + '\n' + CHANGES),
    packages=find_packages('src'),
    namespace_packages=['Products', 'Shared', 'Shared.DC'],
    package_dir={'': 'src'},
    classifiers=[
        'Development Status :: 6 - Mature',
        'Environment :: Web Environment',
        'Framework :: Zope',
        'Framework :: Zope :: 5',
        'License :: OSI Approved :: Zope Public License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Database',
        'Topic :: Database :: Front-Ends',
    ],
    python_requires='>=3.7',
    install_requires=[
        'setuptools',
        'Zope >= 4.2.1',
        'Missing',
        'Record',
        'DocumentTemplate >= 3.2.2',
    ],
    include_package_data=True,
    zip_safe=False,
)
