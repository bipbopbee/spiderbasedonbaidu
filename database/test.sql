create DATABASE videoright;
use videoright;
create table `user` (
    `userid` int (11) NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `username` varchar (150) NOT NULL,
    `userpassword` varchar (150) NOT NULL,
    `email` varchar (150) NOT NULL,
    `apitoken` varchar (150) NOT NULL,
    `role` varchar (11) NOT NULL
);
create table `right` (
    `rightid` int (11) NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `rightname` varchar (150) NOT NULL,
    `publishers` varchar (150) NOT NULL,
    `url` varchar (150) NOT NULL,
    `email` varchar (150) NOT NULL,
    `contentid` int (11) NOT NULL
);
create table `privacy` (
    `privacyid` int (11) NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `url` varchar (150) NOT NULL,
    `rightname` varchar (150) NOT NULL,
    `contentid` int (11) NOT NULL
);
insert into privacy (privacyid, url, rightname, contentid)  values (NULL, 'www.baidu.com','神奇', 22);