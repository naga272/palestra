
DROP TABLE if exists post;
DROP TABLE if exists follower;
DROP table if exists utente;


create table if not exists utente(
	idutente CHAR(4) primary key,
	username varchar(255) not null,
	email varchar(255) not null,
	passw varchar(255) not null,
	bio text
);


create table if not exists post(
	idpost int auto_increment,
	idutente char(4) not null,
	dataora datetime not null,
	didascalia text,
	primary key(idpost, idutente),
	foreign key(idutente) references utente(idutente)
);


create table if not exists follower(
	idutente char(4) not null,
	idfollower char(4) not null,
	datainizio date not null,
	primary key(idutente, idfollower),
	foreign key(idutente) references utente(idutente),
	foreign key(idfollower) references utente(idutente)
);


insert into utente (idutente, username, email, passw, bio) values
('u001', 'alice',   'alice@mail.com',   'pwdalice',   'Bio di Alice'),
('u002', 'bob',     'bob@mail.com',     'pwdbob',     'Bio di Bob'),
('u003', 'carol',   'carol@mail.com',   'pwdcarol',   null),
('u004', 'dave',    'dave@mail.com',    'pwddave',    'Bio di Dave'),
('u005', 'eve',     'eve@mail.com',     'pwdeve',     null),
('a123', 'anna123', 'anna123@mail.com', 'pwdanna', 'Profilo di Anna'),
('u006', 'luca',    'luca@mail.com',    'pwdluca', 'Bio di Luca'),
('u007', 'maria',   'maria@mail.com',   'pwdmaria', null),
('u008', 'paolo',   'paolo@mail.com',   'pwdpaolo', 'Bio di Paolo'),
('u009', 'francesco', 'francesco@mail.com', 'pwdfranco', 'Profilo di Francesco');

insert into post (dataora, didascalia, idutente) values
('2025-01-10 10:30:00', 'Primo post di Alice', 	'u001'),
('2025-01-10 11:00:00', 'Bob al lavoro',       	'u002'),
('2025-01-11 09:15:00', null,                 	'u003'),
('2025-01-11 18:45:00', 'Foto del tramonto',   	'u001'),
('2025-01-12 20:10:00', 'Serata con amici',    	'u005'),
('2025-12-25 09:30:00', 'Natale 🎄', 			'a123'),
('2025-12-26 14:10:00', null,       			'a123'),
('2025-11-01 08:00:00', 'Buongiorno!',        'u009'),
('2025-11-02 09:15:00', 'Caffè mattutino',    'u009'),
('2025-11-03 18:30:00', 'Allenamento finito', 'u009'),
('2025-11-04 12:45:00', 'Pranzo veloce',      'u009'),
('2025-11-05 20:10:00', 'Serata cinema',      'u009'),
('2025-11-06 14:00:00', 'Relax pomeridiano',  'u009');


insert into follower (idutente, idfollower, datainizio) values
('u001', 'u002', '2024-12-01'), -- Bob segue Alice
('u002', 'u001', '2024-12-02'), -- Alice segue Bob (reciproco)
('u003', 'u001', '2024-12-05'), -- Alice segue Carol
('u004', 'u002', '2024-12-10'), -- Bob segue Dave
('u005', 'u003', '2024-12-15'), -- Carol segue Eve
('a123', 'u006', '2025-01-10'),
('a123', 'u003', '2025-01-10'),
('a123', 'u005', '2025-01-10'),
('a123', 'u001', '2025-01-10'),
('a123', 'u007', '2025-02-03'),
('a123', 'u008', '2025-03-15'),
('u009', 'u001', '2025-01-10'),
('u009', 'u002', '2025-01-12'),
('u009', 'u003', '2025-01-15');



-- 1) Trovare tutti i post pubblicati da utenti che abbiano “ann” nello user.
select P.idpost
from post as P join utente as U on P.idutente = U.idutente
where U.username like "%ann%";


-- 2) Trovare tutte le date in cui ha guadagnato follower chi ha pubblicato post il
-- giorno di Natale 2025, senza ripetizioni.
select distinct f.datainizio
from follower f
join post p on f.idutente = p.idutente
where date(p.dataora) = '2025-12-25';


-- 3) Trovare lo username dei follower di “anna123”.
select u.username
from follower f
join utente u on u.idutente = f.idfollower
where f.idutente = 'anna123';


-- 4) Trovare lo username degli utenti che hanno pubblicato post in dicembre 2025
-- senza didascalia o che abbiano un profilo senza bio, senza ripetizioni.
select distinct U.username
from utente as U
join post as P on U.idutente = P.idutente
where (P.dataora > '2025-12-01' and P.dataora < '2025-12-31' and P.didascalia is null) or U.bio is null;


-- 5) Trovare il numero di follower di “anna123”
select count(*) as num_follower_anna
from follower as F join utente as U on F.idutente = U.idutente
where U.username = 'anna123';


-- 6) Trovare il numero di follower di ogni utente (indicandone anche lo username).
select U.username, count(*)
from utente as U 
join follower as F on U.idutente = F.idutente
group by U.username;


-- 7) Trovare la data dell’ultimo post per ogni utente (con username).
select U.username, max(P.dataora)
from utente as U
join post as P on U.idutente = P.idutente
group by U.username;


-- 8) Per ogni utente, dire quanti follower ha guadagnato al giorno (solo nelle date in
-- cui ne ha guadagnati).
select f.idutente, f.datainizio, count(*) as numero_follower
from follower f
group by f.idutente, f.datainizio;


-- 9) Trovare lo username degli utenti che hanno più di 5 follower.
select U.username, count(*) as num_follower
from utente as U
join follower as F on U.idutente = F.idutente
group by U.username
having count(*) > 5;


-- 10) Trovare lo username di chi ha pubblicato più di 5 post nell’ultima settimana.
select U.username, count(*) as five_post_last_week
from post as P
join utente as U on P.idutente = U.idutente
where P.dataora > '2026-01-04' and P.dataora < '2026-01-12'
group by U.username
having count(*) > 5;


-- 11) Trovare chi ha guadagnato più di 3 follower in un giorno.
select F.idutente, F.datainizio, count(*) as num_follower
from follower F
group by F.idutente, F.datainizio
having count(*) > 3;
