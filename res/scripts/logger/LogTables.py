# -*- coding: utf-8 -*-
import os
import KBEngine
from KBEDebug import *
import threading, traceback, logging
import Define

from LogProcesser import CenterLogProcesser
from LogProcesser import g_logProcesser


class CsolLogProcesser( CenterLogProcesser ):
	def __init__( self, manager = g_logProcesser ):
		super(CsolLogProcesser, self).__init__(manager)
		self.checkCreateTable()
	
	def getTableCreateDesc(self, name):
		#获取表的结构
		items = self.dbc.select("SHOW CREATE TABLE " + name + " ;")[0]
		Lines = items[1].split("\n")
		TableName = Lines[0].split("`")[1]
		Fields = {}
		Keys   = {}
		for i in range(1,len(Lines) - 1):
			line = Lines[i].strip()
			if line[0] == "`":
				line = line[1:]
				FieldDef = line.split("`")
				Fields[FieldDef[0]] = FieldDef[1].strip()[:-1]
			else:	
				if line[-1] == ",":
					line = line[:-1]
				Keys[line] = 1

		return (Fields, Keys)

	def checkCreateTable( self ):
		tablename = self.sqlTable.split("`")[1]
		#检查表是否存在
		checktable = "SHOW TABLES LIKE '" + tablename + "'"
		items = self.dbc.select(checktable)
		if len(items) == 0:
			self.dbc.execute( self.sqlTable, "" )
		else:
			tempTable = self.sqlTable.replace("Log_", "Log_Temp_")
			temptablename = tempTable.split("`")[1]

			self.dbc.execute( tempTable, "" )

			oldDescInfo = self.getTableCreateDesc(tablename)
			tempDescInfo = self.getTableCreateDesc(temptablename)
			
			needalert = 0
			#表结构修改
			alterstr =  "ALTER TABLE " + tablename + " "
			for key, value in oldDescInfo[0].items():
				if key in  tempDescInfo[0]:
					if value != tempDescInfo[0][key]:
						#更改
						needalert = 1
						alterstr = alterstr + " CHANGE " + key + " " + key + " " + tempDescInfo[0][key] + ","
					del tempDescInfo[0][key]
				else:
					#删除
					needalert = 1
					alterstr = alterstr + " DROP " + key + ","

			#增加
			for key,value in tempDescInfo[0].items():
				needalert = 1
				alterstr = alterstr + " ADD " + key + " " + value + ","


			#键值的修改
			#print(oldDescInfo[1])
			#print(tempDescInfo[1])
			for key, value in oldDescInfo[1].items():
				if key in  tempDescInfo[1]:
					del tempDescInfo[1][key]
				else:
					#删除
					needalert = 1
					alterstr = alterstr + " DROP KEY " + key.split("`")[1] + ","

			#增加
			for key,value in tempDescInfo[1].items():
				needalert = 1
				alterstr = alterstr + " ADD " + key + ","

			#提交修改
			print(alterstr)
			if needalert == 1:
				alterstr = alterstr[:-1] + ";"
				try:
					self.dbc.execute( alterstr, "" )
				except Exception as error:
					ERROR_MSG("execute sql error: [%s]" % error)
					#执行改表结构预计出错需要删除临时表
					self.dbc.execute( "DROP TABLE " + temptablename + ";", "" )
					
			#删除临时表
			self.dbc.execute( "DROP TABLE " + temptablename + ";", "" )
			
	def onSaveLog( self, logQueue ):
		"""
		"""
		if self.LOG_TYPE not in Define._LOG_TABLES:
			ERROR_MSG("Unknown type '%s'" % self.LOG_TYPE)
			return
		fields = Define._LOG_FIELD_[ self.LOG_TYPE ].split( "," )
		if len(logQueue[0]) != len(fields):
			ERROR_MSG("Type '%s', Define fields config error" % self.LOG_TYPE)
			return
		
		values = []
		for log in logQueue:
			values.append( tuple( log ) )
		sql = "insert into `%s` " % Define._LOG_TABLES[ self.LOG_TYPE ]
		fieldStr = ""
		valueStr = ""
		for field in fields:
			fieldStr += "`%s`, " % field.strip()
			valueStr += "%s, "
		sql = sql + " (" + fieldStr[ : len( fieldStr ) - 2 ] + ") values (" + valueStr[ : len( valueStr ) - 2 ] + ")"
		self.dbc.execute( sql, *values )
		
		
