SELECT *
FROM comuni NATURAL JOIN popolazione_residente NATURAL JOIN stranieri_residenti NATURAL JOIN abitazioni NATURAL JOIN famiglie NATURAL JOIN edifici

SELECT *
FROM comuni NATURAL JOIN localita NATURAL JOIN popolazione_residente NATURAL JOIN stranieri_residenti NATURAL JOIN abitazioni NATURAL JOIN famiglie NATURAL JOIN edifici

SELECT *
FROM comuni NATURAL JOIN sezioni NATURAL JOIN popolazione_residente NATURAL JOIN stranieri_residenti NATURAL JOIN abitazioni NATURAL JOIN famiglie NATURAL JOIN edifici


SELECT *
FROM (comuni NATURAL JOIN localita NATURAL JOIN popolazione_residente NATURAL JOIN stranieri_residenti NATURAL JOIN abitazioni NATURAL JOIN famiglie NATURAL JOIN edifici), loc_extra
WHERE comuni.procom = loc_extra.pro_com
LIMIT 500