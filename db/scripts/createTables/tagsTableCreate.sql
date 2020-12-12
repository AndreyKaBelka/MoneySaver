CREATE TABLE IF NOT EXISTS `moneysaver`.`tags`
(
    `tag_id`   INT UNSIGNED NOT NULL AUTO_INCREMENT,
    `cat_id`   BIGINT UNSIGNED NOT NULL,
    `tag_desc` VARCHAR(20)  NOT NULL,
    PRIMARY KEY (`tag_id`),
    UNIQUE INDEX `tag_id_UNIQUE` (`tag_id` ASC) VISIBLE
)
    COMMENT = 'Tags for category';
ALTER TABLE `moneysaver`.`tags`
    ADD INDEX `cat_id_idx` (`cat_id` ASC) VISIBLE;
ALTER TABLE `moneysaver`.`tags`
    ADD CONSTRAINT `cat_id`
        FOREIGN KEY (`cat_id`)
            REFERENCES `moneysaver`.`categories` (`cat_id`)
            ON DELETE CASCADE
            ON UPDATE NO ACTION;