class LogQuest( CsolLogProcesser ):
	sqlTable = """CREATE TABLE IF NOT EXISTS `Log_Quest` (
					`id` bigint(20) NOT NULL AUTO_INCREMENT,
					`updatetime` VARCHAR(255),
					`action` TINYINT UNSIGNED,
					`roleDBID` BIGINT UNSIGNED,
					`roleName` VARCHAR(255),
					`questID` VARCHAR(255),
					`questName` VARCHAR(255),
					`roleLevel` SMALLINT UNSIGNED,
					`roleGrade` TINYINT UNSIGNED,
					`useTime` VARCHAR(255),
					PRIMARY KEY (`id`)
					)ENGINE=InnoDB DEFAULT CHARSET=utf8;
					"""
	LOG_TYPE = Define.LOG_TYPE_QUEST


class LogItem( CsolLogProcesser ):
	sqlTable = """CREATE TABLE IF NOT EXISTS `Log_Item` (
					`id` bigint(20) NOT NULL AUTO_INCREMENT,
					`updatetime` VARCHAR(255),
					`action` TINYINT UNSIGNED,
					`roleDBID` BIGINT UNSIGNED,
					`roleName` VARCHAR(255),
					`itemID` BIGINT UNSIGNED,
					`itemUid` BIGINT UNSIGNED,
					`itemName` VARCHAR(255),
					`itemNum` TINYINT UNSIGNED,
					`param1` VARCHAR(255),
					`param2` VARCHAR(255),
					`param3` VARCHAR(255),
					`itemData` BLOB,
					PRIMARY KEY (`id`)
					)ENGINE=InnoDB DEFAULT CHARSET=utf8;
					"""
	LOG_TYPE = Define.LOG_TYPE_ITEM


class LogCoin( CsolLogProcesser ):
	sqlTable = """CREATE TABLE IF NOT EXISTS `Log_Coin` (
					`id` BIGINT( 20 ) NOT NULL AUTO_INCREMENT,
					`updateTime` VARCHAR(255),
					`action` TINYINT UNSIGNED,
					`accountDBID` BIGINT UNSIGNED,
					`roleDBID` BIGINT UNSIGNED,
					`roleName` VARCHAR(255),
					`oldValue` BIGINT UNSIGNED,
					`newValue` BIGINT UNSIGNED,
					`reason` VARCHAR(255),
					`orders` VARCHAR(255),
					PRIMARY KEY (`id`)
					)ENGINE = InnoDB DEFAULT CHARSET=utf8;
					"""
	LOG_TYPE = Define.LOG_TYPE_COIN

class LogPro( CsolLogProcesser ):
	sqlTable = """CREATE TABLE IF NOT EXISTS `Log_Pro` (
					`id` BIGINT( 20 ) NOT NULL AUTO_INCREMENT,
					`updateTime` VARCHAR(255),
					`action` TINYINT UNSIGNED,
					`roleDBID` BIGINT UNSIGNED,
					`roleName` VARCHAR(255),
					`param1` VARCHAR(255),
					`param2` VARCHAR(255),
					`param3` VARCHAR(255),
					`param4` VARCHAR(255),
					`param5` VARCHAR(255),
					PRIMARY KEY (`id`)
					)ENGINE = InnoDB DEFAULT CHARSET=utf8;
					"""
	LOG_TYPE = Define.LOG_TYPE_PRO


