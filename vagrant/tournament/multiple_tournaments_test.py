#!/usr/bin/env python
#
# Test cases for tournament.py
# These tests are not exhaustive, but they should cover the majority of cases.
#
# If you do add any of the extra credit options, be sure to add/modify these test cases
# as appropriate to account for your module's added functionality.

from multiple_tournaments import *

DEFAULT_TOURNAMENT = 2
createTournament()
createTournament()


def testCount():
    """
    Test for initial player count,
             player count after 1 and 2 players registered,
             player count after players deleted.
    """
    deleteMatches(DEFAULT_TOURNAMENT)
    deletePlayers(DEFAULT_TOURNAMENT)
    c = countPlayers(DEFAULT_TOURNAMENT)
    if c == '0':
        raise TypeError(
            "countPlayers should return numeric zero, not string '0'.")
    if c != 0:
        raise ValueError("After deletion, countPlayers should return zero.")
    print "1. countPlayers() returns 0 after initial deletePlayers() execution."

    registerPlayer("Chandra Nalaar", DEFAULT_TOURNAMENT)
    c = countPlayers(DEFAULT_TOURNAMENT)
    if c != 1:
        raise ValueError(
            "After one player registers, countPlayers() should be 1. Got {c}".format(c=c))
    print "2. countPlayers() returns 1 after one player is registered."
    registerPlayer("Jace Beleren", DEFAULT_TOURNAMENT)
    c = countPlayers(DEFAULT_TOURNAMENT)
    if c != 2:
        raise ValueError(
            "After two players register, countPlayers() should be 2. Got {c}".format(c=c))
    print "3. countPlayers() returns 2 after two players are registered."
    deletePlayers(DEFAULT_TOURNAMENT)
    c = countPlayers(DEFAULT_TOURNAMENT)
    if c != 0:
        raise ValueError(
            "After deletion, countPlayers should return zero.")
    print "4. countPlayers() returns zero after registered players are deleted.\n5. Player records successfully deleted."

def testStandingsBeforeMatches(tournament=DEFAULT_TOURNAMENT):
    """
    Test to ensure players are properly represented in standings prior
    to any matches being reported.
    """
    deleteMatches(DEFAULT_TOURNAMENT)
    deletePlayers(DEFAULT_TOURNAMENT)
    registerPlayer("Melpomene Murray", tournament)
    registerPlayer("Randy Schwartz", tournament)
    # playerstandings(tournament)
    standings = playerStandings(tournament)
    if len(standings) < 2:
        raise ValueError("Players should appear in playerStandings even before "
                         "they have played any matches.")
    elif len(standings) > 2:
        raise ValueError("Only registered players should appear in standings.")
    # if len(standings[0]) != 4:
    #     raise ValueError("Each playerStandings row should have four columns.")
    if len(standings[0]) != 5:
        raise ValueError("Each playerStandings row should have five columns.")
    [(tournament, id1, name1, wins1, matches1), (tournament, id2, name2, wins2, matches2)] = standings
    if matches1 != 0 or matches2 != 0 or wins1 != 0 or wins2 != 0:
        raise ValueError(
            "Newly registered players should have no matches or wins.")
    if set([name1, name2]) != set(["Melpomene Murray", "Randy Schwartz"]):
        raise ValueError("Registered players' names should appear in standings, "
                         "even if they have no matches played.")
    print "6. Newly registered players appear in the standings with no matches."

def testReportMatches(tournament=DEFAULT_TOURNAMENT):
    """
    Test that matches are reported properly.
    Test to confirm matches are deleted properly.
    """
    deleteMatches(tournament)
    deletePlayers(tournament)
    registerPlayer("Bruno Walton", tournament)
    registerPlayer("Boots O'Neal", tournament)
    registerPlayer("Cathy Burton", tournament)
    registerPlayer("Diane Grant", tournament)
    standings = playerStandings(tournament)
    [id1, id2, id3, id4] = [row[1] for row in standings]
    reportMatch(id1, id2, tournament)
    reportMatch(id3, id4, tournament)
    standings = playerStandings(tournament)
    for (t, i, n, w, m) in standings:
        if m != 1:
            raise ValueError("Each player should have one match recorded.")
        if i in (id1, id3) and w != 1:
            raise ValueError("Each match winner should have one win recorded.")
        elif i in (id2, id4) and w != 0:
            raise ValueError("Each match loser should have zero wins recorded.")
    print "7. After a match, players have updated standings."
    deleteMatches(tournament)
    standings = playerStandings(tournament)
    if len(standings) != 4:
        raise ValueError("Match deletion should not change number of players in standings.")
    for (t, i, n, w, m) in standings:
        if m != 0:
            raise ValueError("After deleting matches, players should have zero matches recorded.")
        if w != 0:
            raise ValueError("After deleting matches, players should have zero wins recorded.")
    print "8. After match deletion, player standings are properly reset.\n9. Matches are properly deleted."

def testPairings(tournament=DEFAULT_TOURNAMENT):
    """
    Test that pairings are generated properly both before and after match reporting.
    """
    deleteMatches(tournament)
    deletePlayers(tournament)
    registerPlayer("Twilight Sparkle", tournament)
    registerPlayer("Fluttershy", tournament)
    registerPlayer("Applejack", tournament)
    registerPlayer("Pinkie Pie", tournament)
    registerPlayer("Rarity", tournament)
    registerPlayer("Rainbow Dash", tournament)
    registerPlayer("Princess Celestia", tournament)
    registerPlayer("Princess Luna", tournament)
    standings = playerStandings(tournament)
    [id1, id2, id3, id4, id5, id6, id7, id8] = [row[1] for row in standings]
    pairings = swissPairings(tournament)
    if len(pairings) != 4:
        raise ValueError(
            "For eight players, swissPairings should return 4 pairs. Got {pairs}".format(pairs=len(pairings)))
    reportMatch(id1, id2, tournament)
    reportMatch(id3, id4, tournament)
    reportMatch(id5, id6, tournament)
    reportMatch(id7, id8, tournament)
    pairings = swissPairings(tournament)
    if len(pairings) != 4:
        raise ValueError(
            "For eight players, swissPairings should return 4 pairs. Got {pairs}".format(pairs=len(pairings)))
    [(pid1, pname1, pid2, pname2), (pid3, pname3, pid4, pname4), (pid5, pname5, pid6, pname6), (pid7, pname7, pid8, pname8)] = pairings
    possible_pairs = set([frozenset([id1, id3]), frozenset([id1, id5]),
                          frozenset([id1, id7]), frozenset([id3, id5]),
                          frozenset([id3, id7]), frozenset([id5, id7]),
                          frozenset([id2, id4]), frozenset([id2, id6]),
                          frozenset([id2, id8]), frozenset([id4, id6]),
                          frozenset([id4, id8]), frozenset([id6, id8])
                          ])
    actual_pairs = set([frozenset([pid1, pid2]), frozenset([pid3, pid4]), frozenset([pid5, pid6]), frozenset([pid7, pid8])])
    for pair in actual_pairs:
        if pair not in possible_pairs:
            raise ValueError(
                "After one match, players with one win should be paired.")
    print "10. After one match, players with one win are properly paired."


if __name__ == '__main__':
    testCount()
    testStandingsBeforeMatches()
    testReportMatches()
    testPairings()
    print "Success!  All tests pass!"
