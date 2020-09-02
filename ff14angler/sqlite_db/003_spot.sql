-- SQLITE
CREATE TABLE IF NOT EXISTS `spot` (
	`spot_angler_spot_id` BIGINT NOT NULL UNIQUE,
	`spot_gathering_type` TEXT NOT NULL,
	`spot_gathering_type_unique_id` BIGINT NOT NULL,
	`spot_angler_area_id` BIGINT NOT NULL,
	`spot_angler_name` VARCHAR(4096) NOT NULL,
	`spot_angler_zone_name` VARCHAR(4096) NOT NULL,
	`spot_gathering_level` SMALLINT NOT NULL,
	`spot_angler_x_coord` SMALLINT NOT NULL,
	`spot_angler_y_coord` SMALLINT NOT NULL,
	`spot_angler_fishers_intuition_comment` VARCHAR(512) NULL,
	PRIMARY KEY (`spot_angler_spot_id`),
	UNIQUE (`spot_gathering_type`, `spot_gathering_type_unique_id`)
);

CREATE INDEX `spot_spot_gathering_type` ON `spot` (`spot_gathering_type`, `spot_gathering_type_unique_id`);
