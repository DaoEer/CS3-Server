# -*- coding: utf-8 -*-

import json
import configparser
from xml.dom.minidom import parse as xmlParse
from collections import OrderedDict

from . import stringRes
from . import ItemTypeEnum

serverConfigFile = "config/ServerConfig.xml"
defaultServerConfigFile = "config/CS3ServerDefaultConfig.ini"
activityConfigFile = "config/ActivityConfig.json"


#---------------------------------------------------------------
#json相关
#---------------------------------------------------------------
def loadJsonDataByFile(file):
	"""
	根据文件名加载json文件数据
	"""
	fileObject = open( file, encoding="utf8" )
	fileContent = fileObject.read()
	if fileContent.startswith(u'\ufeff'):
		fileContent = fileContent.encode('utf8')[3:].decode('utf8')
		
	jsFileObj = json.loads( fileContent )
	fileObject.close()
	return jsFileObj
	
#---------------------------------------------------------------
#xml相关
#---------------------------------------------------------------
def loadXmlData(file):
	"""
	加载xml文件数据
	"""
	domTree = xmlParse(file)
	collection = domTree.documentElement
	return collection

def loadServerConfig():
	"""
	加载服务器配置数据
	"""
	serverConfigs = OrderedDict()
	collection = loadXmlData(serverConfigFile)
	serverCollection = collection.getElementsByTagName("serverConfigs")[0]
	for server in serverCollection.getElementsByTagName("server"):
		tempDict = {}
		key = server.getElementsByTagName("key")[0].childNodes[0].data
		tempDict["name"] = server.getElementsByTagName("name")[0].childNodes[0].data
		tempDict["baseappHosts"] = []
		baseappHost = server.getElementsByTagName("baseappHosts")[0]
		for host in baseappHost.getElementsByTagName("host"):
			tempDict["baseappHosts"].append(host.childNodes[0].data)
		databaseList = ["gameDatabaseInfo", "logDatabaseInfo"]
		for database in databaseList:
			tempDict[database] = {}
			dbInfo = server.getElementsByTagName(database)[0]
			tempDict[database]["host"] = dbInfo.getElementsByTagName("host")[0].childNodes[0].data
			tempDict[database]["port"] = dbInfo.getElementsByTagName("port")[0].childNodes[0].data
			tempDict[database]["database"] = dbInfo.getElementsByTagName("database")[0].childNodes[0].data
			tempDict[database]["user"] = dbInfo.getElementsByTagName("user")[0].childNodes[0].data
			tempDict[database]["password"] = dbInfo.getElementsByTagName("password")[0].childNodes[0].data
			tempDict[database]["charset"] = dbInfo.getElementsByTagName("charset")[0].childNodes[0].data
		serverConfigs[key] = tempDict
	return serverConfigs
	
#---------------------------------------------------------------
#ini相关
#---------------------------------------------------------------
def getDefaultServer():
	"""
	获取默认服务器
	"""
	configInst = configparser.ConfigParser()
	configInst.read(defaultServerConfigFile)
	try:
		defaultServer = configInst.get("DefaultServer", "key")
		return defaultServer
	except:
		return ""
		
def getSeverConfigPath():
	"""
	获取服务器的配置路径
	"""
	configInst = configparser.ConfigParser()
	configInst.read(defaultServerConfigFile)
	try:
		configPath = configInst.get("DefaultServer", "configPath")
		return configPath
	except:
		return ""
		
#---------------------------------------------------------------
#角色相关
#---------------------------------------------------------------
def getRoleXiuweiLevel(level, xiuwei):
	"""
	获取玩家对应的道行等级
	"""
	for daohengLevel, xiuweiData in stringRes.ROLE_DAOHENG_LEVEL_CH_DICT.items():
		if level < xiuweiData["playerLevel"] or xiuwei < xiuweiData["daoheng"]:
			return max(1, int(daohengLevel) - 1)
	return 1

def getRoleJingjie(level, xiuwei, camp):
	"""
	获取玩家境界
	"""
	xiuweiLevel = getRoleXiuweiLevel(level, xiuwei)
	return stringRes.ROLE_DAOHENG_LEVEL_CH_DICT.get( str(xiuweiLevel) ).get("ch").get(camp, level)
	
def getRoleMenpai(camp, profession):
	"""
	获取玩家门派
	"""
	return stringRes.MENPAI_TYPE_DICT[camp][profession]
	
def getEquipClasses(profession):
	"""
	获取装备门派
	"""
	classes = ""
	if profession == 0:
		return stringRes.ALL_MENPAI_RES
	for key, value in stringRes.MENPAI_TYPE_DICT.items():
		classes = classes + value.get(profession, key) + r"/"
	return classes[:-1]
	
def equipAttributeChangeStr(equipData1, equipData2):
	"""
	装备属性值改变
	"""
	keyList = list(set(list(equipData1.keys()) + list(equipData2.keys())))
	changeStr = ""
	tempDict = {}
	for key in keyList:
		tempDict[key] = equipData2.get(key, 0) - equipData1.get(key, 0)
	for key, value in tempDict.items():
		if value > 0:
			changeStr = changeStr + stringRes.ROLE_ATTRIBUTE_NUMBER_DICT.get(key, str(key)) + "+" + str(value) + " "
		elif value < 0:
			changeStr = changeStr + stringRes.ROLE_ATTRIBUTE_NUMBER_DICT.get(key, str(key)) + str(value) + " "
	return changeStr

def getActivityDatas():
	"""
	获取活动配置数据
	"""
	return loadJsonDataByFile(activityConfigFile)