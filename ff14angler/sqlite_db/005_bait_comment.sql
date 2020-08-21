-- SQLITE
CREATE TABLE IF NOT EXISTS `bait_comment` (
	`bait_angler_bait_id` BIGINT NOT NULL,
	`comment_uuid` BLOB NOT NULL,
	PRIMARY KEY (`bait_angler_bait_id`, `comment_uuid`),
	FOREIGN KEY(`bait_angler_bait_id`) REFERENCES `bait` (`bait_angler_bait_id`) ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY(`comment_uuid`) REFERENCES `comment` (`comment_uuid`) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE INDEX `bait_comment_bait_angler_bait_id` ON `bait_comment` (`bait_angler_bait_id`);
