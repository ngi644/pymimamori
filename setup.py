# encoding: utf-8

"""
Created by nagai at 15/04/21
"""

__author__ = 'nagai'

from setuptools import setup, find_packages


setup(
    name='mimamori',
    description='Mimamori',
    author='Takashi Nagai',
    author_email='ngi644@gmail.com',
    url='',
    version='0.1.0',
    license='AGPL-3.0',
    keywords=['ble',],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'gattlib',
        'datadog',
        'docopt'
    ],
    classifiers=[
        # https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Education',
        'Topic :: Internet :: WWW/HTTP',
    ],
)
