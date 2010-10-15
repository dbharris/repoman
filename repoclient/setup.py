#!/usr/bin/env python

from distutils.core import setup
from distutils.dir_util import mkpath

mkpath('/etc/repoclient')

setup(name='repoclient',
	version='0.1',
	description='Client to connect to VM image repository',
	author='Kyle Fransham',
	author_email='fransham@uvic.ca',
	url='http://github.com/hep-gc/repoman',
	packages=['repoclient'],
	scripts=['repoman'],
	data_files=[('/etc/repoclient/',['conf/repoclient.conf'])]
)
