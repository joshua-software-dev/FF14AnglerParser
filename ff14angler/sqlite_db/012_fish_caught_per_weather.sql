-- SQLITE
CREATE TABLE IF NOT EXISTS `fish_caught_per_weather` (
	`fish_angler_fish_id` BIGINT NOT NULL,
	`weather_name` VARCHAR(128) NOT NULL,
	`weather_fish_caught_count` BIGINT NOT NULL,
	PRIMARY KEY (`fish_angler_fish_id`, `weather_name`),
	FOREIGN KEY(`fish_angler_fish_id`) REFERENCES `fish` (`fish_angler_fish_id`) ON UPDATE CASCADE ON DELETE CASCADE
);
