# -*- coding: utf-8 -*-
import os, sys
# env
sys.path.append('/usr/lib/python2.7/dist-packages/')
sys.path.append('/usr/lib/python2.7/')
sys.path.append('/usr/local/lib/python2.7/dist-packages/')
sys.path.append('/data2/django_1.11/')
sys.path.append('/data2/django_projects/')
sys.path.append('/data2/django_third/')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djpagan.settings')

# required if using django models
import django
django.setup()

from django.conf import settings

from djpagan.billing.sql import ALL_TRANSACTIONS

import argparse
import logging
import pyodbc

logger = logging.getLogger('djpagan')

DEBUG = settings.INFORMIX_DEBUG

'''
Shell script...
'''

# set up command-line options
desc = """
Accepts as input...
"""

# RawTextHelpFormatter method allows for new lines in help text
parser = argparse.ArgumentParser(
    description=desc, formatter_class=argparse.RawTextHelpFormatter
)

parser.add_argument(
    '-i', '--id',
    required=True,
    help="Student ID",
    dest='cid'
)
parser.add_argument(
    '--test',
    action='store_true',
    help="Dry run?",
    dest='test'
)

def main():
    '''
    main function
    '''

    sql = ALL_TRANSACTIONS(
        student_id = cid,
        stat = ''
    )

    if test:
        print sql

    cnxn = pyodbc.connect(settings.INFORMIX_ODBC)
    cursor = cnxn.cursor()
    cursor.execute(sql)
    objects = cursor.fetchall()

    for o in objects:
        print o.user_name
        #print o['stat']
        #print o.SUBE_Stat
        print o[15]

    if test:
        print 'this is a test'
        logger.debug("debug = {}".format(test))
    else:
        print 'this is not a test'


######################
# shell command line
######################

if __name__ == '__main__':
    args = parser.parse_args()
    cid = args.cid
    test = args.test

    if test:
        print args

    sys.exit(main())

