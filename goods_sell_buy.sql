/*
 Navicat Premium Data Transfer

 Source Server         : data
 Source Server Type    : SQLite
 Source Server Version : 3008004
 Source Database       : main

 Target Server Type    : SQLite
 Target Server Version : 3008004
 File Encoding         : utf-8

 Date: 04/18/2018 00:19:30 AM
*/

PRAGMA foreign_keys = false;

-- ----------------------------
--  Table structure for goods_sell_buy
-- ----------------------------
DROP TABLE IF EXISTS "goods_sell_buy";
CREATE TABLE "goods_sell_buy" (
	 "goods_id" text NOT NULL,
	 "sell_order" text,
	 "buy_order" text,
	 "back_status" integer,
	 "time" text,
	PRIMARY KEY("goods_id")
);

PRAGMA foreign_keys = true;
