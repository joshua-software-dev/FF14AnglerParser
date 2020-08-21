-- SQLITE
CREATE TABLE IF NOT EXISTS `comment` (
	`comment_uuid` BLOB NOT NULL UNIQUE,
	`comment_fetch_timestamp` DATETIME NOT NULL,
	`comment_timestamp` DATETIME NOT NULL,
	`comment_author` VARCHAR(256) NOT NULL,
	`comment_text_original` VARCHAR(160) NOT NULL,
	`comment_text_translated` VARCHAR(160) NOT NULL,
	PRIMARY KEY (`comment_uuid`)
);
