-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- First off, we need to create the database and connect to it. To do so, we use the commands:
-- vagrant@trusty32: vagrant => CREATE DATABASE tournament;
-- vagrant@trusty32: vagrant => \c tournament;
-- vagrant@trusty32: tournament =>

DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;

\c tournament;

CREATE TABLE players(
	id serial primary key,
	name text
);

CREATE TABLE matches(
	id serial primary key,
	winner int references players(id),
	loser int references players(id)
);

insert into players (name) values ('Player 1 da Silva');
insert into players (name) values ('Player 2 o Segundo');
insert into players (name) values ('Player 3 o Terceiro');
insert into players (name) values ('Player 4 o Quarto');

insert into matches (winner, loser) values (1,2);
insert into matches (winner, loser) values (3,4);

-- create matches_ids view
create view matches_ids as select matches.id, matches.winner as winner, matches.loser as loser from matches, players where matches.winner = players.id or matches.loser = players.id group by matches.id order by matches.id;
-- create winners view
create view winners as select winner from matches;
create view losers as select loser from matches;
-- create players_win_count view
create view players_win_count as select players.id as player_id, count(matches.winner) as wins_count from players left join matches on players.id = matches.winner group by players.id order by player_id;

-- create players_match_count view
create view players_match_count as select p.player, count(p.player) from (select matches.winner as player from matches union all select matches.loser as player from matches) as p group by p.player;

-- id, name, wins, matches
create view players_standings as select players.id, players.name, coalesce(p.wins_count,0) as wins_count, coalesce(p.matches_count,0) as matches_count from players left join (select players_match_count.player, players_match_count.count as matches_count, players_win_count.wins_count from players_match_count, players_win_count where players_match_count.player = players_win_count.player_id) as p on players.id = p.player order by wins_count desc;

