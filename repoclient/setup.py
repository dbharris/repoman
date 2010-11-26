#!/usr/bin/env python

from distutils.core import setup
from distutils.dir_util import mkpath
import sys
import os
import os.path

path = os.getenv("HOME") + '/.repoman/'

if not os.path.exists(path):
    os.makedirs(path)


if os.path.isfile(path + 'repoclient.conf'):
    print os.getenv("HOME") + '/.repoman/repoclient.conf already exists.'
    print "Using this configuration - if you wish to use the default please move this file."
    setup(name='repoclient',
        version='0.1',
        description='Client to connect to VM image repository',
        author='Kyle Fransham, Drew Harris',
        author_email='fransham@uvic.ca, dbharris@uvic.ca',
        url='http://github.com/hep-gc/repoman',
        packages=['repoclient'],
        scripts=['repoman'],
    )
else:
    setup(name='repoclient',
        version='0.1',
        description='Client to connect to VM image repository',
        author='Kyle Fransham, Drew Harris',
        author_email='fransham@uvic.ca, dbharris@uvic.ca',
        url='http://github.com/hep-gc/repoman',
        packages=['repoclient'],
        scripts=['repoman'],
        data_files=[(path,['conf/repoclient.conf'])]
    )
