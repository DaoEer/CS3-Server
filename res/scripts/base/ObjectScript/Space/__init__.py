# -*- coding: utf-8 -*-
import LoadModule
from SmartImport import smartImport

PATH = "GameObject/SpaceObject"
g_objectDict = {}
def loadSpaceObject():
	global g_objectDict
	objConfigs = LoadModule.openJsonPathCfg( PATH )
	for config in objConfigs:
		methodName = config[ "EntityScript" ]
		scriptID = config[ "scriptID" ]
		objClass = smartImport( "ObjectScript.Space."+methodName + ":" + methodName )()
		objClass.initData( config )
		g_objectDict[ scriptID ] = objClass
		
def getObect( scriptID ):
	return g_objectDict.get( scriptID, None )

def hasObject( scriptID ):
	return scriptID in g_objectDict
	

#space配置
SPACE_CONFIG_PATH = "res/config/SpaceConfig.json"
g_noBalanceSpaceList = []
g_noBalanceCellAppList = []
g_spaceConsumeObjectDict = {}
def loadSpaceConfig():
	global g_noBalanceSpaceList
	global g_noBalanceCellAppList
	global g_spaceConsumeObjectDict
	config = LoadModule.openFile(SPACE_CONFIG_PATH)
	g_noBalanceSpaceList = config.get("NoBalanceSpace", [])
	g_noBalanceCellAppList = config.get("NoBalanceCellApp", [])
	g_spaceConsumeObjectDict = config.get("SpaceConsume", {})
	
def getSpaceConsume(scriptID):
	#space消耗配置
	return g_spaceConsumeObjectDict.get(scriptID, 0.5)
	
def getAllNoBalanceSpace():
	#不参与负载均衡的space配置(指定几个空的cellapp来承载这些space)
	return g_noBalanceSpaceList
	
def getAllNoBalanceCellAPP():
	return g_noBalanceCellAppList
	
def loadObject():
	loadSpaceObject()
	loadSpaceConfig()