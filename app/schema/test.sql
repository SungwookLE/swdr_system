-- file name : test.sql
-- pwd : /project_name/app/schema/test.sql
 
use SWDR_DB;

CREATE TABLE `SWDR_DB`.`Project` (
  `프로젝트명` VARCHAR(64) NOT NULL,
  `플랫폼` VARCHAR(64) NULL,
  `양산일` DATE NULL,
  `담당자` VARCHAR(45) NULL,
  `업체` VARCHAR(45) NULL,
  `모델` VARCHAR(45) NULL,
  `진행율` VARCHAR(45) NULL,
  `리뷰계획` DATE NULL,
  `번들대표차종` VARCHAR(45) NULL,
  `비고` VARCHAR(255) NULL,
  UNIQUE INDEX `프로젝트명_UNIQUE` (`프로젝트명` ASC));


ALTER TABLE `SWDR_DB`.`Project` 
ADD COLUMN `1차리뷰` MEDIUMTEXT NULL AFTER `비고`,
ADD COLUMN `2차리뷰` MEDIUMTEXT NULL AFTER `1차리뷰`,
ADD COLUMN `3차리뷰` VARCHAR(45) NULL AFTER `2차리뷰`;

ALTER TABLE `SWDR_DB`.`Project` 
CHANGE COLUMN `3차리뷰` `3차리뷰` MEDIUMTEXT NULL DEFAULT NULL ;

