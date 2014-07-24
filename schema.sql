drop table if exists labels;
create table labels (
    id integer primary key autoincrement,
    imgname text not null,
    imgpath text not null,
    value text
);
