SELECT
    vch_rec.vch_ref, vch_table.txt, count(*) as count
FROM
    vch_rec, vch_table
WHERE
    vch_rec.vch_ref= vch_table.jrnl
GROUP BY
    vch_rec.vch_ref, vch_table.txt
ORDER BY
    count desc

SELECT
    vch_rec.stn_no AS Station, userid_table.user_name AS User,
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
    vch_rec.jrnl_no = gle_rec.jrnl_no AND vch_rec.vch_ref = gle_rec.jrnl_ref
LEFT JOIN
    userid_table
ON
    vch_rec.prep_uid = userid_table.uid
INNER JOIN
    gltr_rec
ON
    gle_rec.jrnl_ref = gltr_rec.jrnl_ref AND
    gle_rec.jrnl_no = gltr_rec.jrnl_no AND
    gle_rec.gle_no = gltr_rec.ent_no
WHERE
    vch_rec.vch_ref = "CH"
AND
    vch_rec.jrnl_no = 228
AND
    vch_ref.stat <> "V"
ORDER BY
    gltr_rec.fund, gltr_rec.func, gltr_rec.obj, gltr_rec.proj, gle_rec.gle_no;
