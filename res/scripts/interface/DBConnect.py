# -*- coding: utf-8 -*-

from KBEDebug import *
from DBConnector import DBConnector
from PyDataSection import PyXMLSection

#kbengine.xml配置路径
#注意：xml解析工具目前已知是支持UTF-8编码格式
KBE_CONFIG_PATH = "res/server/kbengine.xml"

db = None
def getCsol3DB():
	global db
	if not db:
		try:
			dbConfig = getCsol3DBConfig()
			db = DBConnector( **dbConfig )
		except:
			INFO_MSG("connect db error")
	return db
	
#读取kbengine.xml配置
csol_db_config = None
def getCsol3DBConfig():
	global csol_db_config
	if not csol_db_config:
		kbeSection = PyXMLSection.parse(KBE_CONFIG_PATH)
		gameDBSection = kbeSection["dbmgr/databaseInterfaces/default"]
		csol_db_config = {
			"host"		: gameDBSection.readString("host"),
			"port"		: gameDBSection.readString("port"),
			"database"	: gameDBSection.readString("databaseName"),
			"user"		: gameDBSection.readString("auth/username"),
			"password"	: gameDBSection.readString("auth/password"),
			"charset"	: "utf8",
		}
	return csol_db_config