SELECT
    row_number() over (order by end_date) as latest, prog,
    yr, sess, subsess, acyr, beg_date, end_date
FROM
    acad_cal_rec
WHERE
    beg_date > DATE("2010-01-01")
AND
    beg_date < CURRENT
AND
    subsess = ""
ORDER BY
    end_date DESC
INTO TEMP
    ordered_terms
WITH NO LOG;

SELECT
    stu_acad_rec.id, max(ordered_terms.latest) as latest
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
WITH NO LOG;


SELECT
    trim(id_rec.firstname) as fistname,
    trim(id_rec.lastname) as lastname,
    sa.id, latest_term.latest, stu_acad_rec.yr, stu_acad_rec.prog,
    stu_acad_rec.subprog, stu_acad_rec.sess, sa.add_date,
    sa.bal_act as sa_bal, pc.bal_act as pc_bal, ca.bal_act as ca_bal,
    ca1.bal_act as ca1_bal, wo.bal_act as wo_bal, (
        nvl(sa.bal_act,0) +
        nvl(pc.bal_act,0) +
        nvl(ca.bal_act,0) +
        nvl(ca1.bal_act,0) +
        nvl(wo.bal_act,0)
    ) as total_bal,
    sa.ccresrc, sa.def_pmt_terms, sa.payplan, sa.payplan_date, sa.stat,
    sa.alt_addr_code, sa.cr_rating, sa.def_disc, sa.descr,
    sa.interest_wvd, sa.written_off, sa.collect_agc
FROM
    suba_rec sa
LEFT JOIN
    suba_rec pc
ON
    sa.subs = "S/A" and pc.subs = "P/C" and pc.id = sa.id
LEFT JOIN
    suba_rec ca
ON
    ca.subs = "C/A" and sa.id = ca.id
LEFT JOIN
    suba_rec ca1
ON
    ca1.subs = "C/A1" and sa.id = ca1.id
LEFT JOIN
    suba_rec wo
ON
    wo.subs = "W/O" and sa.id = wo.id
LEFT JOIN
    latest_term
ON
    sa.id = latest_term.id and sa.subs = "S/A"
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
    sa.id = 1404156
ORDER BY
    latest_term.latest DESC, sa.id;
