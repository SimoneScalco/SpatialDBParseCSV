--0_create_0-6.sql
CREATE TABLE COMUNI (
PROCOM integer,
CODREG integer,
REGIONE varchar(35),
CODPRO integer,
PROVINCIA varchar(35),
CODCOM integer,
COMUNE varchar(65),
PRIMARY KEY(PROCOM)
);


--1_create_7-11.sql
CREATE TABLE SEZIONI (
SEZ2011 double precision,
PROCOM integer,
NSEZ integer,
ACE integer,
CODLOC integer,
CODASC varchar(10),
PRIMARY KEY(SEZ2011),
FOREIGN KEY(PROCOM) REFERENCES COMUNI (PROCOM)
);


--2_create_12-87.sql
CREATE TABLE POPOLAZIONE_RESIDENTE (
SEZ2011 double precision,
P1 integer,
P2 integer,
P3 integer,
P4 integer,
P5 integer,
P6 integer,
P7 integer,
P8 integer,
P9 integer,
P10 integer,
P11 integer,
P12 integer,
P13 integer,
P14 integer,
P15 integer,
P16 integer,
P17 integer,
P18 integer,
P19 integer,
P20 integer,
P21 integer,
P22 integer,
P23 integer,
P24 integer,
P25 integer,
P26 integer,
P27 integer,
P28 integer,
P29 integer,
P30 integer,
P31 integer,
P32 integer,
P33 integer,
P34 integer,
P35 integer,
P36 integer,
P37 integer,
P38 integer,
P39 integer,
P40 integer,
P41 integer,
P42 integer,
P43 integer,
P44 integer,
P45 integer,
P46 integer,
P47 integer,
P48 integer,
P49 integer,
P50 integer,
P51 integer,
P52 integer,
P53 integer,
P54 integer,
P55 integer,
P56 integer,
P57 integer,
P58 integer,
P59 integer,
P60 integer,
P61 integer,
P62 integer,
P64 integer,
P65 integer,
P66 integer,
P128 integer,
P129 integer,
P130 integer,
P131 integer,
P132 integer,
P135 integer,
P136 integer,
P137 integer,
P138 integer,
P139 integer,
P140 integer,
PRIMARY KEY(SEZ2011),
FOREIGN KEY(SEZ2011) REFERENCES SEZIONI (SEZ2011)
);


--3_create_88-102.sql
CREATE TABLE STRANIERI_RESIDENTI (
SEZ2011 double precision,
ST1 integer,
ST2 integer,
ST3 integer,
ST4 integer,
ST5 integer,
ST6 integer,
ST7 integer,
ST8 integer,
ST9 integer,
ST10 integer,
ST11 integer,
ST12 integer,
ST13 integer,
ST14 integer,
ST15 integer,
PRIMARY KEY(SEZ2011),
FOREIGN KEY(SEZ2011) REFERENCES SEZIONI (SEZ2011)
);


--4_create_103-108.sql
CREATE TABLE ABITAZIONI (
SEZ2011 double precision,
A2 integer,
A3 integer,
A5 integer,
A6 integer,
A7 integer,
A44 integer,
PRIMARY KEY(SEZ2011),
FOREIGN KEY(SEZ2011) REFERENCES SEZIONI (SEZ2011)
);


--5_create_109-120.sql
CREATE TABLE FAMIGLIE (
SEZ2011 double precision,
A46 integer,
A47 integer,
A48 integer,
PF1 integer,
PF2 integer,
PF3 integer,
PF4 integer,
PF5 integer,
PF6 integer,
PF7 integer,
PF8 integer,
PF9 integer,
PRIMARY KEY(SEZ2011),
FOREIGN KEY(SEZ2011) REFERENCES SEZIONI (SEZ2011)
);


--6_create_121-151.sql
CREATE TABLE EDIFICI (
SEZ2011 double precision,
E1 integer,
E2 integer,
E3 integer,
E4 integer,
E5 integer,
E6 integer,
E7 integer,
E8 integer,
E9 integer,
E10 integer,
E11 integer,
E12 integer,
E13 integer,
E14 integer,
E15 integer,
E16 integer,
E17 integer,
E18 integer,
E19 integer,
E20 integer,
E21 integer,
E22 integer,
E23 integer,
E24 integer,
E25 integer,
E26 integer,
E27 integer,
E28 integer,
E29 integer,
E30 integer,
E31 integer,
PRIMARY KEY(SEZ2011),
FOREIGN KEY(SEZ2011) REFERENCES SEZIONI (SEZ2011)
);


