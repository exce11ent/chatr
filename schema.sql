drop table if exists users;
create table users (
  id integer primary key autoincrement,
  username text not null,
  password text not null
);

drop table if exists messages;
create table messages (
  id integer primary key autoincrement,
  sender integer not null,
  receiver integer not null,
  Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
  text text not null
);