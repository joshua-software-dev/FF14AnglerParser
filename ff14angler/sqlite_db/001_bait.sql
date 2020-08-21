-- SQLITE
CREATE TABLE IF NOT EXISTS `bait` (
	`bait_angler_bait_id` BIGINT NOT NULL UNIQUE,
	`bait_xivapi_item_id` BIGINT NOT NULL,
	`bait_angler_name` VARCHAR(4096) NOT NULL,
	`bait_item_name` VARCHAR(4096) NOT NULL,
	`bait_icon_url` VARCHAR(2083) NOT NULL,
	`bait_large_icon_url` VARCHAR(2083) NULL,
	`bait_lodestone_url` VARCHAR(2083) NULL,
	`bait_item_level` SMALLINT NOT NULL,
	`bait_gil_cost` INTEGER NULL,
	`bait_gil_sell_price` INTEGER NULL,
	`bait_is_mooch_fish` TINYINT NOT NULL,
	PRIMARY KEY (`bait_angler_bait_id`)
);

CREATE INDEX `bait_bait_xivapi_item_id` ON `bait` (`bait_xivapi_item_id`);
