\i tournament.sql

CREATE TABLE tournaments(
	id serial primary key,
	name text,
	winner int references players(id)
);

CREATE TABLE tournament_players(
	tournament int references tournaments(id),
	player int references players(id)
);

insert into tournaments (name) values ('WWW Open');