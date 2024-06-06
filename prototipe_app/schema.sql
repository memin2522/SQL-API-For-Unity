create table patient(
	id integer primary key auto_increment,
    registration varchar(50),
    firstName varchar(50) not null,
    lastName varchar(50) not null,
    dateOfBirth date not null,
    militaryStatus varchar(50) not null,
    militaryRank varchar(50)
);

