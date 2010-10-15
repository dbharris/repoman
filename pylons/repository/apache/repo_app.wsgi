import site
site.addsitedir('/opt/mvliet/repoman/lib/python2.4/site-packages')

import os, sys
sys.path.append('/opt/mvliet/repoman/repoman/pylons/repository')
os.environ['PYTHON_EGG_CACHE'] = '/opt/mvliet/repoman/python-eggs'

from paste.deploy import loadapp
application = loadapp('config:/opt/mvliet/repoman/repoman/pylons/repository/development.ini')

