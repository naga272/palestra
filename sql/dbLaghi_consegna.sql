
CREATE TABLE if not exists capitali(
	idCapitale int PRIMARY KEY,
	nomeC VARCHAR(255) NOT NULL,
	abitanti int NOT NULL
);


CREATE TABLE if not exists  stati(
	idStato VARCHAR(3),
	nomeS VARCHAR(255) NOT NULL,
	idCapitale INT NOT NULL,
	PRIMARY KEY (idStato, idCapitale),
	FOREIGN KEY (idCapitale) REFERENCES capitali(idCapitale)
);


CREATE TABLE if not exists laghi(
	idLago INT,
	nomeL VARCHAR(255) NOT NULL,
	altitudine INT,
	superficie INT NOT NULL,
	idStato VARCHAR(3),
	PRIMARY KEY(idLago, idStato),
	FOREIGN KEY (idStato) REFERENCES stati(idStato)
);


INSERT INTO capitali(idCapitale, nomeC, abitanti)
VALUES(1, "Roma", 1111111);

INSERT INTO capitali(idCapitale, nomeC, abitanti)
VALUES(2, "Lorem", 24152);

INSERT INTO capitali(idCapitale, nomeC, abitanti)
VALUES(3, "ipsum", 564654);

INSERT INTO capitali(idCapitale, nomeC, abitanti)
VALUES(4, "Ritchie", 12345666);

INSERT INTO capitali(idCapitale, nomeC, abitanti)
VALUES(5, "Lambda", 99999998);

INSERT INTO stati(idStato, nomeS, idCapitale)
VALUES("ITA", "Italia", 1);

INSERT INTO stati(idStato, nomeS, idCapitale)
VALUES("CIA", "Ciaone", 2);

INSERT INTO stati(idStato, nomeS, idCapitale)
VALUES("CIR", "Circo", 3);

INSERT INTO stati(idStato, nomeS, idCapitale)
VALUES("LAM", "Lambda calcolo", 4);

INSERT INTO stati(idStato, nomeS, idCapitale)
VALUES("LOM", "Lombda colcolo", 5);

INSERT INTO laghi(idLago, nomeL, altitudine, superficie, idStato)
VALUES(1, "Garda", 65, 370, "ITA");

INSERT INTO laghi(idLago, nomeL, altitudine, superficie, idStato)
VALUES(2, "Gardozzo", 655, 3770, "CIA");

INSERT INTO laghi(idLago, nomeL, altitudine, superficie, idStato)
VALUES(3, "Imu", 200, 410, "CIR");

INSERT INTO laghi(idLago, nomeL, altitudine, superficie, idStato)
VALUES(4, "Acab", 200, 410, "CIR");

INSERT INTO laghi(idLago, nomeL, altitudine, superficie, idStato)
VALUES(5, "qwertyuiop", 200, 410, "LOM");


-- Trovare l’id dei laghi con supericie tra i 200 e i 500 km2 e di cui non si conosce l’altitudine.
SELECT L.idLago
FROM laghi AS L
WHERE L.altitudine = NULL AND L.superficie BETWEEN 200 and 500;


-- Trovare tutti i dati dei laghi in cui la penultima lettera del nomeL sia una ‘n’ oppure una ‘d’.
SELECT laghi.*
FROM laghi
WHERE nomeL LIKE "%n" OR nomeL LIKE "%d";


-- Trovare il nome dei laghi con il nome dello stato in cui si trovano e il nome della capitale dello stato.
SELECT L.nomeL, S.nomeS, C.nomeC
FROM (laghi AS L JOIN stati AS S ON L.idStato=S.idStato) JOIN capitali AS C ON S.idCapitale = C.idCapitale;


-- Trovare il nome degli stati in cui si trovano laghi il cui nome inizia per G e che siano
-- o più estesi di 200 km2 o ad una altitudine maggiore di 300 metri slm, senza
-- ripetizioni.

SELECT distinct S.nomeS
FROM laghi AS L JOIN stati AS S ON L.idStato = S.idStato
WHERE L.altitudine > 300 OR L.superficie > 200;

-- Trovare i laghi che si trovano in uno Stato la cui capitale è Berlino oppure Roma.

SELECT L.nomeL 
FROM (laghi AS L JOIN stati AS S ON L.idStato = S.idStato) JOIN capitali AS C ON S.idCapitale = C.idCapitale
WHERE C.nomeC = "Berlino" OR C.nomeC = "Roma";
