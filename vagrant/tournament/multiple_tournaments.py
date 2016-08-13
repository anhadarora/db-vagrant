#!/usr/bin/env python
#
# multiple_tournaments.py -- manages Swiss-system tournaments
#

from tournament import *

def deleteTournaments():
    """Remove all the tournament records from the database."""

    db, cursor = connect()
    cursor.execute("delete from tournaments;")
    db.commit()
    db.close()
    return 'deleted all match records from database'


def createTournament(name='No Name'):
    """Creates a new tournament.

    Args:
      name: the tournament name
    """
    db, cursor = connect()
    cursor.execute("insert into tournaments (name) values (%s)", (name,))
    db.commit()
    db.close()
    return '*** created tournament ***'


def registerPlayer(name, tournament):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    db, cursor = connect()
    cursor.execute("insert into players (name, tournament) values (%s, %s)", (name, tournament))
    db.commit()
    db.close()
    return '*** all player records deleted from database ***'


def playerStandings(tournament):
    """Returns a list of the players and their win records, sorted by wins,
    	filtered by tournament.

    First entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie, in a specific tournament.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    db, cursor = connect()
    cursor.execute("select * from players_standings where tournament=(%s)", (tournament,))
    results = cursor.fetchall()
    db.close()
    return results


def swissPairings(tournament):
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    db, cursor = connect()
    cursor.execute("select * from players_standings where tournament=%s;", (tournament,))
    results = cursor.fetchall()
    db.close()

    matches = []
    count = 0
    while (count < len(results)):
        matches.append(
            (results[count][1], results[count][2],
             results[count+1][1], results[count+1][2]))
        count = count + 2

    print matches
    return matches

