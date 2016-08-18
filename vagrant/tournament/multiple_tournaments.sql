-- Table definitions for the tournament project.

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

CREATE TABLE tournaments(
	id serial primary key,
	name text,
	winner int references players(id)
);

-- matches ids, winner, loser
create view matches_ids as select matches.id, matches.winner as winner, matches.loser as loser from matches, players where matches.winner = players.id or matches.loser = players.id group by matches.id order by matches.id;
-- winners/losers ids view
create view winners as select winner from matches;
create view losers as select loser from matches;
-- create players_win_count view
create view players_win_count as select players.id as player_id, count(matches.winner) as wins_count from players left join matches on players.id = matches.winner group by players.id order by player_id;
-- create players_match_count view
create view players_match_count as select p.player, count(p.player) from (select matches.winner as player from matches union all select matches.loser as player from matches) as p group by p.player;

-- to keep track of which tournament a match belongs to
ALTER TABLE players ADD tournament int references tournaments(id);
-- to keep track if user has received a bye
ALTER TABLE players ADD bye boolean;
-- to keep track of which tournament a match belongs to
ALTER TABLE matches ADD tournament int references tournaments(id);

-- tournament, id, name, wins, matches, bye
create view players_standings as select players.id, players.tournament, players.name, coalesce(p.wins_count,0) as wins_count, coalesce(p.matches_count,0) as matches_count, players.bye from players left join (select players_match_count.player, players_match_count.count as matches_count, players_win_count.wins_count from players_match_count, players_win_count where players_match_count.player = players_win_count.player_id) as p on players.id = p.player order by wins_count desc;
