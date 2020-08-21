-- SQLITE
CREATE TABLE IF NOT EXISTS `spot_comment` (
	`spot_angler_spot_id` BIGINT NOT NULL,
	`comment_uuid` BLOB NOT NULL,
	PRIMARY KEY (`spot_angler_spot_id`, `comment_uuid`),
	FOREIGN KEY(`spot_angler_spot_id`) REFERENCES `spot` (`spot_angler_spot_id`) ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY(`comment_uuid`) REFERENCES `comment` (`comment_uuid`) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE INDEX `spot_comment_spot_angler_spot_id` ON `spot_comment` (`spot_angler_spot_id`);
