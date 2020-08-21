-- SQLITE
CREATE TABLE IF NOT EXISTS `fish_caught_count` (
	`fish_angler_fish_id` BIGINT NOT NULL,
	`fish_caught_all_hours_count` BIGINT NOT NULL,
	`fish_caught_all_weathers_count` BIGINT NULL,
	PRIMARY KEY (`fish_angler_fish_id`),
	FOREIGN KEY(`fish_angler_fish_id`) REFERENCES `fish` (`fish_angler_fish_id`) ON UPDATE CASCADE ON DELETE CASCADE
);
