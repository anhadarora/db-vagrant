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
    cursor.execute(
        "select count(id) from players where tournament=%s;", (tournament,))
    results = cursor.fetchone()
    db.close()
    return results[0]


def deleteTournaments():
    """Remove all the tournament records from the database."""

    db, cursor = connect()
    cursor.execute(
        "delete from tournaments where tournament=%s;", (tournament,))
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
    cursor.execute(
        "insert into players (name, tournament) values (%s, %s)", (name, tournament))
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
    cursor.execute(
        "select * from players_standings where tournament=(%s)", (tournament,))
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

    If there are an odd number of players, randomly select one that has not
    received a bye yet. Return only the 8 players in round, in 4 pairs.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    db, cursor = connect()
    cursor.execute(
        "select * from players_standings where tournament=%s;", (tournament,))
    results = cursor.fetchall()
    db.close()

    # If number of players is odd, must give a 'bye' to one player.
    # A player should not receive more than one 'bye' in a tournament.
    # A bye counts as a free win.
    matches = []
    if len(results) % 2 == 0:
        matches = setMatchesPairs(results, tournament)
        # while (count < len(results)):
        #     matches.append(
        #         # result[][0] is id
        #         # result[][2] is name
        #         (results[count][0], results[count][2],
        #          results[count+1][0], results[count+1][2]))
        #     count = count + 2
    else:
        # need to calculate the top half
        # randomly select a winner from bottom half
        # can't be someone who's won a bye before
        print "ODD NUMBER OF PLAYERS. WILL RANDOM SELECT ONE FROM BOTTOM HALF."

        bottom_half = [result for result in results[:len(results)/2]]
        bye_winner = random.choice(bottom_half)
        # check if player has not received a bye
        # if player has a bye (bye_winner[bye] is false), pick another
        while (bye_winner[5] != None):
            bye_winner = random.choice(bottom_half)

        # insert bye record for player
        updatePlayerBye(str(bye_winner[0]), True)
        # db, cursor = connect()
        # cursor.execute(
        #     "update players set bye=True where id=%s", (str(bye_winner[0]),))
        # db.commit()
        # db.close()

        # exclude from list bye'd player
        print "BYE WINNER: %s" % str(bye_winner[0])
        remaining_players = []
        for player in results:
            if player[0] != bye_winner[0]:
                remaining_players.append(player)

        matches = setMatchesPairs(remaining_players, tournament)

    return matches


def updatePlayerBye(id, set=True):
    # insert bye record for player
    db, cursor = connect()
    if id and set == True:
        print 'giving player %s a bye.' % str(id)
        cursor.execute(
            "update players set bye=True where id=%s", (str(id),))
        db.commit()
        db.close()

    return


def setMatchesPairs(results, tournament):
    matches = []
    count = 0
    while (count < len(results)):
        # preventing rematches here
        # get past matches
        db, cursor = connect()
        cursor.execute(
            "select * from matches where tournament=%s;", (tournament,))
        past_matches = cursor.fetchall()
        db.close()

        # past_matches: id, winner, loser, tournament
        matches_not_allowed = []
        print 'PAST MATCHES'
        print past_matches
        for match in past_matches:
            matches_not_allowed.append((match[1], match[2]))
        print 'MATCHES NOT ALLOWED'
        print matches_not_allowed
        # need to reverse lists as well

        # results: id, tournament, name, wins_count, matches_count, bye
        # players: (id, name)
        players = []
        for player in results:
            players.append(player[0], player[2])

        print 'LEN PLAYERS'
        print len(players)
        print 'MATCHES'
        print matches

        i = 0
        while i < (len(players) - 1):
            match = (players[0], players[i+1])

            print 'MATCH'
            print match
            print 'MATCHES NOT ALLOWED'
            print matches_not_allowed

            rev_match = (match[1], match[0])

            print 'REV MATCH'
            print rev_match

            if (match not in matches_not_allowed) and (rev_match not in matches_not_allowed):
                print 'ALLOWED'
                i += 1
                # add valid match to list of matches
                matches.appent
                # remove players from list of picks
            else:
                print 'NOT ALLOWED, TRY ANOTHER'
                i += 1



        ### MUST RETURN TUPLES (ID, NAME, ID, NAME) FOR MATCHES

        matches.append(
            # result[][0] is id
            # result[][2] is name
            (results[count][0], results[count][2],
             results[count+1][0], results[count+1][2]))
        count=count + 2
    return matches

