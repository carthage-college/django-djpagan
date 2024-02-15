# -*- coding: utf-8 -*-

"""WSGI configuration."""

import os
import sys


# python
sys.path.append('/d2/python_venv/3.10/djlamantin/lib/python3.10/')
sys.path.append('/d2/python_venv/3.10/djlamantin/lib/python3.10/site-packages/')
# django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djpagan.settings.shell')
os.environ.setdefault('PYTHON_EGG_CACHE', '/var/cache/python/.python-eggs')
os.environ.setdefault('TZ', 'America/Chicago')
# informix
os.environ['INFORMIXSERVER'] = ''
os.environ['DBSERVERNAME'] = ''
os.environ['INFORMIXDIR'] = ''
os.environ['ODBCINI'] = ''
os.environ['ONCONFIG'] = ''
os.environ['INFORMIXSQLHOSTS'] = ''
os.environ['LD_LIBRARY_PATH'] = ''
os.environ['LD_RUN_PATH'] = ''
# wsgi
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