class LogEquip( CsolLogProcesser ):
	sqlTable = """CREATE TABLE IF NOT EXISTS `Log_Equip` (
					`id` BIGINT( 20 ) NOT NULL AUTO_INCREMENT,
					`updateTime` VARCHAR(255),
					`action` TINYINT UNSIGNED,
					`roleDBID` BIGINT UNSIGNED,
					`roleName` VARCHAR(255),
					`itemID` BIGINT UNSIGNED,
					`itemUid` BIGINT UNSIGNED,
					`itemName` VARCHAR(255),
					`itemNum` TINYINT UNSIGNED,
					`param1` VARCHAR(255),
					`param2` VARCHAR(255),
					`param3` VARCHAR(255),
					`param4` VARCHAR(255),
					`param5` VARCHAR(255),
					`param6` VARCHAR(255),
					`param7` VARCHAR(255),
					`param8` VARCHAR(255),
					`param9` VARCHAR(2048),
					`param10` VARCHAR(2048),
					`equipData` BLOB,
					PRIMARY KEY (`id`)
					)ENGINE = InnoDB DEFAULT CHARSET=utf8;
					"""
	LOG_TYPE = Define.LOG_TYPE_EQUIP


class LogRelation( CsolLogProcesser ):
	sqlTable = """CREATE TABLE IF NOT EXISTS `Log_Relation` (
					`id` BIGINT( 20 ) NOT NULL AUTO_INCREMENT,
					`updateTime` VARCHAR(255),
					`action` TINYINT UNSIGNED,
					`roleDBID` BIGINT UNSIGNED,
					`roleName` VARCHAR(255),
					`tRoleDBID` BIGINT UNSIGNED,
					`tRoleName` VARCHAR(255),
					`param1` VARCHAR(255),
					`param2` VARCHAR(255),
					`param3` VARCHAR(255),
					PRIMARY KEY (`id`)
					)ENGINE = InnoDB DEFAULT CHARSET=utf8;
					"""
	LOG_TYPE = Define.LOG_TYPE_RELATION


class LogPet( CsolLogProcesser ):
	sqlTable = """CREATE TABLE IF NOT EXISTS `Log_Pet` (
					`id` BIGINT( 20 ) NOT NULL AUTO_INCREMENT,
					`updateTime` VARCHAR(255),
					`action` TINYINT UNSIGNED,
					`roleDBID` BIGINT UNSIGNED,
					`roleName` VARCHAR(255),
					`petName` VARCHAR(255),
					`petUname` VARCHAR(255),
					`petUid` VARCHAR(255),
					`petQuality` TINYINT UNSIGNED,
					`petLevel` TINYINT UNSIGNED,
					`param1` VARCHAR(255),
					`param2` VARCHAR(255),
					`param3` VARCHAR(255),
					`param4` VARCHAR(255),
					`param5` VARCHAR(255),
					`param6` VARCHAR(255),
					`param7` VARCHAR(255),
					`param8` VARCHAR(255),
					`param9` VARCHAR(255),
					`param10` VARCHAR(255),
					`petData` BLOB,
					PRIMARY KEY (`id`)
					)ENGINE = InnoDB DEFAULT CHARSET=utf8;
					"""	
	LOG_TYPE = Define.LOG_TYPE_PET


class LogTrade( CsolLogProcesser ):
	sqlTable = """CREATE TABLE IF NOT EXISTS `Log_Trade` (
					`id` BIGINT( 20 ) NOT NULL AUTO_INCREMENT,
					`updateTime` VARCHAR(255),
					`action` TINYINT UNSIGNED,
					`roleDBID` BIGINT UNSIGNED,
					`roleName` VARCHAR(255),
					`param1` VARCHAR(255),
					`param2` VARCHAR(255),
					`param3` VARCHAR(255),
					`param4` VARCHAR(255),
					`param5` VARCHAR(255),
					`param6` VARCHAR(255),
					`param7` VARCHAR(255),
					`param8` VARCHAR(255),
					`param9` VARCHAR(255),
					`itemData` BLOB,
					PRIMARY KEY (`id`)
					)ENGINE = InnoDB DEFAULT CHARSET=utf8;
					"""	
	LOG_TYPE = Define.LOG_TYPE_TRADE


