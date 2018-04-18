/*
 Navicat Premium Data Transfer

 Source Server         : data
 Source Server Type    : SQLite
 Source Server Version : 3017000
 Source Schema         : main

 Target Server Type    : SQLite
 Target Server Version : 3017000
 File Encoding         : 65001

 Date: 18/04/2018 10:06:40
*/

PRAGMA foreign_keys = false;

-- ----------------------------
-- Table structure for goods_sell_buy
-- ----------------------------
DROP TABLE IF EXISTS "goods_sell_buy";
CREATE TABLE "goods_sell_buy" (
  "goods_id" text NOT NULL,
  "sell_order" text,
  "buy_order" text,
  "back_status" integer NOT NULL,
  "price" real,
  "status" integer NOT NULL DEFAULT 0,
  "time" text,
  PRIMARY KEY ("goods_id")
);

-- ----------------------------
-- Records of "goods_sell_buy"
-- ----------------------------
INSERT INTO "goods_sell_buy" VALUES (33232, NULL, NULL, 0, NULL, 1, NULL);

PRAGMA foreign_keys = true;
