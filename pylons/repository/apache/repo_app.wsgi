import site
site.addsitedir('/opt/repo/repository/lib/python2.4/site-packages')

import os, sys
sys.path.append('/opt/repo/repository/repository')
os.environ['PYTHON_EGG_CACHE'] = '/opt/repo/repository/python-eggs'

from paste.deploy import loadapp
application = loadapp('config:/opt/repo/repository/repository/development.ini')

