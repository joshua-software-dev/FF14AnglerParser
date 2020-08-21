-- SQLITE
CREATE TABLE IF NOT EXISTS `spot_bait_total_fish_caught` (
	`spot_angler_spot_id` BIGINT NOT NULL,
	`bait_angler_bait_id` BIGINT NOT NULL,
	`spot_bait_total_catch_count` BIGINT NOT NULL,
	PRIMARY KEY (`spot_angler_spot_id`, `bait_angler_bait_id`),
	FOREIGN KEY(`spot_angler_spot_id`) REFERENCES `spot` (`spot_angler_spot_id`) ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY(`bait_angler_bait_id`) REFERENCES `bait` (`bait_angler_bait_id`) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE INDEX `spot_bait_total_fish_caught_bait_angler_bait_id` ON `spot_bait_total_fish_caught` (`bait_angler_bait_id`);

CREATE INDEX `spot_bait_total_fish_caught_spot_angler_spot_id` ON `spot_bait_total_fish_caught` (`spot_angler_spot_id`);
