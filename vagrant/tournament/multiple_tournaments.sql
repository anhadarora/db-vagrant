\i tournament.sql

CREATE TABLE tournaments(
	id serial primary key,
	name text,
	winner int references players(id)
);

-- CREATE TABLE tournament_players(
-- 	tournament int references tournaments(id),
-- 	player int references players(id)
-- );

-- to keep track of which tournament a match belongs to
ALTER TABLE players ADD tournament int references tournaments(id);
-- to keep track if user has received a bye
ALTER TABLE players ADD bye boolean;
-- to keep track of which tournament a match belongs to
ALTER TABLE matches ADD tournament int references tournaments(id);

-- tournament, id, name, wins, matches, bye
DROP VIEW players_standings;
create view players_standings as select players.id, players.tournament, players.name, coalesce(p.wins_count,0) as wins_count, coalesce(p.matches_count,0) as matches_count, players.bye from players left join (select players_match_count.player, players_match_count.count as matches_count, players_win_count.wins_count from players_match_count, players_win_count where players_match_count.player = players_win_count.player_id) as p on players.id = p.player order by wins_count desc;
