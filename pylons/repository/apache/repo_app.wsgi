import site
site.addsitedir('/opt/git/repoman/lib/python2.4/site-packages')

import os, sys
sys.path.append('/opt/git/repoman/repoman/pylons/repository')
os.environ['PYTHON_EGG_CACHE'] = '/opt/git/repoman/python-eggs'

from paste.deploy import loadapp
application = loadapp('config:/opt/git/repoman/repoman/pylons/repository/development.ini')

