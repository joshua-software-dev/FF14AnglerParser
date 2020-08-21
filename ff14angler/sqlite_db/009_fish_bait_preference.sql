-- SQLITE
CREATE TABLE IF NOT EXISTS `fish_bait_preference` (
	`fish_angler_fish_id` BIGINT NOT NULL,
	`bait_angler_bait_id` BIGINT NOT NULL,
	`bait_percentage` VARCHAR(8) NOT NULL,
	PRIMARY KEY (`fish_angler_fish_id`, `bait_angler_bait_id`)
);

CREATE INDEX `fish_bait_preference_bait_angler_bait_id` ON `fish_bait_preference` (`bait_angler_bait_id`);

CREATE INDEX `fish_bait_preference_fish_angler_fish_id` ON `fish_bait_preference` (`fish_angler_fish_id`);
