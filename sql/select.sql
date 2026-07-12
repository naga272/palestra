CREATE TABLE if not exists Registi(
    codR CHAR(5) primary KEY,
    nome varchar(64) not null,
    cognome varchar(64) not NULL
);


CREATE TABLE if not exists Film(
    codFilm INT PRIMARY KEY auto_increment,
    titolo varchar(255) not null,
    codR CHAR(5) NOT null,
    animazione BOOL NOT NULL,
    anno DATE NOT NULL,
    dataIta DATE,
	 foreign key(codR) references Registi(codR)
);

-- 1. Trovare il codice del regista del film con id 3.
SELECT codR
FROM Film
WHERE codFilm = 3;

-- 2. Trovare tutti i titoli e gli id dei film di animazione.
SELECT titolo, codFilm
FROM Film
WHERE animazione = TRUE;

-- 3. Trovare il titolo dei film non di animazione usciti quest'anno per cui non si conosce la data di uscita in Italia.
SELECT titolo
FROM Film
WHERE animazione = 1 AND dataIta IS NULL AND anno BETWEEN "2025-01-01" AND "2025-12-31";

-- 4. Trovare il titolo dei film che iniziano per "La" o per "Il".
SELECT titolo
FROM Film
WHERE titolo LIKE "La%" OR titolo LIKE "Il%";

-- 5. Trovare il codice dei registi che hanno prodotto film di animazione.
SELECT codR
FROM Film
WHERE animazione = 1;

-- 6. Trovare i film usciti in Italia nel 2021 o nel 2019.
SELECT *
FROM Film
WHERE dataIta BETWEEN '2019-01-00' AND '2021-12-31';

-- 7. Trovare tutti i registi che contengono nel nome "anna" o "Anna" (es: Anna, Annalisa,
-- Arianna, Marianna, ...)
SELECT *
FROM Registi
WHERE nome LIKE '%anna%' OR nome LIKE '%Anna%';


-- 8. Trovare il codice regista dei film usciti in Italia durante le vacanze di Natale 21-22.
SELECT codR
FROM Film
WHERE dataIta BETWEEN '2021-12-23' AND '2021-01-07' OR dataIta BETWEEN '2022-12-23' AND '2022-01-07';


-- 9. Trovare il risultato dell’operazione di join tra le due tabelle, provando entrambe le sintassi.
SELECT *
FROM Registi inner JOIN Film ON Registi.codR = Film.codR;

SELECT *
FROM Registi right JOIN Film ON Registi.codR = Film.codR;

SELECT *
FROM Registi left JOIN Film ON Registi.codR = Film.codR;


-- 10. Trovare i dati di tutti i film del regista Steven Spielberg (o di un altro regista inserito nel database).
SELECT *
FROM Film INNER JOIN Registi ON Film.codR = Registi.codR
WHERE Registi.nome = 'Steven' AND Registi.cognome = 'Spielberg';








