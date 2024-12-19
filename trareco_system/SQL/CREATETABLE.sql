DROP TABLE IF EXISTS tourist_area;
CREATE TABLE tourist_area (
	tourist_id serial,
	path TEXT,
	area_name TEXT,
	longitude numeric(9,6),
	latitude numeric(9,6),
	season_id integer,
	timezone_id integer,
	category_id integer,
	crowding numeric,
	weather integer
	);

DROP TABLE IF EXISTS colorhistgram;
CREATE TABLE colorhistgram (
	tourist_id serial,
	red integer,
	orange integer,
	yellow integer,
	green integer,
	blue integer,
	indigo integer,
	purple integer,
	black integer,
	gray integer,
	white integer
	);
	
DROP TABLE IF EXISTS season;
CREATE TABLE season (
	season_id integer,
	season TEXT
	);

DROP TABLE IF EXISTS timezone;
CREATE TABLE timezone (
	timezone_id integer,
	timezone TEXT
	);
	
DROP TABLE IF EXISTS category;
CREATE TABLE category (
	category_id integer,
	category TEXT
	);

DROP TABLE IF EXISTS weather;
CREATE TABLE weather (
    weather_id	INT,
    weather	TEXT
);

DROP TABLE IF EXISTS color2imp;
CREATE TABLE color2imp (
	imp_id serial,
	imp_name TEXT,
	red integer,
	orange integer,
	yellow integer,
	green integer,
	blue integer,
	indigo integer,
	purple integer,
	black integer,
	gray integer,
	white integer
	);
	
DROP TABLE IF EXISTS imp_weight;
CREATE TABLE imp_weight (
	weight_id serial,
	season_spring real,
	season_summer real,
	season_fall real,
	season_winter real,
	time_morning2noon real,
	time_night real,
	category_mountain real,
	category_hotspring real,
	category_temple real
	);
	
	
DROP TABLE IF EXISTS return_tourist_area;
CREATE TABLE return_tourist_area (
	r_tourist_id serial,
	r_path TEXT,
	r_area_name TEXT,
	r_longitude numeric(9,6),
	r_latitude numeric(9,6),
	r_season_id integer,
	r_timezone_id integer,
	r_category_id integer,
	r_crowding numeric,
	r_weather_id integer
	);

DROP TABLE IF EXISTS return_colorhistgram;
CREATE TABLE return_colorhistgram (
	r_tourist_id serial,
	r_red integer,
	r_orange integer,
	r_yellow integer,
	r_green integer,
	r_blue integer,
	r_indigo integer,
	r_purple integer,
	r_black integer,
	r_gray integer,
	r_white integer
	);