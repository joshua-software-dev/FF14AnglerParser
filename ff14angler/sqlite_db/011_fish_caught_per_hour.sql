-- SQLITE
CREATE TABLE IF NOT EXISTS `fish_caught_per_hour` (
	`fish_angler_fish_id` BIGINT NOT NULL,
	`hour_num` TINYINT NOT NULL,
	`hour_fish_caught_count` BIGINT NOT NULL,
	PRIMARY KEY (`fish_angler_fish_id`, `hour_num`),
	FOREIGN KEY(`fish_angler_fish_id`) REFERENCES `fish` (`fish_angler_fish_id`) ON UPDATE CASCADE ON DELETE CASCADE
);
