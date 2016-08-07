drop table if exists entries;
create table entries (
	id integer primary key autoincrement,
	username text not null,
	password text not null,
	team text,
	hidden boolean
);

drop table if exists config;
create table config (
	id integer primary key check(id=0),
	contest_title text,
	contest_details text,
	link_to_login text,
	link_to_ranking text,
	closed boolean
);

insert into config values (0, '$contest_title', '$contest_details', '$link_to_login', '$link_to_ranking', 0);
