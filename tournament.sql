/* creates tables for the tournament and connects to the database */

DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament

create table player_info ( id serial primary key,
                           name text,   
                           wins integer,
                           matches integer );

create table match_results ( match_id serial primary key,
                             winner_id integer references player_info(id),
                             loser_id integer references player_info(id) );
