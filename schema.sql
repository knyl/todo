drop table if exists todolist;
create table todolist (
  id integer primary key,
  title text not null,
  prio integer not null,
  done boolean not null
);
