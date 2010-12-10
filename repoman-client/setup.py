#!/usr/bin/env python

try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages
from distutils.dir_util import mkpath
import os.path

if not os.path.exists('/etc/repoman-client'):
    mkpath('/etc/repoman-client')

setup(name='repoman-client',
    version='0.2.2',
    description='Client to connect to Repoman image repository.',
    author='Kyle Fransham, Drew Harris',
    author_email='fransham@uvic.ca, dbharris@uvic.ca',
    url='http://github.com/hep-gc/repoman',
    install_requires=["simplejson","argparse"],
    packages=['repoman_client'],
    scripts=['scripts/repoman']
)