class LogMail( CsolLogProcesser ):
	sqlTable = """CREATE TABLE IF NOT EXISTS `Log_Mail` (
					`id` BIGINT( 20 ) NOT NULL AUTO_INCREMENT,
					`updateTime` VARCHAR(255),
					`action` TINYINT UNSIGNED,
					`senderName` VARCHAR(255),
					`receiverName` VARCHAR(255),
					`mailType` TINYINT UNSIGNED,
					`title` VARCHAR(255),
					`money` MEDIUMINT,
					`itemData` BLOB,
					`param1` VARCHAR(255),
					`param2` VARCHAR(255),
					PRIMARY KEY (`id`)
					)ENGINE = InnoDB DEFAULT CHARSET=utf8;
					"""	
	LOG_TYPE = Define.LOG_TYPE_MAIL



class LogTong( CsolLogProcesser ):
	sqlTable = """CREATE TABLE IF NOT EXISTS `Log_Tong` (
					`id` BIGINT( 20 ) NOT NULL AUTO_INCREMENT,
					`updateTime` VARCHAR(255),
					`action` TINYINT UNSIGNED,
					`tongDBID` BIGINT UNSIGNED,
					`tongName` VARCHAR(255),
					`param1` VARCHAR(255),
					`param2` VARCHAR(255),
					`param3` VARCHAR(255),
					`param4` VARCHAR(255),
					`param5` VARCHAR(255),
					`param6` VARCHAR(255),
					`param7` VARCHAR(255),
					PRIMARY KEY (`id`)
					)ENGINE = InnoDB DEFAULT CHARSET=utf8;
					"""	
	LOG_TYPE = Define.LOG_TYPE_TONG


class LogSkill( CsolLogProcesser ):
	sqlTable = """CREATE TABLE IF NOT EXISTS `Log_Skill` (
					`id` BIGINT( 20 ) NOT NULL AUTO_INCREMENT,
					`updateTime` VARCHAR(255),
					`action` TINYINT UNSIGNED,
					`roleDBID` BIGINT UNSIGNED,
					`roleName` VARCHAR(255),
					`skillID` VARCHAR(255),
					`param1` VARCHAR(255),
					`param2` VARCHAR(255),
					`param3` VARCHAR(255),
					`param4` VARCHAR(255),
					`param5` VARCHAR(255),
					`param6` VARCHAR(255),
					PRIMARY KEY (`id`)
					)ENGINE = InnoDB DEFAULT CHARSET=utf8;
					"""	
	LOG_TYPE = Define.LOG_TYPE_SKILL


class LogRecharge( CsolLogProcesser ):
	sqlTable = """CREATE TABLE IF NOT EXISTS `Log_Recharge` (
					`id` BIGINT( 20 ) NOT NULL AUTO_INCREMENT,
					`updateTime` VARCHAR(255),
					`accountDBID` BIGINT UNSIGNED,
					`accountName` VARCHAR(255),
					`rechargeType` TINYINT UNSIGNED,
					`coinType` TINYINT UNSIGNED,
					`value` BIGINT UNSIGNED,
					`transactionID` VARCHAR(255),
					PRIMARY KEY (`id`)
					)ENGINE = InnoDB DEFAULT CHARSET=utf8;
					"""	
	LOG_TYPE = Define.LOG_TYPE_RECHARGE


class LogAccount( CsolLogProcesser ):
	sqlTable = """CREATE TABLE IF NOT EXISTS `Log_Account` (
					`id` BIGINT( 20 ) NOT NULL AUTO_INCREMENT,
					`updateTime` VARCHAR(255),
					`action` TINYINT UNSIGNED,
					`accountDBID` BIGINT UNSIGNED,
					`accountName` VARCHAR(255),
					`param1` VARCHAR(255),
					`param2` VARCHAR(255),
					`param3` VARCHAR(255),
					PRIMARY KEY (`id`)
					)ENGINE = InnoDB DEFAULT CHARSET=utf8;
					"""	
	LOG_TYPE = Define.LOG_TYPE_ACCOUNT


