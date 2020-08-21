-- SQLITE
CREATE TABLE IF NOT EXISTS `fish_involved_leve` (
	`fish_angler_fish_id` BIGINT NOT NULL,
	`leve_id` BIGINT NOT NULL,
	`leve_name` VARCHAR(4096) NOT NULL,
	`leve_angler_name` VARCHAR(4096) NOT NULL,
	`leve_angler_name_jp` VARCHAR(4096) NOT NULL,
	`leve_level` SMALLINT NOT NULL,
	`leve_angler_turn_in_count` SMALLINT NOT NULL,
	PRIMARY KEY (`fish_angler_fish_id`, `leve_id`),
	FOREIGN KEY(`fish_angler_fish_id`) REFERENCES `fish` (`fish_angler_fish_id`) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE INDEX `fish_involved_leve_fish_angler_fish_id` ON `fish_involved_leve` (`fish_angler_fish_id`);
