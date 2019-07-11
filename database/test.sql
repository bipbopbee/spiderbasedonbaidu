create DATABASE videoright DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
use videoright;
create table `user` (
    `userid` int (11) NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `username` varchar (150) NOT NULL,
    `userpassword` varchar (150) NOT NULL,
    `email` varchar (150) NOT NULL,
    `apitoken` varchar (150) NOT NULL,
    `role` varchar (11) NOT NULL
) DEFAULT CHARSET=utf8;
create table `right`(
    `rightid` int (11) NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `rightname` varchar (150) NOT NULL,
    `url` varchar (150) NOT NULL,
    `email` varchar (150) NOT NULL,
    `contentid` int (11) NOT NULL
) DEFAULT CHARSET=utf8;
create table `right_tmp`  (
    `rightid` int (11) NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `rightname` varchar (150) NOT NULL,
    `url` varchar (150) NOT NULL,
    `email` varchar (150) NOT NULL,
    `contentid` int (11) NOT NULL
) DEFAULT CHARSET=utf8;;
create table `privacy` (
    `privacyid` int (11) NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `url` varchar (150) NOT NULL,
    `rightname` varchar (150) NOT NULL,
    `contentid` int (11) NOT NULL
)DEFAULT CHARSET=utf8;
insert into privacy (privacyid, url, rightname, contentid)  values (NULL, 'www.baidu.com','神奇', 22);
insert into user (userid, username, userpassword, email, apitoken, role)  values (NULL, 'abc','abc', '516854715@qq.com', 'LWtrKgMmLIeAWyyDUlLa', 'basic');
insert into user (userid, username, userpassword, email, apitoken, role)  values (NULL, 'tom','abc', '123456@qq.com', 'LWtrKgMmLIeAWyyDUlLa', 'basic');