class LogRole( CsolLogProcesser ):
	sqlTable = """CREATE TABLE IF NOT EXISTS `Log_Role` (
					`id` BIGINT( 20 ) NOT NULL AUTO_INCREMENT,
					`updateTime` VARCHAR(255),
					`action` TINYINT UNSIGNED,
					`roleDBID` BIGINT UNSIGNED,
					`roleName` VARCHAR(255),
					`accountDBID` BIGINT UNSIGNED,
					`accountName` VARCHAR(255),
					`param1` VARCHAR(255),
					`param2` VARCHAR(255),
					`param3` VARCHAR(255),
					`param4` VARCHAR(255),
					`param5` VARCHAR(255),
					`blobParam1` BLOB,
					`blobParam2` BLOB,
					`blobParam3` BLOB,
					PRIMARY KEY (`id`)
					)ENGINE = InnoDB DEFAULT CHARSET=utf8;
					"""	
	LOG_TYPE = Define.LOG_TYPE_ROLE


class LogVend( CsolLogProcesser ):
	sqlTable = """CREATE TABLE IF NOT EXISTS `Log_Vend` (
					`id` BIGINT( 20 ) NOT NULL AUTO_INCREMENT,
					`updateTime` VARCHAR(255),
					`roleDBID` BIGINT UNSIGNED,
					`roleName` VARCHAR(255),
					PRIMARY KEY (`id`)
					)ENGINE = InnoDB DEFAULT CHARSET=utf8;
					"""	
	LOG_TYPE = Define.LOG_TYPE_VEND


class LogActCopy( CsolLogProcesser ):
	sqlTable = """CREATE TABLE IF NOT EXISTS `Log_ActCopy` (
					`id` BIGINT( 20 ) NOT NULL AUTO_INCREMENT,
					`updateTime` VARCHAR(255),
					`action` TINYINT UNSIGNED,
					`actCopyType` TINYINT UNSIGNED,
					`actCopyName` VARCHAR(255),
					`roleDBID` BIGINT UNSIGNED,
					`roleName` VARCHAR(255),
					`param1` VARCHAR(255),
					`param2` VARCHAR(255),
					`param3` VARCHAR(255),
					PRIMARY KEY (`id`)
					)ENGINE = InnoDB DEFAULT CHARSET=utf8;
					"""	
	LOG_TYPE = Define.LOG_TYPE_ACT_COPY


class LogOnline( CsolLogProcesser ):
	sqlTable = """CREATE TABLE IF NOT EXISTS `Log_Online` (
					`id` BIGINT( 20 ) NOT NULL AUTO_INCREMENT,
					`update_time` VARCHAR(255),
					`lineNum` TINYINT UNSIGNED,
					`onlineRoleNum` INT UNSIGNED,
					`onlineMacNum` INT UNSIGNED,
					PRIMARY KEY (`id`)
					)ENGINE = InnoDB DEFAULT CHARSET=utf8;
					"""	
	LOG_TYPE = Define.LOG_TYPE_ONLINE


class LogCost( CsolLogProcesser ):
	sqlTable = """CREATE TABLE IF NOT EXISTS `Log_Cost` (
					`id` BIGINT( 20 ) NOT NULL AUTO_INCREMENT,
					`update_time` VARCHAR(255),
					`account_id` VARCHAR(32),
					`gid` VARCHAR(32),
					`buy_item_id` VARCHAR(32),
					`buy_item_name` VARCHAR(32),
					`item_price` INT UNSIGNED,
					`buy_item_amount` INT UNSIGNED,
					`gold_coin_cost` INT UNSIGNED,
					`gold_coin_left` INT UNSIGNED,
					`bind_coin_cost` INT UNSIGNED,
					`bind_coin_left` INT UNSIGNED,
					`level` INT UNSIGNED,
					PRIMARY KEY (`id`)
					)ENGINE = InnoDB DEFAULT CHARSET=utf8;
					"""	
	LOG_TYPE = Define.LOG_TYPE_COST


class LogProp( CsolLogProcesser ):
	sqlTable = """CREATE TABLE IF NOT EXISTS `Log_Prop` (
					`id` BIGINT( 20 ) NOT NULL AUTO_INCREMENT,
					`update_time` VARCHAR(255),
					`line` VARCHAR(32),
					`account_id` VARCHAR(32),
					`gid` VARCHAR(32),
					`level` INT UNSIGNED,
					`iid` VARCHAR(64),
					`item_name` VARCHAR(108),
					`memo` VARCHAR(108),
					PRIMARY KEY (`id`)
					)ENGINE = InnoDB DEFAULT CHARSET=utf8;
					"""	
	LOG_TYPE = Define.LOG_TYPE_PROP


