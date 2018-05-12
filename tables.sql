create table rooms (
	id serial primary key,
	name char(50),
	hashpw char(100)
);

create table users (
	id serial primary key,
	rid int,
	name char(50),
	ip char(15),
	port int
);
