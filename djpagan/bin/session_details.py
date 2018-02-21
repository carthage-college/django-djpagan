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

from django.conf import settings

from djpagan.core.sql import ORDERED_TERMS_TEMP, SESSION_DETAILS

from djzbar.utils.informix import get_session

import argparse

DEBUG = settings.INFORMIX_DEBUG
EARL = settings.INFORMIX_EARL

'''
test the session detail data retrieval infrastructure
'''

# set up command-line options
desc = """
Accepts as input a student ID
"""

# RawTextHelpFormatter method allows for new lines in help text
parser = argparse.ArgumentParser(
    description=desc, formatter_class=argparse.RawTextHelpFormatter
)

parser.add_argument(
    '-i', '--id',
    required=True,
    help="Student ID",
    dest='sid'
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

    session = get_session(EARL)
    #...........................................
    #print "drop temp table, just in case"
    sql = "DROP TABLE ordered_terms"
    try:
        session.execute(sql)
        print "ordered_terms table dropped"
    except:
        print "ordered_terms table not found"

    sql = ORDERED_TERMS_TEMP
    if test:
        print sql
    else:
        session.execute(sql)

    #...........................................
    print "session details SQL"

    sql = SESSION_DETAILS(
        student_number = sid,
    )

    if test:
        print sql
    else:
        details = session.execute(sql).first()
        print details

    session.close()

######################
# shell command line
######################

if __name__ == '__main__':
    args = parser.parse_args()
    sid = args.sid
    test = args.test

    if test:
        print args

    sys.exit(main())