class LogRoleUpLevel( CsolLogProcesser ):
	sqlTable = """CREATE TABLE IF NOT EXISTS `Log_RoleUpLevel` (
					`id` BIGINT( 20 ) NOT NULL AUTO_INCREMENT,
					`update_time` VARCHAR(255),
					`account_id` VARCHAR(32),
					`gid` VARCHAR(32),
					`level` INT UNSIGNED,
					`time_used` INT UNSIGNED,
					`last_lv_up` VARCHAR(32),
					PRIMARY KEY (`id`)
					)ENGINE = InnoDB DEFAULT CHARSET=utf8;
					"""	
	LOG_TYPE = Define.LOG_TYPE_ROLE_UP_LEVEL


class LogActiveRecord( CsolLogProcesser ):
	sqlTable = """CREATE TABLE IF NOT EXISTS `Log_ActRecord` (
					`id` BIGINT( 20 ) NOT NULL AUTO_INCREMENT,
					`update_time` VARCHAR(255),
					`line` VARCHAR(32),
					`action` VARCHAR(108),
					`account_id` VARCHAR(32),
					`gid` VARCHAR(32),
					`level` INT UNSIGNED,
					`bonus_type` VARCHAR(32),
					`bonus_name` VARCHAR(32),
					`start_time` VARCHAR(32),
					`time_used` INT UNSIGNED,
					`action_status` INT UNSIGNED,
					PRIMARY KEY (`id`)
					)ENGINE = InnoDB DEFAULT CHARSET=utf8;
					"""	
	LOG_TYPE = Define.LOG_TYPE_ACTIVE_RECORD
	
class LogItemLoad( CsolLogProcesser ):
	sqlTable = """CREATE TABLE IF NOT EXISTS `Log_ItemLoad` (
					`id` BIGINT( 20 ) NOT NULL AUTO_INCREMENT,
					`update_time` VARCHAR(255),
					`itemID` BIGINT UNSIGNED,
					PRIMARY KEY (`id`)
					)ENGINE = InnoDB DEFAULT CHARSET=utf8;
					"""	
	LOG_TYPE = Define.LOG_TYPE_ITEM_LOAD




_LOG_TYPE_DICT_ = {
	Define.LOG_TYPE_QUEST: 		LogQuest,
	Define.LOG_TYPE_ITEM: 			LogItem,
	Define.LOG_TYPE_COIN: 		LogCoin,
	Define.LOG_TYPE_PRO:			LogPro,
	Define.LOG_TYPE_EQUIP:		LogEquip,
	Define.LOG_TYPE_RELATION:	LogRelation,
	Define.LOG_TYPE_PET:			LogPet,
	Define.LOG_TYPE_TRADE:		LogTrade,
	Define.LOG_TYPE_MAIL:			LogMail,
	Define.LOG_TYPE_TONG:		LogTong,
	Define.LOG_TYPE_SKILL:			LogSkill,
	Define.LOG_TYPE_ACCOUNT:	LogAccount,
	Define.LOG_TYPE_ROLE:			LogRole,
	Define.LOG_TYPE_RECHARGE:	LogRecharge,
	Define.LOG_TYPE_VEND:			LogVend,
	Define.LOG_TYPE_ACT_COPY:	LogActCopy,
	Define.LOG_TYPE_ONLINE:	LogOnline,
	Define.LOG_TYPE_COST:	LogCost,
	Define.LOG_TYPE_PROP:	LogProp,
	Define.LOG_TYPE_ROLE_UP_LEVEL:	LogRoleUpLevel,
	Define.LOG_TYPE_ACTIVE_RECORD:	LogActiveRecord,
	Define.LOG_TYPE_ITEM_LOAD:	LogItemLoad,
	}

def init():
	for type, className in _LOG_TYPE_DICT_.items():
		className()
		pass
