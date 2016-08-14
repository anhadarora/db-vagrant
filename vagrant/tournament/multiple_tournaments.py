#!/usr/bin/env python
#
# multiple_tournaments.py -- manages Swiss-system tournaments
#

from tournament import *
import random

def deleteMatches(tournament):
    """Remove all the match records from a particular tournament."""

    db, cursor = connect()
    cursor.execute("delete from matches where tournament=%s;", (tournament,))
    db.commit()
    db.close()
    return 'deleted all match records from database'


def deletePlayers(tournament):
    """Remove all the player records from a particular tournament."""
    db, cursor = connect()
    cursor.execute("delete from players where tournament=%s;", (tournament,))
    db.commit()
    db.close()
    return 'deleted all player records from database'


def countPlayers(tournament):
    """Returns the number of players currently registered in a tournament."""
    db, cursor = connect()
    cursor.execute("select count(id) from players where tournament=%s;", (tournament,))
    results = cursor.fetchone()
    db.close()
    return results[0]

def deleteTournaments():
    """Remove all the tournament records from the database."""

    db, cursor = connect()
    cursor.execute("delete from tournaments where tournament=%s;", (tournament,))
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
    """Adds a player a tournament.

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

def reportMatch(winner, loser, tournament):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
      tournament: the id of the tournament this match belongs to
    """
    db, cursor = connect()
    cursor.execute(
        "insert into matches (winner, loser, tournament) values (%s, %s, %s)", (winner, loser, tournament))
    db.commit()
    db.close()
    return '*** match recorded ***'


def playerStandings(tournament):
    """Returns a list of the players and their win records, sorted by wins,
    	filtered by tournament.

    First entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie, in a specific tournament.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        tournament: the id of the tournament
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
    """Returns a list of pairs of players for the next round of a match
    in a particular tournament.

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

    print "AQUI"
    print len(results)

    matches = []
    count = 0

    # If number of players is odd, must give a 'bye' to one player.
    # A player should not receive more than one 'bye' in a tournament.
    # A bye counts as a free win.
    if len(results) % 2 == 0:
        while (count < len(results)):
            matches.append(
                # result[][0] is id
                # result[][2] is name
                (results[count][0], results[count][2],
                 results[count+1][0], results[count+1][2]))
            count = count + 2
    else:
        # need to calculate the top half
        # randomly select a winner from bottom half
        # can't be someone who's won a bye before
        print "ODD NUMBER OF PLAYERS. WILL RANDOM SELECT ONE FROM BOTTOM HALF."

        bottom_half = [result for result in results[:len(results)/2]]
        bye_winner = random.choice(bottom_half)
        # check if player has not received a bye
        # if it has received a bye, pick another player

        print "BYES"
        print bye_winner
        print bye_winner[5]

        # if player has a bye, pick another
        while (bye_winner[5] != None):
             bye_winner = random.choice(bottom_half)

        #insert bye record for player
        db, cursor = connect()
        cursor.execute(
            "update players set bye=True where id=%s", (str(bye_winner[0]),))
        db.commit()
        db.close()

        # set up matches, excluding bye'd player

        # exclude from list bye'd player
        # same sorting as above line 143

        matches = ['I', 'DON\'T', 'KNOW']
        print "PLAYERS and WINS"
        for player in results:
            print player
        #ord


    return matches

