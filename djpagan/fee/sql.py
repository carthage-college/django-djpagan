ORDERED_TERMS_TEMP = '''
SELECT
    ROW_NUMBER() OVER (ORDER BY end_date) AS latest, prog,
    yr, sess, subsess, acyr, beg_date, end_date
FROM
    acad_cal_rec
WHERE
    beg_date > "{start_date}"
AND
    beg_date < CURRENT
AND
    subsess = ""
ORDER BY
    end_date DESC
INTO TEMP
    ordered_terms
WITH NO LOG
'''.format

LATEST_TERM_TEMP = '''
SELECT
    stu_acad_rec.id, MAX(ordered_terms.latest) AS latest
FROM
    stu_acad_rec, ordered_terms
WHERE
    stu_acad_rec.id in (
        SELECT id
        FROM   suba_rec
        WHERE  subs= "S/A"
    )
AND
    ordered_terms.prog = stu_acad_rec.prog
AND
    ordered_terms.yr = stu_acad_rec.yr
AND
    ordered_terms.sess = stu_acad_rec.sess
GROUP BY
    stu_acad_rec.id
INTO TEMP
    latest_term
WITH NO LOG
'''

SA_BALANCES_TEMP = '''
SELECT
    subtr_rec.subs_no AS id, SUM(subtr_rec.amt) AS late_fee_balance
FROM
    subtr_rec
JOIN
    sube_rec
ON
    subtr_rec.ent_no = sube_rec.sube_no
AND
    subtr_rec.subs_no = sube_rec.subs_no
AND
    subtr_rec.subs = sube_rec.subs
WHERE
    subtr_rec.subs = "S/A"
AND
    subtr_rec.stat = "P"
AND
    (
        sube_rec.jrnl_date < MDY(MONTH(CURRENT), 15, YEAR(CURRENT)) - 1
        UNITS MONTH OR subtr_rec.amt < 0
    )
GROUP BY
    subtr_rec.subs_no
HAVING
    SUM(subtr_rec.amt) > 0
INTO TEMP
    sa_balances
WITH NO LOG
'''

PC_BALANCES_TEMP = '''
SELECT
    subtr_rec.subs_no AS id, SUM(subtr_rec.amt) AS late_fee_balance
FROM
    subtr_rec
JOIN
    sube_rec
ON
    subtr_rec.ent_no = sube_rec.sube_no
AND
    subtr_rec.subs_no = sube_rec.subs_no
AND
    subtr_rec.subs = sube_rec.subs
WHERE
    subtr_rec.subs = "P/C"
AND
    subtr_rec.stat = "P"
AND
    (
        sube_rec.jrnl_date < MDY(MONTH(CURRENT), 15, YEAR(CURRENT)) - 1
        UNITS MONTH OR subtr_rec.amt < 0
    )
GROUP BY
    subtr_rec.subs_no
HAVING
    SUM(subtr_rec.amt) > 0
INTO TEMP
    pc_balances
WITH NO LOG
'''

CA_BALANCES_TEMP = '''
SELECT
    subtr_rec.subs_no AS id, SUM(subtr_rec.amt) AS late_fee_balance
FROM
    subtr_rec
JOIN
    sube_rec
ON
    subtr_rec.ent_no = sube_rec.sube_no 
AND
    subtr_rec.subs_no = sube_rec.subs_no
AND
    subtr_rec.subs = sube_rec.subs
WHERE
    subtr_rec.subs = "C/A"
AND
    subtr_rec.stat = "P"
AND
    (
        sube_rec.jrnl_date < MDY(MONTH(CURRENT), 15, YEAR(CURRENT)) - 1
        UNITS MONTH OR subtr_rec.amt < 0
    )
GROUP BY
    subtr_rec.subs_no
HAVING
    SUM(subtr_rec.amt) > 0
INTO TEMP
    ca_balances
WITH NO LOG
'''

