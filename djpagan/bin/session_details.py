# -*- coding: utf-8 -*-
import os, sys
# env
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djpagan.settings')

from django.conf import settings

from djpagan.fee.sql import ORDERED_TERMS_TEMP
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
        print(settings.ORDERED_TERMS_START_DATE)
        sql = SESSION_DETAILS(
            student_number = sid, start_date = settings.ORDERED_TERMS_START_DATE
        )
        #sql = 'select * from ordered_terms'
        sql = '''
SELECT
    stu_acad_rec.id, stu_acad_rec.sess, stu_acad_rec.yr, stu_acad_rec.prog,
    stu_acad_rec.subprog,
    ordered_terms.latest,
    stu_acad_rec.cl, stu_acad_rec.reg_stat, stu_acad_rec.reg_hrs,
    stu_acad_rec.acst, stu_acad_rec.fin_clr,
    stu_serv_rec.rsv_stat, stu_serv_rec.offcampus_res_appr,
    stu_serv_rec.intend_hsg, stu_serv_rec.bldg, stu_serv_rec.room,
    stu_serv_rec.suite, stu_serv_rec.bill_code, stu_serv_rec.spec_flag,
    stu_serv_rec.hlth_ins_wvd, stu_serv_rec.meal_plan_type,
    stu_serv_rec.meal_plan_wvd, stu_serv_rec.res_asst, stu_serv_rec.stat,
    stu_serv_rec.park_prmt_no, stu_serv_rec.park_prmt_exp_date,
    stu_serv_rec.park_location, stu_serv_rec.lot_no
FROM
    stu_acad_rec
LEFT JOIN
    stu_serv_rec
ON (
    stu_acad_rec.id = stu_serv_rec.id
    AND
    stu_acad_rec.yr = stu_serv_rec.yr
    AND
    stu_acad_rec.sess = stu_serv_rec.sess
)
, (
    SELECT
        CAST( rank() over (order by end_date) AS CHAR(12)) as latest,
        prog, yr, sess, subsess, acyr, beg_date, end_date
    FROM
        acad_cal_rec
    WHERE
        beg_date >  MDY(1,1,2010)
    AND
        end_date < CURRENT
    AND
        subsess = ""
) ordered_terms
WHERE
    stu_acad_rec.id = 1458533
AND
    stu_acad_rec.yr = ordered_terms.yr
AND
    stu_acad_rec.sess = ordered_terms.sess
AND
    stu_acad_rec.prog = ordered_terms.prog
ORDER BY
    ordered_terms.latest desc;
        '''
        #sql='select * from cc_djpagan__student_detail'

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
