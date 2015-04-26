#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    """Assumes the database has already been created: see tournament.sql"""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    DB = connect()
    c = DB.cursor()
    c.execute("DELETE FROM matches *")
    DB.commit()
    c.close()
    DB.close()
    return

def deletePlayers():
    """Remove all the player records from the database."""
    DB = connect()
    c = DB.cursor()
    c.execute("DELETE FROM players *")
    DB.commit()
    c.close()
    DB.close()
    return

def countPlayers():
    """Returns the number of players currently registered."""
    DB = connect()
    c = DB.cursor()
    c.execute("SELECT count(*) FROM players")
    num_registered_players = c.fetchone()[0]
    c.close()
    DB.close()
    return num_registered_players

def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    DB = connect()
    c = DB.cursor()
    c.execute("INSERT INTO players(name) VALUES (%s)", (name,))
    DB.commit()
    c.close()
    DB.close()
    return

def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played

    Assumes creation of views for
    winners, to give count of wins for each player...
        id: players.id
        name: players.name
        wins: count of where players.id=matches.winner_id
    and for
    match_summary to give count of matches for each player...
        id: players.id
        name: players.name
        matches: count of where players.id=matches.winner_id or =matches.loser_id
    """
    DB = connect()
    c = DB.cursor()
    """List all players"""
    c.execute("""SELECT winners.id,
                        winners.name,
                        winners.wins,
                        match_summary.matches
                 FROM winners, match_summary
                 WHERE winners.id=match_summary.id
                 ORDER BY winners.wins DESC, winners.id;""")
    """Write list of tuples for return"""
    standings = c.fetchall()
    c.close()
    DB.close()
    return standings


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    DB = connect()
    c = DB.cursor()
    c.execute("INSERT INTO matches (winner_id, loser_id) VALUES (%s, %s)", (winner, loser,))
    DB.commit()
    c.close()
    DB.close()
    return
 
 
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
    standings = playerStandings()
    pairings = []  
    for i in range(1,len(standings),2):
        first_id = standings[i-1][0]
        first_name = standings[i-1][1]
        second_id = standings[i][0]
        second_name = standings[i][1]
        pairings.append((first_id,first_name,second_id,second_name))    
    return pairings
