-- SQLITE
CREATE TABLE IF NOT EXISTS `comment` (
	`comment_uuid` BLOB NOT NULL UNIQUE,
	`comment_fetch_timestamp` DATETIME NOT NULL,
	`comment_timestamp` DATETIME NOT NULL,
	`comment_author` VARCHAR(256) NOT NULL,
	`comment_html` TEXT NOT NULL,
	`comment_text_original` TEXT NOT NULL,
	`comment_text_translated` TEXT NOT NULL,
	PRIMARY KEY (`comment_uuid`)
);
