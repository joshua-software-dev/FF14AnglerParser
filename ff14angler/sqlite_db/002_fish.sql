-- SQLITE
CREATE TABLE IF NOT EXISTS `fish` (
	`fish_angler_fish_id` BIGINT NOT NULL UNIQUE,
	`fish_xivapi_item_id` BIGINT NOT NULL UNIQUE,
	`fish_angler_name` VARCHAR(4096) NOT NULL,
	`fish_item_name_de` VARCHAR(4096) NOT NULL,
	`fish_item_name_en` VARCHAR(4096) NOT NULL,
	`fish_item_name_fr` VARCHAR(4096) NOT NULL,
	`fish_item_name_ja` VARCHAR(4096) NOT NULL,
	`fish_icon_url` VARCHAR(2083) NOT NULL,
	`fish_large_icon_url` VARCHAR(2083) NULL,
	`fish_lodestone_url` VARCHAR(2083) NULL,
	`fish_item_level` SMALLINT NOT NULL,
	`fish_item_description_de` TEXT NOT NULL,
	`fish_item_description_en` TEXT NOT NULL,
	`fish_item_description_fr` TEXT NOT NULL,
	`fish_item_description_ja` TEXT NOT NULL,
	`fish_fishing_log_description_de` TEXT NULL,
	`fish_fishing_log_description_en` TEXT NULL,
	`fish_fishing_log_description_fr` TEXT NULL,
	`fish_fishing_log_description_ja` TEXT NULL,
	`fish_introduced_patch` VARCHAR(8) NOT NULL,
	`fish_angler_territory` VARCHAR(128) NULL,
	`fish_angler_item_category` VARCHAR(128) NOT NULL,
	`fish_angler_double_hooking_count` VARCHAR(8) NOT NULL,
	`fish_angler_aquarium_size` VARCHAR(8) NULL,
	`fish_angler_canvas_size` VARCHAR(8) NULL,
	PRIMARY KEY (`fish_angler_fish_id`)
);

CREATE INDEX `fish_fish_xivapi_item_id` ON `fish` (`fish_xivapi_item_id`);
