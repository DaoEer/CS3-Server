# -*- coding: utf-8 -*-
import LoadModule
from SmartImport import smartImport

PATH = "Stall"

g_objectDict = {}

def loadObject():
	global g_objectDict
	objConfigs = LoadModule.openJsonPathCfg( PATH )
	for config in objConfigs:
		objClass = smartImport( "ObjectScript.Stall.StallBase" + ":" + "StallBase" )()
		scriptID = config[ "scriptID" ]
		objClass.initData( config )
		g_objectDict[ scriptID ] = objClass
		
def getObject( scriptID ):
	return g_objectDict.get( scriptID, None )

def hasObject( scriptID ):
	return scriptID in g_objectDict