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

 Date: 15/03/2019 19:18:48
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for tb_realtor_detail_json
-- ----------------------------
DROP TABLE IF EXISTS `tb_realtor_detail_json`;
CREATE TABLE `tb_realtor_detail_json`  (
  `property_id` bigint(20) NOT NULL,
  `last_update` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `address` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `last_operation_date` datetime(0) NULL DEFAULT NULL,
  `lat` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `lon` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `beds` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `sqft` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `baths` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `price` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `lot_size` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `data_interface` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `is_dirty` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `detail_json` json NULL,
  PRIMARY KEY (`property_id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;
