-- SQLITE
CREATE TABLE IF NOT EXISTS `fish_tug_strength` (
	`fish_angler_fish_id` BIGINT NOT NULL,
	`tug_strength` TINYINT NOT NULL,
	`tug_strength_percent` DECIMAL NOT NULL,
	PRIMARY KEY (`fish_angler_fish_id`, `tug_strength`),
	FOREIGN KEY(`fish_angler_fish_id`) REFERENCES `fish` (`fish_angler_fish_id`) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE INDEX `fish_tug_strength_fish_angler_fish_id` ON `fish_tug_strength` (`fish_angler_fish_id`);
