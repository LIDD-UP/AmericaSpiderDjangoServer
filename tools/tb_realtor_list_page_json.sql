/*
 Navicat MySQL Data Transfer

 Source Server         : local_mysql
 Source Server Type    : MySQL
 Source Server Version : 50724
 Source Host           : localhost:3306
 Source Schema         : america_real_estate

 Target Server Type    : MySQL
 Target Server Version : 50724
 File Encoding         : 65001

 Date: 15/03/2019 19:18:57
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for tb_realtor_list_page_json
-- ----------------------------
DROP TABLE IF EXISTS `tb_realtor_list_page_json`;
CREATE TABLE `tb_realtor_list_page_json`  (
  `json_data` json NULL,
  `last_operation_date` datetime(0) NULL DEFAULT NULL
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;
