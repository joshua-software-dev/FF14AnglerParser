-- SQLITE
CREATE TABLE IF NOT EXISTS `fish_comment` (
	`fish_angler_fish_id` BIGINT NOT NULL,
	`comment_uuid` BLOB NOT NULL,
	PRIMARY KEY (`fish_angler_fish_id`, `comment_uuid`),
	FOREIGN KEY(`fish_angler_fish_id`) REFERENCES `fish` (`fish_angler_fish_id`) ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY(`comment_uuid`) REFERENCES `comment` (`comment_uuid`) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE INDEX `fish_comment_fish_angler_fish_id` ON `fish_comment` (`fish_angler_fish_id`);
