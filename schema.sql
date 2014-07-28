drop table if exists attributes;
create table attributes (
    id integer primary key autoincrement,
    imgname text not null,
    imgpath text not null,
    value text
);
create table regions (
    id integer primary key autoincrement,
    imgname text not null,
    imgpath text not null,
    value text
)
