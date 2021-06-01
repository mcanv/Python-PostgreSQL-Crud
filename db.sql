create table users(
	user_id serial primary key,
	user_name varchar(50) not null,
	user_group int not null
);

create table user_groups(
	group_id serial primary key,
	group_name varchar(100) not null
);
