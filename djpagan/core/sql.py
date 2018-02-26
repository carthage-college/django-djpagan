from django.conf import settings


PROGRAM_ENROLLMENT = '''
SELECT
    id_rec.id, trim(firstname) as firstname, trim(lastname) as lastname,
    prog, subprog, major1, major2, major3, nurs_prog, cl, cohort_yr,
    cohort_ctgry, acst, plan_grad_yr, plan_grad_sess, deg, tle
FROM
    id_rec, prog_enr_rec
WHERE
    id_rec.id = prog_enr_rec.id
AND
    id_rec.id = {student_number}
'''.format

SUBSIDIARY_BALANCES = '''
SELECT
    id, subs, bal_act, def_pmt_terms, stat, ent_no, cr_rating, descr,
    dunning_letter, interest_wvd, written_off, collect_agc,
    ccresrc as payment_group
FROM
    suba_rec
WHERE
    id = {student_number}
'''.format

ACCOUNT_NOTES = '''
SELECT
    suba_rec.subs, suba_rec.id, suba_blob.comm
FROM
    suba_blob, suba_rec
WHERE
    suba_blob.bsuba_no = suba_rec.bsuba_no
AND
    suba_blob.comm is not null
AND
    suba_rec.id = {student_number}
'''.format

ORDERED_TERMS_TEMP = '''
SELECT
    rank() over (order by end_date) as latest,
    prog, yr, sess, subsess, acyr, beg_date, end_date
FROM
    acad_cal_rec
WHERE
    beg_date >  "{}"
AND
    end_date < CURRENT
AND
    subsess = ""
ORDER BY
    end_date DESC
INTO TEMP
    ordered_terms
'''.format(settings.ORDERED_TERMS_START_DATE)

SESSION_DETAILS = '''
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
, ordered_terms
WHERE
    1 = 1
AND
    stu_acad_rec.yr = ordered_terms.yr
AND
    stu_acad_rec.sess = ordered_terms.sess
AND
    stu_acad_rec.prog = ordered_terms.prog
AND
    stu_acad_rec.id = {student_number}
ORDER BY
    ordered_terms.latest desc;
'''.format

SEARCH_STUDENTS = '''
SELECT
     id_rec.id, trim(firstname) as firstname, trim(lastname) as lastname,
     prog, subprog, cl, nurs_prog, cohort_yr,
     acst, bal_act as SA_balance, descr, dunning_letter, interest_wvd
FROM
     prog_enr_rec, id_rec
LEFT JOIN
    suba_rec
ON
    id_rec.id = suba_rec.id
    AND
    suba_rec.subs= "S/A"
WHERE
    id_rec.id = prog_enr_rec.id
AND
    LOWER(lastname) = TRIM(LOWER("{lastname}"))
AND
    prog_enr_rec.acst = "GOOD"
ORDER BY
    lastname, firstname
'''.format
