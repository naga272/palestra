
CREATE TABLE Registi(
    codR int primary KEY auto_increment,
    nome varchar(64) not null,
    cognome varchar(64) not NULL
);


CREATE TABLE Film(
    codFilm INT PRIMARY KEY auto_increment,
    titolo varchar(255) not null,
    codR INT NOT null,
    animazione BOOL NOT NULL,
    anno DATE NOT NULL,
    dataIta DATE,
	 foreign key(codR) references Registi(codR)
);


INSERT INTO Registi(nome, cognome)
VALUES("lorem", "ipsum");


INSERT INTO Registi(nome, cognome)
VALUES("Mario", "Rossi");


INSERT INTO Registi(nome, cognome)
VALUES("lorem", "ipsum");


INSERT INTO Registi(nome, cognome)
VALUES("lorem", "ipsum");


INSERT INTO Registi(nome, cognome)
VALUES("lorem", "ipsum");

-- POPOLAZIONE TABELLA FILM
INSERT INTO Film(titolo, codR, animazione, anno)
VALUES("Titolo Film", 1, TRUE, "2025-01-12");

INSERT INTO Film(titolo, codR, animazione, anno)
VALUES("Titolo Film", 1, TRUE, "2025-01-12");

INSERT INTO Film(titolo, codR, animazione, anno)
VALUES("Titolo Film", 1, TRUE, "2025-01-12");

INSERT INTO Film(titolo, codR, animazione, anno)
VALUES("Titolo Film", 1, TRUE, "2025-01-12");

INSERT INTO Film(titolo, codR, animazione, anno)
VALUES("Titolo Film", 1, TRUE, "2025-01-12");

-- SECONDA PARTE

CREATE TABLE Regioni(
	idRegione CHAR(2) PRIMARY KEY,
	nomeRegione VARCHAR(32) NOT NULL
);


CREATE TABLE Fiumi(
	nome VARCHAR(32),
	lunghezza FLOAT NOT NULL,
	idRegione CHAR(2) NOT NULL,
	PRIMARY KEY(nome, idRegione),
	FOREIGN KEY (idRegione) REFERENCES Regioni(idRegione)
);


INSERT INTO Regioni(idRegione, nomeRegione)
VALUES('VT', 'VENETO');


INSERT INTO Regioni(idRegione, nomeRegione)
VALUES('LZ', 'LAZIO');


INSERT INTO Regioni(idRegione, nomeRegione)
VALUES('LB', 'LOMBARDIA');


INSERT INTO Regioni(idRegione, nomeRegione)
VALUES('SC', 'SICILIA');

INSERT INTO Fiumi(nome, lunghezza, idRegione)
VALUES('Ipsum', 1208.03, 'SC');



-- MODIFICA TABELLE

-- ALTER TABLE <t> add <TipoDato> <Vincoli>;
-- ALTER TABLE <t> DROP COLUMN <nome_colonna>;
-- ALTER TABLE <t> DROP constraint (<colonna>);

-- togliere vincolo NULL da una tabella:
-- ALTER TABLE <t> CHANGE <colonna> <colonna> type NULL;
-- ALTER TABLE <t> DROP FOREIGN KEY <colonna>;

-- UPDATE:
-- usata per modificare i record della tabella

-- UPDATE <t>
-- SET (colonna1 = valore1, ...)
-- [WHERE condizione];
