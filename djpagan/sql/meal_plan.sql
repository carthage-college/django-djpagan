SELECT
    TRIM(NVL(meal_plan_type, '')),
    (TRIM(cvid_rec.ldap_name) || '@carthage.edu') AS email,
    id_rec.lastname, id_rec.firstname
FROM
    id_rec
LEFT JOIN
    cvid_rec
ON
    id_rec.id = cvid_rec.cx_id
LEFT JOIN
    stu_serv_rec
ON
    id_rec.id = stu_serv_rec.id
WHERE
    yr = 2022
AND
    sess = 'RC'
AND id_rec.id =
