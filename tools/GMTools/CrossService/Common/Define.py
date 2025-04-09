# -*- coding: utf-8 -*-
"""
声明、定义
"""

import logging
logger = logging.getLogger("KST")


SERVER_CONFIG_PATH = "CrossService/Config/ServerConfig.json"
CROSS_FIELDS_CONFIG_PATH = "CrossService/Config/CrossFieldsConfig.json"




#表
TABLE_NAME_ROLE = "tbl_Role"
TABLE_NAME_ACCOUNT = "tbl_Account"
TABLE_NAME_ACCOUNT_INFO = "kbe_accountinfos"

#子表中父表dbid的字段名
PARENT_TABLE_DBID_FIELD_NAME = "parentID"
CHILD_TABLE_DBID_FIELD_NAME = "id"

#同步数据配置表(CrossFieldsConfig.json)禁止配置的字段
FIELDS_CONFIG_FORBID_DICT = {
	TABLE_NAME_ROLE: ["id, sm_parentDBID"], 
	TABLE_NAME_ACCOUNT: ["id"],
}

#玩家名字和dbid数据库字段名
ROLE_NAME_FIELD_NAME = "sm_playerName"

#数据库表主键类型
DB_FIELD_KEY_TYPE_ACCOUNT_NAME = 0 #账号名字
DB_FIELD_KEY_TYPE_ACCOUNT_DBID = 1 #账号entityDBID
DB_FIELD_KEY_TYPE_ROLE_NAME = 2 #角色名字
DB_FIELD_KEY_TYPE_ROLE_DBID = 3 #角色DBID
DB_FIELD_KEY_TYPE_PARENT_DBID = 4 #父表DBID

PLAYER_DEFAULT_VALUE = -1

#删除角色数据后需要改变Account表的上次登录玩家DBID值
ACCOUNT_LAST_LOGON_DBID_DEFAULE_VALUE = 0
ACCOUNT_LAST_LOGON_DBID_NAME = "sm_lastLogonDBID"
ACCOUNT_NAME_FIELD_NAME = "sm_playerName"

#需要检查的服务器
CHECK_SERVER_KEY_TYPE_PREV = 1
CHECK_SERVER_KEY_TYPE_FOLLOWED = 2

#跨服登录的玩家关键字识别字段
CROSS_LOGON_FIELD_KEY_NAME_ACCOUNT = "sm_isCrossServiceAccount"
CROSS_LOGON_FIELD_KEY_NAME_ROLE = "sm_isCrossServiceLogon"

CS3_GAME_SECRET = "CSOL"
