#!/usr/bin/env python

from distutils.core import setup
from distutils.dir_util import mkpath
import os.path

if not os.path.exists('/etc/repoclient'):
    mkpath('/etc/repoclient')

setup(name='repoclient',
    version='0.1b3',
    description='Client to connect to VM image repository',
    author='Kyle Fransham, Drew Harris',
    author_email='fransham@uvic.ca, dbharris@uvic.ca',
    url='http://github.com/hep-gc/repoman',
    packages=['repoclient'],
    scripts=['repoman'],
    data_files=[('/etc/repoclient/',['conf/repoclient.conf'])]
)