CA1_BALANCES_TEMP = '''
SELECT
    subtr_rec.subs_no AS id, SUM(subtr_rec.amt) AS late_fee_balance
FROM
    subtr_rec
JOIN
    sube_rec
ON
    subtr_rec.ent_no = sube_rec.sube_no
AND
    subtr_rec.subs_no = sube_rec.subs_no
AND
    subtr_rec.subs = sube_rec.subs
WHERE
    subtr_rec.subs = "C/A1"
AND
    subtr_rec.stat = "P"
AND
    (
        sube_rec.jrnl_date < MDY(MONTH(CURRENT), 15, YEAR(CURRENT)) - 1
        UNITS MONTH OR subtr_rec.amt < 0
    )
GROUP BY
    subtr_rec.subs_no
HAVING
    SUM(subtr_rec.amt) > 0
INTO TEMP
    ca1_balances
WITH NO LOG
'''

WO_BALANCES_TEMP = '''
SELECT
    subtr_rec.subs_no AS id, SUM(subtr_rec.amt) AS late_fee_balance
FROM
    subtr_rec
JOIN
    sube_rec
ON
    subtr_rec.ent_no = sube_rec.sube_no
AND
    subtr_rec.subs_no = sube_rec.subs_no
AND
    subtr_rec.subs = sube_rec.subs
WHERE
    subtr_rec.subs = "W/O"
AND
    subtr_rec.stat = "P"
AND
    (
        sube_rec.jrnl_date < MDY(MONTH(CURRENT), 15, YEAR(CURRENT)) - 1
        UNITS MONTH OR subtr_rec.amt < 0
    )
GROUP BY
    subtr_rec.subs_no
HAVING
    SUM(subtr_rec.amt) > 0
INTO TEMP
    wo_balances
WITH NO LOG
'''

STUDENT_BALANCE_LATE_FEE = '''
SELECT
    trim(id_rec.firstname) AS fistname,
    trim(id_rec.lastname) AS lastname,
    sa.id, latest_term.latest, stu_acad_rec.yr, stu_acad_rec.prog,
    stu_acad_rec.subprog, stu_acad_rec.sess,
    sa_balances.late_fee_balance AS sa_bal,
    pc_balances.late_fee_balance AS pc_bal,
    ca_balances.late_fee_balance AS ca_bal,
    ca1_balances.late_fee_balance AS ca1_bal,
    wo_balances.late_fee_balance AS wo_bal, (
        nvl(sa_balances.late_fee_balance,0) +
        nvl(pc_balances.late_fee_balance,0) +
        nvl(ca_balances.late_fee_balance,0) +
        nvl(ca1_balances.late_fee_balance,0) +
        nvl(wo_balances.late_fee_balance,0)
    ) AS total_bal,
    sa.ccresrc, sa.def_pmt_terms, sa.payplan, sa.payplan_date, sa.stat,
    sa.alt_addr_code, sa.cr_rating, sa.def_disc, sa.descr, sa.interest_wvd,
    sa.written_off, sa.collect_agc
FROM
    suba_rec sa
LEFT JOIN
     sa_balances
ON
    sa.subs = "S/A" AND sa_balances.id = sa.id
LEFT JOIN
    pc_balances
ON
     pc_balances.id = sa.id
LEFT JOIN
    ca_balances
ON
    ca_balances.id = sa.id
LEFT JOIN
    ca1_balances
ON
    ca1_balances.id = sa.id
LEFT JOIN
    wo_balances
ON
    wo_balances.id = sa.id
LEFT JOIN
    latest_term
ON
    sa.id = latest_term.id AND sa.subs = "S/A"
LEFT JOIN
    ordered_terms
ON
    ordered_terms.latest = latest_term.latest,
    stu_acad_rec, id_rec
WHERE
  stu_acad_rec.yr = ordered_terms.yr
AND
    stu_acad_rec.prog = ordered_terms.prog
AND
    stu_acad_rec.sess = ordered_terms.sess
AND
    stu_acad_rec.id = latest_term.id
AND
    sa.id = id_rec.id
AND
    (
        (
            NVL(sa_balances.late_fee_balance,0) +
            NVL(pc_balances.late_fee_balance,0) +
            NVL(ca_balances.late_fee_balance,0) +
            NVL(ca1_balances.late_fee_balance,0) +
            NVL(wo_balances.late_fee_balance,0)
        ) > 0
    )
ORDER BY
    latest_term.latest DESC, sa.id
'''
