JOURNAL_TYPES = '''
SELECT
    vch_rec.vch_ref, vch_table.txt, count(*) AS count
FROM
    vch_rec, vch_table
WHERE
    vch_rec.vch_ref= vch_table.jrnl
GROUP BY
    vch_rec.vch_ref, vch_table.txt
ORDER BY
    count DESC
'''

JOURNAL_TRANSACTIONS = '''
SELECT
    vch_rec.stn_no AS station, userid_table.user_name AS User,
    vch_rec.amt_type, vch_rec.vch_ref, vch_rec.jrnl_no, vch_rec.stat
    AS Vch_Status, gle_rec.gle_no, vch_rec.pst_date, vch_rec.fscl_yr,
    vch_rec.fscl_mo, gle_rec.descr AS GLEdesc, gle_rec.doc_ref,
    gle_rec.doc_no, gle_rec.doc_id, gle_rec.ctgry AS CtgryGle, gltr_rec.amt,
    gltr_rec.fund, gltr_rec.func, gltr_rec.obj, gltr_rec.proj, gltr_rec.stat
FROM
    vch_rec
INNER JOIN
    gle_rec
ON
    vch_rec.jrnl_no = gle_rec.jrnl_no
AND
    vch_rec.vch_ref = gle_rec.jrnl_ref
LEFT JOIN
    userid_table
ON
    vch_rec.prep_uid = userid_table.uid
INNER JOIN
    gltr_rec
ON
    gle_rec.jrnl_ref = gltr_rec.jrnl_ref
AND
    gle_rec.jrnl_no = gltr_rec.jrnl_no
AND
    gle_rec.gle_no = gltr_rec.ent_no
WHERE
    vch_rec.vch_ref = "{vch_ref}"
AND
    vch_rec.jrnl_no = {journal_no}
{stat}
ORDER BY
    gltr_rec.fund, gltr_rec.func, gltr_rec.obj, gltr_rec.proj, gle_rec.gle_no
'''.format
BRIDGED_CLASSES = '''
SELECT
    a.yr, a.crs_no, a.sec_no as sec_no, a.sess as a_sess, b.sess as b_sess,
    trim(crs_rec.title1) || " " || trim(crs_rec.title2) as course_title,
    a.title as a_title, b.title as b_title
FROM
    sec_rec a
JOIN
    sec_rec b
ON
    a.yr= b.yr
AND
    a.crs_no = b.crs_no
AND
    a.sec_no = b.sec_no
AND (
        (a.sess = "AA" and b.sess = "AB")
    OR
        (a.sess = "AK" and b.sess = "AM")
    OR
        (a.sess = "AS" and b.sess = "AT")
),
    crs_rec
WHERE
    crs_rec.crs_no = a.crs_no
AND
    crs_rec.cat = a.cat
AND
    a.hrs= 2.0
AND
    b.hrs = 2.0
AND
    a.yr > {year}
{course_no}
ORDER BY
    a.yr, a.sess, a.crs_no, a.sec_no
'''.format

BRIDGED_CLASSES_STUDENTS = '''
SELECT
    cw_rec.id AS CW_IDno, id_rec.fullname, cw_rec.crs_no, cw_rec.sec,
    cw_rec.yr, cw_rec.sess, cw_rec.subsess, cw_rec.cat, cw_rec.hrs,
    cw_rec.id, cw_rec.stat AS CWstat,
    cw_rec.cw_no AS CWno, reg_rec.*
FROM
    cw_rec
LEFT JOIN
    reg_rec
ON
    cw_rec.cw_no = reg_rec.cw_no
INNER JOIN
    id_rec
ON
    cw_rec.id = id_rec.id
WHERE
    cw_rec.crs_no = "{course_no}"
AND
    cw_rec.yr = {year}
AND
    cw_rec.sess = "{a_sess}"
OR
    cw_rec.crs_no = "{course_no}"
AND
    cw_rec.yr = {year}
AND
    cw_rec.sess = "{b_sess}"
ORDER BY
    cw_rec.id, cw_rec.crs_no, cw_rec.sec, cw_rec.yr, cw_rec.sess,
    reg_rec.sys_date, reg_rec.tm, reg_rec.beg_date
'''.format

