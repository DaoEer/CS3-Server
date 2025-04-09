# -*- coding: utf-8 -*-
import LoadModule
from SmartImport import smartImport

PATH = "BunchSpace"

g_objectDict = {}

def loadObject():
	global g_objectDict
	objConfigs = LoadModule.openJsonPathCfg( PATH )
	for config in objConfigs:
		methodName = config[ "DomainType" ]
		scriptID = config[ "scriptID" ]
		objClass = smartImport( "ObjectScript.BunchSpaceDomain."+methodName + ":" + methodName )()
		objClass.initData( config )
		g_objectDict[ scriptID ] = objClass

def getAllBunchSpaceDomian():
	global g_objectDict
	return g_objectDict

def getObect( scriptID ):
	global g_objectDict
	return g_objectDict.get( scriptID, None )

def hasObject( scriptID ):
	global g_objectDict
	return g_objectDict.has_key( scriptID )