#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#


##################### IMPORTS #####################
import psycopg2
from contextlib import contextmanager
###################################################


def connect():
    """Connects to the Postgres database, Returns a database connection"""
    return psycopg2.connect("dbname=tournament")

@contextmanager
def get_cursor():
    """Helper function that takes care of the db connection and cursor"""
    db = connect()
    cursor = db.cursor()
    yield cursor
    db.commit()
    cursor.close()
    db.close()

def deleteMatches():
    """Removes all the match records from the database"""
    with get_cursor() as cursor:
        cursor.execute("delete from match_results;")

def deletePlayers():
    """Removes all the player records from the database"""
    with get_cursor() as cursor:
        cursor.execute("delete from player_info;")

def countPlayers():
    """Returns the number of players currently registered"""
    with get_cursor() as cursor:
        cursor.execute("select count(id) as num_of_players from player_info;")
        num_of_players = cursor.fetchall()
    return num_of_players[0][0]

def registerPlayer(name):
    """Adds a player to the tournament database."""
    with get_cursor() as cursor:
        cursor.execute('insert into player_info (name, wins, matches) values (%s, 0, 0)', (name,))

def playerStandings():
    """Returns a list of the players and their win records, sorted by wins"""
    with get_cursor() as cursor:
        cursor.execute("select id, name, wins, matches from player_info order by wins desc;")
        standings = cursor.fetchall()
    return standings

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players"""
    with get_cursor() as cursor:
        cursor.execute("update player_info set wins = (wins + 1) where id = %s;", (winner,))
        cursor.execute("update player_info set matches = (matches + 1) where id = %s or id = %s;", (winner, loser,))
        cursor.execute("insert into match_results (winner_id, loser_id) values (%s, %s);", (winner, loser,))

def swissPairings():
    """
    Returns a list of pairs of players for the next round of a match.
    0 index of a standings tuple refers to id, 1 refers to name
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    standings = playerStandings()
    pairings = []
    player_1_index = 0
    player_2_index = 1
    while player_2_index < len(standings):
        pairings.append((standings[player_1_index][0], standings[player_1_index][1], 
            standings[player_2_index][0], standings[player_2_index][1],))
        player_1_index += 2
        player_2_index += 2
    return pairings

