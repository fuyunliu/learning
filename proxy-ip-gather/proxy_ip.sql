create table `proxy_ip` (
    `id` int not null auto_increment primary key,
    `ip` varchar(15) default '' comment 'ip地址',
    `port` varchar(5) default '' comment '端口',
    `type` varchar(10) default '' comment '类型',
    `anonymity` varchar(10) default '' comment '匿名度',
    `address` varchar(50) default '' comment '服务器地址',
    `availability` varchar(6) default '' comment '可用性'
) engine = innodb default charset = utf8mb4 collate = utf8mb4_unicode_ci;
