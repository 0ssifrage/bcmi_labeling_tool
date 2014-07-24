drop table if exists images;
create table images (
    id integer primary key autoincrement,
    imgname text not null,
    imgpath text not null,
    value text
);
