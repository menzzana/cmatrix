/* Table creation */
CREATE TABLE user (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	username VARCHAR(45) UNIQUE NOT NULL,
	full_name VARCHAR(45)  NOT NULL,
    salt VARCHAR(6) UNIQUE,
	password VARCHAR(45)  NOT NULL,
	session_id VARCHAR(45),
	session_time VARCHAR(20)
	);
CREATE TABLE category (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	name VARCHAR(255) UNIQUE  NOT NULL,
	vr_code VARCHAR(5) UNIQUE
	);
CREATE TABLE competence_scale (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	name VARCHAR(255) UNIQUE  NOT NULL
	);
CREATE TABLE competence (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	category_id INTEGER  NOT NULL,
	name VARCHAR(255) UNIQUE  NOT NULL
	);
CREATE TABLE user_competence (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER  NOT NULL,
    competence_id INTEGER  NOT NULL,
    scale_id INTEGER  NOT NULL
	);

/* Views */
CREATE VIEW cmatrix AS
	SELECT user_competence.id AS id,username,full_name,category.name AS category,
	competence.id AS competence_id,competence.name AS competence,user_competence.scale_id
	FROM competence,category,user
	LEFT JOIN user_competence 
	ON competence.id=user_competence.competence_id
	AND user.id=user_competence.user_id
	WHERE competence.category_id=category.id;

/* Inserts */
INSERT INTO competence_scale(id,name) values(0,'Unknown');
INSERT INTO competence_scale(id,name) values(1,'No experience');
INSERT INTO competence_scale(id,name) values(2,'No experience but want to learn');
INSERT INTO competence_scale(id,name) values(3,'Worked with but with limited competence');
INSERT INTO competence_scale(id,name) values(4,'Experienced but need to learn more');
INSERT INTO competence_scale(id,name) values(5,'Professional experience');
INSERT INTO category(name) values('Programming language');
INSERT INTO category(name) values('Software');
INSERT INTO category(name,vr_code) VALUES
	('Scientific area','0');
INSERT INTO category(name,vr_code) VALUES
	('Natural sciences','10');
INSERT INTO category(name,vr_code) VALUES
	('Mathematic','101');
INSERT INTO category(name,vr_code) VALUES
	('Data- and information science)','102');
INSERT INTO category(name,vr_code) VALUES
	('Physics','103');
INSERT INTO category(name,vr_code) VALUES
	('Chemistry','104');
INSERT INTO category(name,vr_code) VALUES
	('Geosciences','105');
INSERT INTO category(name,vr_code) VALUES
	('Biological sciences','106');
INSERT INTO category(name,vr_code) VALUES
	('Technological science','20');
INSERT INTO category(name,vr_code) VALUES
	('Electrotechnological science and electronics','202');
INSERT INTO category(name,vr_code) VALUES
	('Mechanical science','203');
INSERT INTO category(name,vr_code) VALUES
	('Technological chemistry','204');
INSERT INTO category(name,vr_code) VALUES
	('Material science','205');
INSERT INTO category(name,vr_code) VALUES
	('Medical technology','206');
INSERT INTO category(name,vr_code) VALUES
	('Natural resources technology','207');
INSERT INTO category(name,vr_code) VALUES
	('Environmental biotechnology','208');
INSERT INTO category(name,vr_code) VALUES
	('Industrial biotechnology','209');
INSERT INTO category(name,vr_code) VALUES
	('Nanotechnology','210');
INSERT INTO category(name,vr_code) VALUES
	('Other technology','211');
INSERT INTO category(name,vr_code) VALUES
	('Medical science','30');
INSERT INTO category(name,vr_code) VALUES
	('Cinical medicine','302');
INSERT INTO category(name,vr_code) VALUES
	('Health science','303');
INSERT INTO category(name,vr_code) VALUES
	('Medical biotechnology','304');
INSERT INTO category(name,vr_code) VALUES
	('Agricultural science','40');
INSERT INTO category(name,vr_code) VALUES
	('Agricultural science forestry and fishing','401');
INSERT INTO category(name,vr_code) VALUES
	('Animal science','402');
INSERT INTO category(name,vr_code) VALUES
	('Veterinary science','403');
INSERT INTO category(name,vr_code) VALUES
	('Social science','50');
INSERT INTO category(name,vr_code) VALUES
	('Psychoology','501');
INSERT INTO category(name,vr_code) VALUES
	('Economics','502');
INSERT INTO category(name,vr_code) VALUES
	('Educational science','503');
INSERT INTO category(name,vr_code) VALUES
	('Sociology','504');
INSERT INTO category(name,vr_code) VALUES
	('Law','505');
INSERT INTO category(name,vr_code) VALUES
	('Political science','506');
INSERT INTO category(name,vr_code) VALUES
	('Social and economic geography','507');
INSERT INTO category(name,vr_code) VALUES
	('Communikation science','508');
INSERT INTO category(name,vr_code) VALUES
	('Humanities','60');
INSERT INTO category(name,vr_code) VALUES
	('Philosophical ethics and religion','603');
INSERT INTO category(name,vr_code) VALUES
	('Art','604');

