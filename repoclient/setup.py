#!/usr/bin/env python

try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages
from distutils.dir_util import mkpath
import os.path

if not os.path.exists('/etc/repoclient'):
    mkpath('/etc/repoclient')

setup(name='repoclient',
    version='0.1.1',
    description='Client to connect to Repoman image repository.',
    author='Kyle Fransham, Drew Harris',
    author_email='fransham@uvic.ca, dbharris@uvic.ca',
    url='http://github.com/hep-gc/repoman',
    install_requires=["simplejson"],
    packages=['repoclient'],
    scripts=['scripts/repoclient'],
    data_files=[('/etc/repoclient/',['repoclient/repoclient.conf'])]
)

