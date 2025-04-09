# -*- coding: utf-8 -*-
import LoadModule
from SmartImport import smartImport

PATH = "BunchSpace"

g_objectDict = {}

def loadObject():
	global g_objectDict
	objConfigs = LoadModule.openJsonPathCfg( PATH )
	for config in objConfigs:
		methodName = config[ "BunchScript" ]
		scriptID = config[ "scriptID" ]
		objClass = smartImport( "ObjectScript.BunchSpace."+methodName + ":" + methodName )()
		objClass.initData( config )
		g_objectDict[ scriptID ] = objClass
		
def getObect( scriptID ):
	return g_objectDict.get( scriptID, None )

def hasObject( scriptID ):
	return scriptID in g_objectDict