CREATE TABLE Account (
            id integer primary key autoincrement,username varchar(255) unique,password varchar(255),name varchar(255),is_active tinyint not null default True,created datetime not null default '<built-in method now of type object at 0x00007FFF00F18990>'
        );
CREATE TABLE sqlite_sequence(name,seq);
CREATE TABLE Librarian (
            id integer primary key autoincrement,account_id integer unique,foreign key(account_id) references Account(id)
        );
CREATE TABLE Book (
            id integer primary key autoincrement,title varchar(255),author varchar(255),isbn varchar(255),publish_date date,created datetime not null default '<built-in method now of type object at 0x00007FFF00F18990>'
        );
CREATE TABLE Borrow (
            id integer primary key autoincrement,account_id varchar(255),book_id varchar(255),borrow_time datetime not null default '<built-in method now of type object at 0x00007FFF00F18990>',return_time datetime
        );
