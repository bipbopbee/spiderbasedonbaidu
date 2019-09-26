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
    `url` varchar (1000) NOT NULL,
    `rightname` varchar (150) NOT NULL,
    `contentid` int (11) NOT NULL,
    `hosturl` varchar (150) NOT NULL
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
create table `bilibili` (
    `id` int (11) NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `keyword` varchar (150) NOT NULL,
    `title` varchar (150) NOT NULL,
    `detailurl` varchar (150) NOT NULL,
    `videourl` varchar (150) NOT NULL,
    `upname` varchar (150) NOT NULL
)DEFAULT CHARSET=utf8;
create table `meipai` (
    `id` int (11) NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `keyword` varchar (150) NOT NULL,
    `title` varchar (150) NOT NULL,
    `detailurl` varchar (150) NOT NULL,
    `videourl` varchar (150) NOT NULL,
    `upname` varchar (150) NOT NULL
)DEFAULT CHARSET=utf8;
drop table if exists `aiqiyi`;
create table `aiqiyi` (
    `id` int (11) NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `keyword` varchar (150) NOT NULL,
    `title` varchar (150) NOT NULL,
    `detailurl` varchar (150) NOT NULL,
    `videourl` varchar (150) NOT NULL,
    `upname` varchar (150) NOT NULL
)DEFAULT CHARSET=utf8;
drop table if exists `youku`;
create table `youku` (
    `id` int (11) NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `keyword` varchar (150) NOT NULL,
    `title` varchar (150) NOT NULL,
    `detailurl` varchar (150) NOT NULL,
    `videourl` varchar (150) NOT NULL,
    `upname` varchar (150) NOT NULL
)DEFAULT CHARSET=utf8;
drop table if exists `tengxun`;
create table `tengxun` (
    `id` int (11) NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `keyword` varchar (150) NOT NULL,
    `title` varchar (150) NOT NULL,
    `detailurl` varchar (150) NOT NULL,
    `videourl` varchar (1000) NOT NULL,
    `upname` varchar (150) NOT NULL
)DEFAULT CHARSET=utf8;

drop table if exists `appium`;
create table `appium` (
    `id` int (11) NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `keyword` varchar (150) NOT NULL,
    `check` varchar (150) NOT NULL,
    `lastsearchtime` varchar (150) NOT NULL
)DEFAULT CHARSET=utf8;

insert into privacy (privacyid, url, rightname, contentid)  values (NULL, 'http://ivi.bupt.edu.cn/hls/cctv3hd.m3u8','急速追杀', 240303);
insert into user (userid, username, userpassword, email, apitoken, role)  values (NULL, 'abc','abc', '516854715@qq.com', 'LWtrKgMmLIeAWyyDUlLa', 'basic');
insert into user (userid, username, userpassword, email, apitoken, role)  values (NULL, 'tom','abc', '123456@qq.com', 'LWtrKgMmLIeAWyyDUlLa', 'basic');
insert into gongzhonghao (id, url, title, publishname, publishdate)  values (NULL, 'http://weixin.sogou.com/api/share?timestamp=1564649418&signature=qIbwY*nI6KU9tBso4VCd8lYSesxOYgLcHX5tlbqlMR8N6flDHs4LLcFgRw7FjTAOdoVu-Y9-TphrwUo0FGpF-l9TdjqBEcb81AuS67HX41kChMrMEa0swXwHStcyXbOylZKg3rvI-aQlxU12cfhFgoMcBPo*Y1qDo4PnwVgGP8e64LbM7d2tgZ50RhfBkgMijhSz*g*e3WNZKSCQlKOQJ5eW2hvVUQFW7MnCNSa6XKY=', '神奇', '知安视娱', '2019-08-01');
insert into searches (id, name, type, year, keyword, searchnums, lastsearchtime)  values (NULL, '权力的游戏', 'film', '2017', '权力的游戏', '100', '2019-8-20 11:29:30');
insert into searchengine (id, name, keyword, searchnums)  values (NULL, '百度', '急速追杀', '1000');
alter table tengxun alter column videourl varchar(1000) NOT NULL;
update searchengine set searchnums= 1003 where keyword='急速追杀';
alter table searchengine add column (searchtime char(150));
alter table privacy add column (hosturl char(150));
alter table privacy alter column url varchar(1000) NOT NULL;
insert into privacy (url, rightname, contentid, hosturl) values ('https://api.nxflv.com/data/iqiyi/d3d4412c25630ce642770d51663cd7a3.m3u8', '蜘蛛侠3', '240320','http://www.iqiyi.com/v_19rszmv9hg.html')