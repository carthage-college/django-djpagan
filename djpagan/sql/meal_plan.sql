SELECT
    TRIM(NVL(meal_plan_type, '')),
    TRIM(cvid_rec.ldap_name) as ldap_name
FROM
    stu_serv_rec
LEFT JOIN
    cvid_rec
ON
    stu_serv_rec.id = cvid_rec.cx_id
WHERE
    yr = 2022
AND
    sess = 'RC'
AND id = 1570198

