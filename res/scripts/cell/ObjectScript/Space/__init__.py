# -*- coding: utf-8 -*-
import LoadModule
from SmartImport import smartImport

PATH = "GameObject/SpaceObject"

g_objectDict = {}
g_tongSpaceCopy = {}

def loadSpaceObject():
	global g_objectDict
	objConfigs = LoadModule.openJsonPathCfg( PATH )
	for config in objConfigs:
		methodName = config[ "EntityScript" ]
		scriptID = config[ "scriptID" ]
		objClass = smartImport( "ObjectScript.Space."+methodName + ":" + methodName )()
		objClass.initData( config )
		g_objectDict[ scriptID ] = objClass
		
def getObject( scriptID ):
	return g_objectDict.get( scriptID, None )

def hasObject( scriptID ):
	return scriptID in g_objectDict
	
def registerTongSpaceCopy( scriptID, reqLevel ):
	global g_tongSpaceCopy
	if reqLevel not in g_tongSpaceCopy:
		g_tongSpaceCopy[reqLevel] = [ scriptID ]
	else:
		if scriptID not in g_tongSpaceCopy[reqLevel]:
			g_tongSpaceCopy[reqLevel].append( scriptID )
	
def getTongSpaceCopyScriptIDs():
	global g_tongSpaceCopy
	return g_tongSpaceCopy
	
#space负载消耗配置
SPACE_CONFIG_PATH = "res/config/SpaceConfig.json"
g_noBalanceCellAppList = []
def loadSpaceConfig():
	global g_noBalanceCellAppList
	config = LoadModule.openFile(SPACE_CONFIG_PATH)
	g_noBalanceCellAppList = config.get("NoBalanceCellApp", [])
	
def getAllNoBalanceCellAPP():
	return g_noBalanceCellAppList
	
def loadObject():
	loadSpaceObject()
	loadSpaceConfig()
	