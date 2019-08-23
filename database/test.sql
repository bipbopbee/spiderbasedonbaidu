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
    `createtime` varchar (100) NOT NULL,
    `rightname` varchar (150) NOT NULL,
    `url` varchar (150) NOT NULL,
    `email` varchar (150) NOT NULL,
    `contentid` int (11) NOT NULL
) DEFAULT CHARSET=utf8;
create table `privacy` (
    `privacyid` int (11) NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `url` varchar (150) NOT NULL,
    `rightname` varchar (150) NOT NULL,
    `contentid` int (11) NOT NULL
)DEFAULT CHARSET=utf8;
create table `gongzhonghao` (
    `id` int (11) NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `url` varchar (150) NOT NULL,
    `title` varchar (150) NOT NULL,
    `publishname` varchar (150) NOT NULL,
    `publishdate` varchar (150) NOT NULL
)DEFAULT CHARSET=utf8;
create table `searches` (
    `id` int (11) NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `name` varchar (150) NOT NULL,
    `type` varchar (150) NOT NULL,
    `year` varchar (150) NOT NULL,
    `keyword` varchar (150) NOT NULL,
    `searchnums` varchar (150) NOT NULL,
    `lastsearchtime` varchar (150) NOT NULL
)DEFAULT CHARSET=utf8;
create table `searchengine` (
    `id` int (11) NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `name` varchar (150) NOT NULL,
    `keyword` varchar (150) NOT NULL,
    `searchnums` varchar (150) NOT NULL
)DEFAULT CHARSET=utf8;
insert into privacy (privacyid, url, rightname, contentid)  values (NULL, 'http://ivi.bupt.edu.cn/hls/cctv3hd.m3u8','急速追杀', 240303);
insert into user (userid, username, userpassword, email, apitoken, role)  values (NULL, 'abc','abc', '516854715@qq.com', 'LWtrKgMmLIeAWyyDUlLa', 'basic');
insert into user (userid, username, userpassword, email, apitoken, role)  values (NULL, 'tom','abc', '123456@qq.com', 'LWtrKgMmLIeAWyyDUlLa', 'basic');
insert into gongzhonghao (id, url, title, publishname, publishdate)  values (NULL, 'http://weixin.sogou.com/api/share?timestamp=1564649418&signature=qIbwY*nI6KU9tBso4VCd8lYSesxOYgLcHX5tlbqlMR8N6flDHs4LLcFgRw7FjTAOdoVu-Y9-TphrwUo0FGpF-l9TdjqBEcb81AuS67HX41kChMrMEa0swXwHStcyXbOylZKg3rvI-aQlxU12cfhFgoMcBPo*Y1qDo4PnwVgGP8e64LbM7d2tgZ50RhfBkgMijhSz*g*e3WNZKSCQlKOQJ5eW2hvVUQFW7MnCNSa6XKY=', '神奇', '知安视娱', '2019-08-01');
insert into searches (id, name, type, year, keyword, searchnums, lastsearchtime)  values (NULL, '权力的游戏', 'film', '2017', '权力的游戏', '100', '2019-8-20 11:29:30');
insert into searchengine (id, name, keyword, searchnums)  values (NULL, '百度', '急速追杀', '1000');
update searchengine set searchnums= 1003 where keyword='急速追杀';
alter table searchengine add column (searchtime char(150));
alter table privacy add column (hosturl char(150));