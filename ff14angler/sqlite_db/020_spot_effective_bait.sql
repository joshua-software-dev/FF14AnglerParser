-- SQLITE
CREATE TABLE IF NOT EXISTS `spot_effective_bait` (
	`spot_angler_spot_id` BIGINT NOT NULL,
	`bait_angler_bait_id` BIGINT NOT NULL,
	FOREIGN KEY(`spot_angler_spot_id`) REFERENCES `spot` (`spot_angler_spot_id`) ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY(`bait_angler_bait_id`) REFERENCES `bait` (`bait_angler_bait_id`) ON UPDATE CASCADE ON DELETE CASCADE,
	PRIMARY KEY (`spot_angler_spot_id`, `bait_angler_bait_id`)
);

CREATE INDEX `spot_effective_bait_bait_angler_bait_id` ON `spot_effective_bait` (`bait_angler_bait_id`);

CREATE INDEX `spot_effective_bait_spot_angler_spot_id` ON `spot_effective_bait` (`spot_angler_spot_id`);