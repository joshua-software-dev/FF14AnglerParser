-- SQLITE
CREATE TABLE IF NOT EXISTS `fish_involved_recipe` (
	`fish_angler_fish_id` BIGINT NOT NULL,
	`recipe_item_id` BIGINT NOT NULL,
	`recipe_item_name` VARCHAR(4096) NOT NULL,
	`recipe_angler_name` VARCHAR(4096) NOT NULL,
	`recipe_icon_url` VARCHAR(2083) NOT NULL,
	`recipe_large_icon_url` VARCHAR(2083) NULL,
	`recipe_angler_lodestone_url` VARCHAR(2083) NULL,
	`recipe_angler_crafting_class` TEXT NOT NULL,
	PRIMARY KEY (`fish_angler_fish_id`, `recipe_item_id`),
	FOREIGN KEY(`fish_angler_fish_id`) REFERENCES `fish` (`fish_angler_fish_id`) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE INDEX `fish_involved_recipe_fish_angler_fish_id` ON `fish_involved_recipe` (`fish_angler_fish_id`);
