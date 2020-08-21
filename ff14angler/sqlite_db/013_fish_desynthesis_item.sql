-- SQLITE
CREATE TABLE IF NOT EXISTS `fish_desynthesis_item` (
	`fish_angler_fish_id` BIGINT NOT NULL,
	`desynthesis_item_id` BIGINT NOT NULL,
	`desynthesis_item_name` VARCHAR(4096) NOT NULL,
	`desynthesis_icon_url` VARCHAR(2083) NOT NULL,
	`desynthesis_large_icon_url` VARCHAR(2083) NULL,
	`desynthesis_angler_item_name` VARCHAR(4096) NOT NULL,
	`desynthesis_angler_lodestone_url` VARCHAR(2083) NULL,
	`desynthesis_angler_percentage` VARCHAR(8) NOT NULL,
	PRIMARY KEY (`fish_angler_fish_id`, `desynthesis_item_id`),
	FOREIGN KEY(`fish_angler_fish_id`) REFERENCES `fish` (`fish_angler_fish_id`) ON UPDATE CASCADE ON DELETE CASCADE
);
