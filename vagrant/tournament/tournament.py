#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect(dbname='tournament'):
    """Connect to the PostgreSQL database.  Returns a database connection."""

    try:
        db = psycopg2.connect("dbname=%s" % dbname)
        cursor = db.cursor()
        return db, cursor
    except:
        raise IOError('Error connecting to database %s' % dbname)


def deleteMatches():
    """Remove all the match records from the database."""

    db, cursor = connect()
    cursor.execute("delete from matches;")
    db.commit()
    db.close()
    return 'deleted all match records from database'


def deletePlayers():
    """Remove all the player records from the database."""
    db, cursor = connect()
    cursor.execute("delete from players;")
    db.commit()
    db.close()
    return 'deleted all player records from database'


def countPlayers():
    """Returns the number of players currently registered."""
    db, cursor = connect()
    cursor.execute("select count(id) from players;")
    results = cursor.fetchone()
    db.close()
    return results[0]


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    db, cursor = connect()
    cursor.execute("insert into players (name) values (%s)", (name,))
    db.commit()
    db.close()
    return '*** all player records deleted from database ***'


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    First entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    db, cursor = connect()
    cursor.execute("select * from players_standings;")
    results = cursor.fetchall()
    db.close()
    return results


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db, cursor = connect()
    cursor.execute(
        "insert into matches (winner, loser) values (%s,%s)", (winner, loser))
    db.commit()
    db.close()
    return '*** match recorded ***'


def swissPairings():
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
    cursor.execute("select * from players_standings;")
    results = cursor.fetchall()
    db.close()

    matches = []
    count = 0
    while (count < len(results)):
        matches.append(
            (results[count][0], results[count][1],
             results[count+1][0], results[count+1][1]))
        count = count + 2

    print matches
    return matches
