
SELECT COUNT(*)
FROM spatial_ref
WHERE cod_reg = 4 AND sez2011 NOT IN(
    SELECT sez2011
    FROM sezioni NATURAL JOIN comuni
    WHERE codreg = 4)