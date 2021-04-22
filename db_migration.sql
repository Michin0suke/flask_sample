CREATE TABLE addresses(
    id integer primary key,
    name varchar(128),
    name_ruby varchar(255),
    address text,
    memo varchar(255)
);
INSERT INTO addresses VALUES(1,'alice','ありす','tokyo','メモ');
INSERT INTO addresses VALUES(2,'bob','ぼぶ','hokkaido','');
INSERT INTO addresses VALUES(3,'charlie','ちゃーりー','shizuoka','');
INSERT INTO addresses VALUES(4,'david','でいびっど','akita','男');