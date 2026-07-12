CREATE TABLE if not exists Attori (
    ID INT PRIMARY KEY,
    Nome VARCHAR(50),
    Cognome VARCHAR(50),
    AnnoNascita INT
);

CREATE TABLE if not exists Film (
    ID INT PRIMARY KEY,
    Titolo VARCHAR(100),
    Regista VARCHAR(100),
    AnnoProduzione INT
);

CREATE TABLE if not exists Sale (
    ID INT PRIMARY KEY,
    Nome VARCHAR(100),
    Città VARCHAR(100),
    Posti INT
);

CREATE TABLE if not exists Interpretazioni (
    IDAttore INT,
    IDFilm INT,
    PRIMARY KEY (IDAttore, IDFilm),
    FOREIGN KEY (IDAttore) REFERENCES Attori(ID),
    FOREIGN KEY (IDFilm) REFERENCES Film(ID)
);

CREATE TABLE if not exists Proiezioni (
    IDFilm INT,
    IDSala INT,
    DataProiezione DATE,
    Incasso DECIMAL(10,2),
    PRIMARY KEY (IDFilm, IDSala, DataProiezione),
    FOREIGN KEY (IDFilm) REFERENCES Film(ID),
    FOREIGN KEY (IDSala) REFERENCES Sale(ID)
);