ALL_TRANSACTIONS = '''
SELECT
     vch_rec.stn_no,
     userid_table.user_name,
     gle_rec.jrnl_ref,
     gle_rec.jrnl_no,
     gle_rec.gle_no,
     gle_rec.descr,
     gle_rec.doc_ref,
     gle_rec.doc_no,
     gle_rec.doc_id,
     gle_rec.ctgry AS GLE_Ctgry,
     gle_rec.pmt_frm,
     gle_rec.pmt_no,
     sube_rec.jrnl_date,
     gle_rec.add_date,
     vch_rec.pst_date,
     vch_rec.stat AS VCH_Stat,
     sube_rec.stat AS SUBE_Stat,
     subtr_rec.amt,
     subtr_rec.subs,
     suba_rec.suba_no,
     id_rec.fullname,
     subtr_rec.stat AS SUBTR_Stat,
     sube_rec.ctgry,
     sube_rec.sube_no AS SUBE_EntNo,
     subtr_rec.tot_code,
     subtr_rec.tot_prd,
     subtr_rec.bal_code,
     subtr_rec.bal_prd
FROM
    (
        (
        vch_rec
            INNER JOIN
                gle_rec
            ON
                (vch_rec.jrnl_no = gle_rec.jrnl_no)
            AND
                (vch_rec.vch_ref = gle_rec.jrnl_ref)
        )
        LEFT JOIN
            userid_table
        ON
            vch_rec.prep_uid = userid_table.uid
    )
    INNER JOIN (
        (
            (
            suba_rec
                INNER JOIN
                    sube_rec
                ON
                     (suba_rec.subs = sube_rec.subs)
                AND
                    (suba_rec.suba_no = sube_rec.subs_no)
            )
            INNER JOIN
                subtr_rec
            ON
                (sube_rec.subs = subtr_rec.subs)
            AND
                (sube_rec.subs_no = subtr_rec.subs_no)
            AND
                (sube_rec.sube_no = subtr_rec.ent_no)
        )
        INNER JOIN
            id_rec
        ON
            sube_rec.subs_no = id_rec.id
    )
    ON
        (gle_rec.jrnl_ref = sube_rec.jrnl_ref)
    AND
        (gle_rec.jrnl_no = sube_rec.jrnl_no)
    AND
        (gle_rec.gle_no = sube_rec.jrnl_ent_no)
WHERE
    suba_rec.suba_no = {student_id}
{stat}
ORDER BY
    sube_rec.jrnl_date, gle_rec.gle_no, subtr_rec.ent_no
'''.format

CHEQUE_NUMBER = '''
SELECT
    vch_rec.stn_no AS Station,
    userid_table.user_name AS User,
    gle_rec.jrnl_ref, gle_rec.jrnl_no,
    gle_rec.gle_no,
    gle_rec.descr AS GLE_desc,
    gle_rec.doc_ref,
    gle_rec.doc_no,
    gle_rec.doc_id,
    gle_rec.ctgry AS GLE_Ctgry,
    gle_rec.pmt_frm,
    gle_rec.pmt_no AS PaymentNo,
    sube_rec.jrnl_date,
    gle_rec.add_date,
    vch_rec.pst_date,
    sube_rec.stat,
    subtr_rec.amt,
    subtr_rec.subs,
    suba_rec.suba_no,
    id_rec.fullname,
    sube_rec.stat AS SUBE_Stat,
    sube_rec.ctgry,
    sube_rec.sube_no AS SUBE_EntNo,
    subtr_rec.tot_code,
    subtr_rec.tot_prd,
    subtr_rec.bal_code,
    subtr_rec.bal_prd
FROM
    (
        (
        vch_rec
        INNER JOIN
            gle_rec
        ON
            (vch_rec.vch_ref = gle_rec.jrnl_ref)
        AND
            (vch_rec.jrnl_no = gle_rec.jrnl_no)
        )
        LEFT JOIN
            userid_table
        ON
            vch_rec.prep_uid = userid_table.uid
    )
    LEFT JOIN
    (
        (
            (
            suba_rec
            RIGHT JOIN
                sube_rec
            ON
                (suba_rec.suba_no = sube_rec.subs_no)
            AND
                (suba_rec.subs = sube_rec.subs)
            )
            LEFT JOIN
                subtr_rec
            ON
                (sube_rec.sube_no = subtr_rec.ent_no)
            AND
                (sube_rec.subs_no = subtr_rec.subs_no)
            AND
                (sube_rec.subs = subtr_rec.subs)
        )
        LEFT JOIN
            id_rec
        ON
            sube_rec.subs_no = id_rec.id
    )
    ON
        (gle_rec.gle_no = sube_rec.jrnl_ent_no)
    AND
        (gle_rec.jrnl_no = sube_rec.jrnl_no)
    AND
        (gle_rec.jrnl_ref = sube_rec.jrnl_ref)
WHERE
    gle_rec.pmt_no = "{cheque_number}"
{stat}
ORDER BY
    sube_rec.jrnl_date, gle_rec.gle_no, subtr_rec.ent_no
'''.format
