/*
 Navicat Premium Data Transfer

 Source Server         : spider_server
 Source Server Type    : MySQL
 Source Server Version : 50716
 Source Host           : 10.108.107.104
 Source Database       : house_spider

 Target Server Type    : MySQL
 Target Server Version : 50716
 File Encoding         : utf-8

 Date: 11/27/2016 10:31:39 AM
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
--  Table structure for `bus_station`
-- ----------------------------
DROP TABLE IF EXISTS `bus_station`;
CREATE TABLE `bus_station` (
  `id` varchar(36) NOT NULL COMMENT 'id',
  `name` varchar(64) NOT NULL COMMENT '公交车站的名字',
  `lat` float(32,20) DEFAULT NULL COMMENT '维度',
  `lng` float(32,20) DEFAULT NULL COMMENT '经度',
  `lines` varchar(512) DEFAULT NULL COMMENT '经过的线路',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='周边信息——公交车站';

-- ----------------------------
--  Table structure for `commercial_area`
-- ----------------------------
DROP TABLE IF EXISTS `commercial_area`;
CREATE TABLE `commercial_area` (
  `id` varchar(36) NOT NULL COMMENT 'id',
  `name` varchar(64) DEFAULT NULL COMMENT '商圈名称',
  `address` varchar(255) DEFAULT NULL COMMENT '商圈地址',
  `lat` float(32,20) DEFAULT NULL COMMENT '纬度',
  `lng` float(32,20) DEFAULT NULL COMMENT '经度',
  `tag` varchar(64) DEFAULT NULL COMMENT '标签',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='周边信息——商圈';

-- ----------------------------
--  Table structure for `community`
-- ----------------------------
DROP TABLE IF EXISTS `community`;
CREATE TABLE `community` (
  `id` varchar(36) NOT NULL,
  `source` varchar(10) DEFAULT NULL COMMENT '数据信息来源',
  `title` varchar(64) DEFAULT NULL COMMENT '数据信息标题',
  `internal_id` varchar(64) DEFAULT NULL COMMENT '来源网站内部id（可能是数字也可能是拼音）',
  `address` varchar(64) DEFAULT NULL,
  `total_buildings` varchar(64) DEFAULT NULL,
  `total_houses` varchar(64) DEFAULT NULL COMMENT '房屋数量',
  `build_type` varchar(64) DEFAULT NULL,
  `build_time` varchar(64) DEFAULT NULL COMMENT '建造年份',
  `developer` varchar(64) DEFAULT NULL,
  `property` varchar(64) DEFAULT NULL,
  `property_fee` varchar(64) DEFAULT NULL COMMENT '物业费',
  `parking_num` varchar(255) DEFAULT NULL COMMENT '停车位数量',
  `green_rate` varchar(10) DEFAULT NULL COMMENT '绿化率',
  `plot_rate` varchar(10) DEFAULT NULL COMMENT '容积率',
  `lat` float(32,20) DEFAULT NULL COMMENT '纬度',
  `lng` float(32,20) DEFAULT NULL COMMENT '经度',
  `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '时间戳',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='小区';

-- ----------------------------
--  Table structure for `community_5i5j`
-- ----------------------------
DROP TABLE IF EXISTS `community_5i5j`;
CREATE TABLE `community_5i5j` (
  `id` varchar(36) NOT NULL,
  `source` varchar(10) DEFAULT NULL COMMENT '数据信息来源',
  `title` varchar(64) DEFAULT NULL COMMENT '数据信息标题',
  `internal_id` varchar(64) DEFAULT NULL COMMENT '来源网站内部id（可能是数字也可能是拼音）',
  `address` varchar(64) DEFAULT NULL,
  `unit_price` int(10) DEFAULT NULL COMMENT '均价',
  `prices` varchar(255) DEFAULT NULL COMMENT '以往房价信息',
  `total_buildings` varchar(64) DEFAULT NULL,
  `total_houses` varchar(64) DEFAULT NULL COMMENT '房屋数量',
  `build_type` varchar(64) DEFAULT NULL,
  `build_time` varchar(64) DEFAULT NULL COMMENT '建造年份',
  `developer` varchar(64) DEFAULT NULL,
  `property` varchar(64) DEFAULT NULL,
  `property_fee` varchar(64) DEFAULT NULL COMMENT '物业费',
  `parking_num` varchar(255) DEFAULT NULL COMMENT '停车位数量',
  `green_rate` varchar(10) DEFAULT NULL COMMENT '绿化率',
  `plot_rate` varchar(10) DEFAULT NULL COMMENT '容积率',
  `lat` float(32,20) DEFAULT NULL COMMENT '纬度',
  `lng` float(32,20) DEFAULT NULL COMMENT '经度',
  `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '时间戳',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='小区';

-- ----------------------------
--  Table structure for `community_bus_relation`
-- ----------------------------
DROP TABLE IF EXISTS `community_bus_relation`;
CREATE TABLE `community_bus_relation` (
  `id` varchar(36) NOT NULL COMMENT 'id',
  `community_id` varchar(36) NOT NULL COMMENT '小区id',
  `bus_station_id` varchar(36) NOT NULL COMMENT '公交车站id',
  `distance` int(10) DEFAULT NULL COMMENT '小区与公交车站的距离',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='小区与公交车站关系表';

-- ----------------------------
--  Table structure for `community_commercial_relation`
-- ----------------------------
DROP TABLE IF EXISTS `community_commercial_relation`;
CREATE TABLE `community_commercial_relation` (
  `id` varchar(36) NOT NULL COMMENT 'id',
  `community_id` varchar(36) DEFAULT NULL COMMENT '小区id',
  `commercial_area_id` varchar(36) DEFAULT NULL COMMENT '商圈id',
  `distance` int(10) DEFAULT NULL COMMENT '小区与商圈的距离',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='小区与商圈关系表';

-- ----------------------------
--  Table structure for `community_hospital_relation`
-- ----------------------------
DROP TABLE IF EXISTS `community_hospital_relation`;
CREATE TABLE `community_hospital_relation` (
  `id` varchar(36) NOT NULL COMMENT 'id',
  `community_id` varchar(36) NOT NULL COMMENT '小区id',
  `hospital_id` varchar(36) NOT NULL COMMENT '医院id',
  `distance` int(32) DEFAULT NULL COMMENT '小区与医院的距离',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='小区与医院关系表';

-- ----------------------------
--  Table structure for `community_market_relation`
-- ----------------------------
DROP TABLE IF EXISTS `community_market_relation`;
CREATE TABLE `community_market_relation` (
  `id` varchar(36) NOT NULL COMMENT 'id',
  `community_id` varchar(36) DEFAULT NULL COMMENT '小区id',
  `market_place_id` varchar(36) DEFAULT NULL COMMENT '商场id',
  `distance` int(10) DEFAULT NULL COMMENT '小区与商场的距离',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='小区与商场关系表';

-- ----------------------------
--  Table structure for `community_price_history`
-- ----------------------------
DROP TABLE IF EXISTS `community_price_history`;
CREATE TABLE `community_price_history` (
  `id` varchar(36) CHARACTER SET latin1 NOT NULL COMMENT 'id',
  `source` varchar(10) DEFAULT NULL COMMENT '数据来源',
  `community_id` varchar(36) CHARACTER SET latin1 DEFAULT NULL COMMENT '小区id',
  `month` varchar(10) CHARACTER SET latin1 DEFAULT NULL COMMENT '月份',
  `price` int(10) DEFAULT NULL COMMENT '价格',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
--  Table structure for `community_school_relation`
-- ----------------------------
DROP TABLE IF EXISTS `community_school_relation`;
CREATE TABLE `community_school_relation` (
  `id` varchar(36) NOT NULL COMMENT 'id',
  `community_id` varchar(36) NOT NULL COMMENT '小区id',
  `school_id` varchar(36) NOT NULL COMMENT '学校id',
  `distance` int(10) DEFAULT NULL COMMENT '小区与学校的距离',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='小区与学校关系表';

-- ----------------------------
--  Table structure for `community_subway_relation`
-- ----------------------------
DROP TABLE IF EXISTS `community_subway_relation`;
CREATE TABLE `community_subway_relation` (
  `id` varchar(36) NOT NULL COMMENT 'id',
  `community_id` varchar(36) NOT NULL COMMENT '小区id',
  `subway_station_id` varchar(36) NOT NULL COMMENT '地铁站id',
  `distance` int(10) DEFAULT NULL COMMENT '小区与地铁站的距离',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='小区与地铁关系表';

-- ----------------------------
--  Table structure for `hospital`
-- ----------------------------
DROP TABLE IF EXISTS `hospital`;
CREATE TABLE `hospital` (
  `id` varchar(36) NOT NULL COMMENT 'id',
  `name` varchar(64) NOT NULL COMMENT '医院名称',
  `address` varchar(255) DEFAULT NULL COMMENT '医院地址',
  `lat` float(32,20) DEFAULT NULL COMMENT '纬度',
  `lng` float(32,20) DEFAULT NULL COMMENT '经度',
  `tag` varchar(64) DEFAULT NULL COMMENT '百度地图标签',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='周边信息——医院';

-- ----------------------------
--  Table structure for `market_place`
-- ----------------------------
DROP TABLE IF EXISTS `market_place`;
CREATE TABLE `market_place` (
  `id` varchar(36) NOT NULL COMMENT 'id',
  `name` varchar(64) DEFAULT NULL COMMENT '商场名称',
  `address` varchar(255) DEFAULT NULL COMMENT '商场地址',
  `lat` float(32,20) DEFAULT NULL COMMENT '纬度',
  `lng` float(32,20) DEFAULT NULL COMMENT '经度',
  `tag` varchar(64) DEFAULT NULL COMMENT '标签',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='周边信息——商场';

-- ----------------------------
--  Table structure for `school`
-- ----------------------------
DROP TABLE IF EXISTS `school`;
CREATE TABLE `school` (
  `id` varchar(36) NOT NULL COMMENT 'id',
  `name` varchar(64) NOT NULL COMMENT '学校名字',
  `address` varchar(255) DEFAULT NULL COMMENT '学校地址',
  `lat` float(32,20) DEFAULT NULL COMMENT '维度',
  `lng` float(32,20) DEFAULT NULL COMMENT '经度',
  `tag` varchar(64) DEFAULT NULL COMMENT '百度地图标签',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='周边信息——学校';

-- ----------------------------
--  Table structure for `subway_station`
-- ----------------------------
DROP TABLE IF EXISTS `subway_station`;
CREATE TABLE `subway_station` (
  `id` varchar(36) NOT NULL COMMENT 'id',
  `name` varchar(64) NOT NULL COMMENT '地铁站名',
  `lat` float(32,20) DEFAULT NULL COMMENT '维度',
  `lng` float(32,20) DEFAULT NULL COMMENT '经度',
  `lines` varchar(64) DEFAULT NULL COMMENT '经过的地铁线',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='周边信息——地铁站';

SET FOREIGN_KEY_CHECKS = 1;
