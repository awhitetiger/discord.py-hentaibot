BEGIN TRANSACTION;
CREATE TABLE `users` (
	`user_id`	INTEGER,
	`bounties_comp`	INTEGER,
	`bounty_credits`	INTEGER
);
INSERT INTO `users` VALUES (239563864918851584,0,0);
CREATE TABLE "bounties" (
	`bounty_id`	INTEGER,
	`poster_id`	INTEGER,
	`saucer`	INTEGER
);
COMMIT;
