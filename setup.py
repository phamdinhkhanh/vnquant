# -*- coding: utf-8 -*-
"""
Created on Mon Nov 12 00:23:29 2018

@author: khanhphamdinh
"""

from setuptools import setup, find_packages

try:
    from pypandoc import convert
    read_md = lambda f: convert(f, 'rst')
except ImportError:
    print("warning: pypandoc module not found, could not convert Markdown to RST")
    read_md = lambda f: open(f, 'r').read()

DISTNAME = 'VNDS'
INSTALL_REQUIRES = (
    ['pandas>=0.19.2', 'requests>=2.3.0', 'wrapt>=1.10.0', 'lxml']
)

VERSION = '0.0.1'
LICENSE = 'MIT'
DESCRIPTION = 'VietNam stock market'
AUTHOR = "KhanhPhamDinh"
EMAIL = "phamdinhkhanh.tkt53.neu@gmail.com"
URL = "https://github.com/phamdinhkhanh/FirstPackagePython"
DOWNLOAD_URL = 'https://github.com/phamdinhkhanh/FirstPackagePython'

setup(name=DISTNAME,
      version=VERSION,
      description=DESCRIPTION,
      author=AUTHOR,
      author_email=EMAIL,
      url=URL,
      license = LICENSE,
      #package name are looked in python path
      packages=find_packages(exclude = ['contrib', 'docs', 'tests*']),
      #root directory
      # package_dir = {'':'src'},
      # package_data={'mypack': ['template/*.txt', 'template/*.rst']},
      #Looking for modules file
      # py_modules = ['Birds', 'Mammals'],
      classifiers=[
        'Development Status :: 0 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Trader/Investor/Science/Research',
        'Operating System :: OS Independent',
        'Programming Language :: Cython',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Financial/Stock Market',
      ],

      keywords = 'data',
      # long_description = read_md('READM.md'),
      install_requires=INSTALL_REQUIRES,
      test_suite='tests',
      zip_safe=False,
     )
