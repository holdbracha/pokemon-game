
use pokemon;





-- delete from pokemon_owner; 
-- delete from pokemon_type;
-- delete from owner;
-- delete from types;
-- delete from city;
-- delete from pokemon;

drop table pokemon_owner;
-- drop table pokemon_type;
drop table owner;
-- drop table types;
drop table city;
drop table pokemon;





create table city(
    id int NOT NULL auto_increment PRIMARY KEY,
    name VARCHAR(20)
);

create table owner(
    id int NOT NULL auto_increment PRIMARY KEY,
    name VARCHAR(20),
    city_id int,
    FOREIGN KEY(city_id) REFERENCES city(id)
);

create table pokemon(
    id int NOT NULL auto_increment PRIMARY KEY,
    name VARCHAR(50),
    height int,
    weight int
);

create table types(
    id int NOT NULL PRIMARY KEY,
    type VARCHAR(20)
);

create table pokemon_type(
    id int NOT NULL auto_increment PRIMARY KEY,
    type_id int,
    pokemon_id int,
    FOREIGN KEY(type_id) REFERENCES types(id),
    FOREIGN KEY(pokemon_id) REFERENCES pokemon(id)
);

create table pokemon_owner(
    pokemon_id int,
    owner_id int ,
    FOREIGN KEY(pokemon_id) REFERENCES pokemon_type(id),
    FOREIGN KEY(owner_id) REFERENCES owner(id)
);
