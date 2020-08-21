-- SQLITE
CREATE TABLE IF NOT EXISTS `spot_bait_fish_catch_info` (
	`spot_angler_spot_id` BIGINT NOT NULL,
	`bait_angler_bait_id` BIGINT NOT NULL,
	`fish_angler_fish_id` BIGINT NOT NULL,
	`spot_bait_fish_catch_count` BIGINT NOT NULL,
	`spot_bait_fish_average_seconds_to_hook` SMALLINT,
	`spot_bait_fish_catch_percentage` VARCHAR(8) NOT NULL,
	PRIMARY KEY (`spot_angler_spot_id`, `bait_angler_bait_id`, `fish_angler_fish_id`),
	FOREIGN KEY(`spot_angler_spot_id`) REFERENCES `spot` (`spot_angler_spot_id`) ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY(`bait_angler_bait_id`) REFERENCES `bait` (`bait_angler_bait_id`) ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY(`fish_angler_fish_id`) REFERENCES `fish` (`fish_angler_fish_id`) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE INDEX `spot_bait_fish_catch_info_bait_angler_bait_id` ON `spot_bait_fish_catch_info` (`bait_angler_bait_id`);

CREATE INDEX `spot_bait_fish_catch_info_fish_angler_fish_id` ON `spot_bait_fish_catch_info` (`fish_angler_fish_id`);

CREATE INDEX `spot_bait_fish_catch_info_spot_angler_spot_id` ON `spot_bait_fish_catch_info` (`spot_angler_spot_id`);
