--
-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.
--

-- 
-- Setup database before running code:
--    At the ubuntu shell prompt, change to the right directory "cd /vagrant/tournament"
--    Enter "psql"
--    Create the database "tournament" by using "create database tournament;" in psql
--    Then use "\i tournament.sql;" to import this file into psql
--    The quit psql "\q" to return to ubuntu prompt
--

--
-- Clear previous versions of tables and views
--
DROP VIEW IF EXISTS winners;
DROP VIEW IF EXISTS match_summary;
DROP TABLE IF EXISTS players;
DROP TABLE IF EXISTS matches;

--
-- Create the table "players"
--
CREATE TABLE players (
	id SERIAL PRIMARY KEY, 
	name TEXT);

--
-- Create the table "matches"
-- Assume SERIAL can be written to INT
--
CREATE TABLE matches (
	id SERIAL PRIMARY KEY, 
	winner_id INT, 
	loser_id INT);

--
-- Create a view for "winners" for num. wins for each player
--
CREATE VIEW winners AS
	SELECT players.id, players.name, COUNT(matches.id) AS wins
	FROM players LEFT JOIN matches
	ON players.id=matches.winner_id
	GROUP BY players.id, players.name
	ORDER BY players.id;

--
-- Create a view for "match_summary" for num. matches for each player
--
CREATE VIEW match_summary AS
	SELECT players.id, players.name, COUNT(matches.id) AS matches
	FROM players LEFT JOIN matches
	ON players.id=matches.winner_id OR players.id=matches.loser_id
	GROUP BY players.id, players.name
	ORDER BY players.id;

\d;

--
-- Create the table "tournament_names"
--
-- CREATE TABLE tournament_names (
--	id SERIAL PRIMARY KEY,
--	name TEXT);

--
-- To start anew, use "dropdb tournament" in psql
--