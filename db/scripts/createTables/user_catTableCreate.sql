CREATE TABLE `moneysaver`.`user_cat`
(
    `user_id` INT UNSIGNED NOT NULL,
    `cat_id`  BIGINT UNSIGNED NOT NULL,
    PRIMARY KEY (`user_id`, `cat_id`),
    INDEX `user_id` (`user_id` ASC) VISIBLE,
    INDEX `cat_id` (`cat_id` ASC) VISIBLE,
    CONSTRAINT `user_id`
        FOREIGN KEY (`user_id`)
            REFERENCES `moneysaver`.`users` (`user_id`)
            ON DELETE CASCADE
            ON UPDATE CASCADE,
    CONSTRAINT `cat_id_user`
        FOREIGN KEY (`cat_id`)
            REFERENCES `moneysaver`.`categories` (`cat_id`)
            ON DELETE CASCADE
            ON UPDATE CASCADE
)
    COMMENT = 'Table to get rid off MANY to MANY';