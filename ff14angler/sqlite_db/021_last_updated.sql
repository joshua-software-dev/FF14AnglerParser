-- SQLITE
CREATE TABLE IF NOT EXISTS `last_updated` (
	`last_updated_timestamp` DATETIME NOT NULL,
	`bait_count` BIGINT NOT NULL,
	`fish_count` BIGINT NOT NULL,
	`spot_count` BIGINT NOT NULL,
	PRIMARY KEY (`last_updated_timestamp`)
);
