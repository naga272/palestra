use ospedale;

create table if not exists Medici(
	codiceM char(5) primary key,
	nome varchar(32) not null,
	cognome varchar(32) not null,
	specializzazione varchar(32) not null,
	telefono varchar(9) not null
);


create table if not exists pazienti(
	cf char(16) primary key not null,
	nome varchar(32) not null,
	cognome varchar(32) not null,
	dataN date not null,
	indirizzo varchar(64)
);


create table if not exists PrenotazioniVisite(
	cf char(16),
	codiceM char(5),
	dataVisita date,
	numeroAmbulatorio int not null,
	primary key(cf, codiceM, dataVisita),
	foreign key(cf) references pazienti(cf),
	foreign key(codiceM) references Medici(codiceM)
);


INSERT INTO Medici (codiceM, nome, cognome, specializzazione, telefono) VALUES
('M0001', 'Luca', 'Rossi', 'Cardiologia', '345123456'),
('M0002', 'Giulia', 'Bianchi', 'Neurologia', '345234567'),
('M0003', 'Marco', 'Verdi', 'Pediatria', '345345678'),
('M0004', 'Sara', 'Neri', 'Dermatologia', '345456789'),
('M0005', 'Paolo', 'Gialli', 'Ortopedia', '345567890');

INSERT INTO pazienti (cf, nome, cognome, dataN, indirizzo) VALUES
('RSSMRA01A01H501Z', 'Mario', 'Rossi', '1985-01-01', 'Via Roma 1, Milano'),
('BNCLGU02B02H501Y', 'Luca', 'Bianchi', '1990-02-02', 'Via Milano 2, Torino'),
('VRDGNN03C03H501X', 'Gianna', 'Verdi', '2000-03-03', 'Via Napoli 3, Roma'),
('NRSRRA04D04H501W', 'Sara', 'Neri', '1995-04-04', 'Via Firenze 4, Firenze'),
('PLLGLL05E05H501V', 'Paolo', 'Gialli', '1988-05-05', 'Via Venezia 5, Venezia');

INSERT INTO PrenotazioniVisite (cf, codiceM, dataVisita, numeroAmbulatorio) VALUES
('RSSMRA01A01H501Z', 'M0001', '2026-02-01', 101),
('BNCLGU02B02H501Y', 'M0002', '2026-02-03', 102),
('VRDGNN03C03H501X', 'M0003', '2026-02-05', 103),
('NRSRRA04D04H501W', 'M0004', '2026-02-07', 104),
('PLLGLL05E05H501V', 'M0005', '2026-02-09', 105);



-- 1) Trovare tutti i dati dei cittadini che per il 2025 hanno prenotato una visita con un medico
-- specializzato in cardiologia.

select distinct pa.*
from PrenotazioniVisite P
join Pazienti as pa on P.cf = pa.cf
join Medici as m on P.codiceM = m.codiceM
where P.dataVisita like "2025%" and m.specializzazione = 'cardiologia';

-- 2. Trovare tutti i medici con cui ha prenotato visite Mario Rossi.
select distinct m.*
from prenotazionivisite p
join medici m on p.codiceM = m.codiceM
join Pazienti pa on p.cf = pa.cf
where pa.nome = "Mario" and pa.cognome = "Rossi";


-- 3) Trovare la data di nascita dei cittadini che hanno prenotato visite con specialisti in
-- discipline che cominciano con “endo”.

select pa.cf, pa.dataN
from prenotazionivisite p
join Pazienti pa on p.cf = pa.cf
join Medici as m on P.codiceM = m.codiceM
where m.specializzazione like "endo%";


-- 4. Trovare gli ambulatori in cui visitano i medici specializzati in pneumologia, senza
-- ripetizioni.
select distinct p.numeroAmbulatorio
from prenotazionivisite p
join medici m on p.codiceM = m.codiceM
where m.specializzazione = "pneumologia";


-- 5. Trovare tutte le date in cui Mario Rossi ha avuto visite prenotate con il medico Gigi
-- Grandottore.
select p.dataVisita
from prenotazionivisite p
join Pazienti pa on p.cf = pa.cf
join Medici as m on P.codiceM = m.codiceM
where pa.nome = "Mario" and pa.cognome = "Rossi" and m.nome = "Gigi" and m.cognome = "Grandattore";


-- 6. Trovare chi ha prenotato visite con Gigi Grandottore per gennaio 2026 o per marzo
-- 2026.

select pa.*
from prenotazionivisite p
join Pazienti pa on p.cf = pa.cf
join Medici as m on P.codiceM = m.codiceM
where (
	pa.nome = "Mario" and pa.cognome = "Rossi" and
	m.nome = "Gigi" and m.cognome = "Grandattore" and
	(p.dataVisita like "2026-01%" or p.dataVisita like "2026-03%")
); 


-- 7. Trovare chi ha visitato cittadini di cui non si conosce l’indirizzo.
select distinct m.*
from prenotazionivisite p
join Pazienti pa on p.cf = pa.cf
join Medici as m on P.codiceM = m.codiceM
where pa.indirizzo is NULL; 


-- 8. Trovare cf, nome e cognome dei cittadini che per dicembre 2025 hanno prenotato una
-- visita con un medico specializzato in cardiologia o in pneumologia. 
select distinct pa.cf, pa.nome, pa.cognome
from prenotazionivisite p
join Pazienti pa on p.cf = pa.cf
join Medici as m on P.codiceM = m.codiceM
where (
	(m.specializzazione = 'cardiologia' or m.specializzazione = 'pneumologia') and
	p.dataVisita like '2025-12%'
); 