CREATE TABLE IF NOT EXISTS `moneysaver`.`categories`
(
    `cat_id`  BIGINT UNSIGNED NOT NULL,
    `cat_exp` DOUBLE UNSIGNED NOT NULL DEFAULT 0,
    PRIMARY KEY (`cat_id`),
    UNIQUE INDEX `cat_id_UNIQUE` (`cat_id` ASC) VISIBLE
)
    COMMENT = 'Categories table';