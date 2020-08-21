-- SQLITE
CREATE TABLE IF NOT EXISTS `spot_available_fish` (
	`spot_angler_spot_id` BIGINT NOT NULL,
	`fish_angler_fish_id` BIGINT NOT NULL,
	FOREIGN KEY(`spot_angler_spot_id`) REFERENCES `spot` (`spot_angler_spot_id`) ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY(`fish_angler_fish_id`) REFERENCES `fish` (`fish_angler_fish_id`) ON UPDATE CASCADE ON DELETE CASCADE,
	PRIMARY KEY (`spot_angler_spot_id`, `fish_angler_fish_id`)
);

CREATE INDEX `spot_available_fish_fish_angler_fish_id` ON `spot_available_fish` (`fish_angler_fish_id`);

CREATE INDEX `spot_available_fish_spot_angler_spot_id` ON `spot_available_fish` (`spot_angler_spot_id`);
