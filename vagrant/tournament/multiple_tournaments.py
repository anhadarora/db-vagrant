#!/usr/bin/env python
#
# multiple_tournaments.py -- manages Swiss-system tournaments
#

import random
import psycopg2


def connect(dbname='tournament'):
    """Connect to the PostgreSQL database.  Returns a database connection."""

    try:
        db = psycopg2.connect("dbname=%s" % dbname)
        cursor = db.cursor()
        return db, cursor
    except:
        raise IOError('Error connecting to database %s' % dbname)


def deleteMatches(tournament=None):
    """Remove all the match records from a particular tournament."""

    db, cursor = connect()

    if tournament != None:
        cursor.execute(
            "delete from matches where tournament=%s;", (tournament,))
    else:
        cursor.execute("delete from matches")
    db.commit()
    db.close()
    return 'deleted all match records from database'


def deletePlayers(tournament=None):
    """Remove all the player records from a particular tournament."""
    db, cursor = connect()

    if tournament != None:
        cursor.execute(
            "delete from players where tournament=%s;", (tournament,))
    else:
        cursor.execute("delete from players")
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


def deleteTournaments(tournament=None):
    """Remove a the tournament record from the database."""

    db, cursor = connect()

    if tournament != None:
        cursor.execute(
            "delete from tournaments where tournament=%s;", (tournament,))
    else:
        cursor.execute("delete from tournaments")
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

    matches = []

    results = playerStandings(tournament)

    # If number of players is odd, must give a 'bye' to one player.
    # A player should not receive more than one 'bye' in a tournament.
    # A bye counts as a free win.
    if len(results) % 2 == 0:
        matches = setMatchesPairs(results, tournament)
    else:
        # randomly select a bye winner from bottom half
        # can't be someone who's won a bye before
        bottom_half = [result for result in results[:len(results)/2]]
        bye_winner = random.choice(bottom_half)
        # check if player has not received a bye
        # if player has a bye (bye_winner[bye] is True), pick another
        while (bye_winner[5] != None):
            bye_winner = random.choice(bottom_half)

        # record bye given
        updatePlayerBye(str(bye_winner[0]), True)

        # exclude from list bye'd player
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
        cursor.execute(
            "update players set bye=True where id=%s", (str(id),))
        db.commit()
    db.close()

    return


def setMatchesPairs(results, tournament):
    # results: id, tournament, name, wins_count, matches_count, bye

    matches = []
    players = []
    # matches_not_allowed are past matches, so no rematches
    matches_not_allowed = []

    # get past matches
    past_matches = getPastMatchesTournament(tournament)

    def resetMatchMaking():

        del matches[:]
        del players[:]
        del matches_not_allowed[:]

        # past_matches: id, winner, loser, tournament
        for match in past_matches:
            matches_not_allowed.append((match[1], match[2]))

        # players: (id, name)
        for player in results:
            players.append((player[0], player[2]))

    resetMatchMaking()

    i = 1
    # If the last pair match is not allowed, reset all matchmaking and
    # reorder players[-j] and players[-j-1] positions for a next matchmaking try.
    # Incrementing [-j] allows for more than one reorder, moving up the list.
    j = 2
    matches_set = False
    while not matches_set:

        # If there are only 2 players in list and
        # the first match (players[0], players[i]) was not allowed (i == 1),
        # then last match is not allowed and matchmaking must reset
        if (len(players) == 2) and (i == 2):
            # resets lists
            resetMatchMaking()
            # reorder a pair of positions for a new matchmaking try
            x = players[-j]
            players[-j] = players[-j-1]
            players[-j-1] = x
            j += 1
            i = 1

        # if list of players is empty, all players have been assigned a match
        if len(players) == 0:
            matches_set = True

        else:
            # make match
            match = (players[0], players[i])
            # only players ids, for formatting
            match_ids = (players[0][0], players[i][0])
            # reversed order also, to check if match not in past matches
            rev_match = (match_ids[1], match_ids[0])

            # if the match has happened before it is not allowed
            if (match_ids in matches_not_allowed) or (rev_match in matches_not_allowed):
                i += 1

            # else, match is allowed
            else:
                # add match to list of matches
                matches.append(match)
                # remove players from list to pair in match
                del players[0]
                # -1 because just deleted 1
                del players[i-1]
                # restart match making
                i = 1

    # MUST RETURN TUPLES (ID, NAME, ID, NAME) FOR MATCHES
    formatted_matches = []
    for match in matches:
        formatted_matches.append(
            (match[0][0], match[0][1], match[1][0], match[1][1]))

    return formatted_matches


def getPastMatchesTournament(tournament):
    # get past matches
    db, cursor = connect()
    cursor.execute(
        "select * from matches where tournament=%s;", (tournament,))
    past_matches = cursor.fetchall()
    db.close()

    return past_matches
