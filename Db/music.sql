BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS `music` (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`file_id`	TEXT NOT NULL,
	`right_answer`	TEXT NOT NULL,
	`wrong_answers`	TEXT NOT NULL
);
INSERT INTO `music` VALUES (1,'AwADAgADcAADNzBJSrXFsyNJFi_cAg','Стук в дверь','Клоун из ОНО, Мама входит в комнату, Это ты идешь есть в 01:00');
INSERT INTO `music` VALUES (2,'AwADAgADcAADiqtJShCNH7nFo5wQAg','Звон бокалов ','Что-то падает на пол, Это ребенок играет с посудой, На заводе фарфоровых игрушек');
COMMIT;
