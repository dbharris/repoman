# This file defines the application variable for mod-wsgi to load.
# Replace @@VIRTUAL_ENV@@ with the fullpath to your virtual environment

import site
site.addsitedir('@@VIRTUAL_ENV@@/lib/python2.4/site-packages')

import os, sys
sys.path.append('@@VIRTUAL_ENV@@/repoman/server/repoman')
os.environ['PYTHON_EGG_CACHE'] = '@@VIRTUAL_ENV@@/python-eggs'

from paste.deploy import loadapp
application = loadapp('config:@@VIRTUAL_ENV@@/repoman/server/repoman/development.ini')

