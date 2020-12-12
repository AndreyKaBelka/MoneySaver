CREATE TABLE IF NOT EXISTS `moneysaver`.`users`
(
    `user_id`   INT UNSIGNED NOT NULL,
    `user_bank` DOUBLE       NOT NULL DEFAULT 0,
    PRIMARY KEY (`user_id`),
    UNIQUE INDEX `user_id_UNIQUE` (`user_id` ASC) VISIBLE
)
    COMMENT = 'User database';