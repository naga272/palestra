CREATE DATABASE if NOT EXISTS db;
USE db;

CREATE TABLE if NOT EXISTS Prodotti(
	id INT PRIMARY KEY AUTO_INCREMENT,
	Nome NVARCHAR(32) NOT NULL,
	Descrizione TEXT NOT NULL,
	Prezzo FLOAT NOT null
);


INSERT INTO Prodotti(Nome, Descrizione, Prezzo)
VALUES ("Lorem", "Lorem ipsum dolor", 4.12),
("Lorem", "Lorem ipsum dolor", 8.88),
("Ipsum", "Lorem ipsum dolor", 9.99),
("Dolor", "Lorem ipsum dolodbr", 4.12);
