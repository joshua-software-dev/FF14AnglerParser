-- SQLITE
CREATE TABLE IF NOT EXISTS `bait_alt_currency_price` (
	`bait_angler_bait_id` BIGINT NOT NULL,
	`bait_alt_currency_id` BIGINT NOT NULL,
	`bait_alt_currency_cost` INTEGER NOT NULL,
	`bait_alt_currency_name` VARCHAR(4096) NOT NULL,
	PRIMARY KEY (`bait_angler_bait_id`, `bait_alt_currency_id`, `bait_alt_currency_cost`),
	FOREIGN KEY(`bait_angler_bait_id`) REFERENCES `bait` (`bait_angler_bait_id`) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE INDEX `bait_alt_currency_price_bait_angler_bait_id` ON `bait_alt_currency_price` (`bait_angler_bait_id`);
