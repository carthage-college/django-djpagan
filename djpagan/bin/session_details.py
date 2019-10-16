# -*- coding: utf-8 -*-
import os, sys
# env
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djpagan.settings')

from django.conf import settings

from djpagan.core.sql import SESSION_DETAILS

from djimix.settings.shell import INFORMIX_ODBC_TRAIN
from djimix.core.database import get_connection, xsql

import argparse

DEBUG = settings.INFORMIX_DEBUG

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

    #...........................................
    connection = get_connection(earl=INFORMIX_ODBC_TRAIN)
    # automatically closes the connection after leaving 'with' block
    with connection:
        #...........................................
        print("session details SQL")
        sql = SESSION_DETAILS(
            student_number = sid
        )
        if test:
            print(sql)
        else:
            print("session details data")
            result = xsql(sql, connection, settings.INFORMIX_DEBUG)
            print(result.fetchone())


######################
# shell command line
######################

if __name__ == '__main__':
    args = parser.parse_args()
    sid = args.sid
    test = args.test

    if test:
        print(args)

    sys.exit(main())
