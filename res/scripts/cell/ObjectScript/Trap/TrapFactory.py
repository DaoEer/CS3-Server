# -*- coding: utf-8 -*-

from ObjectScript.ObjectScriptBase.ScriptFactory import ScriptFactory
from SmartImport import smartImport
import LoadModule
from ObjectScript.Trap.Type.ServerTriggerTrap import ServerTriggerTrap

IMPORT_PATH = "ObjectScript.Trap.Type."

class TrapFactory( ScriptFactory ):
	def __init__( self ):
		ScriptFactory.__init__( self )
		self._datas = {}
	
	def loadData( self, pathUrl ):
		jsFileObj = LoadModule. openJsonCfg( pathUrl )
		for scriptID, data in jsFileObj.items():
			methodName = data[ "EntityScript" ]
			objClass = smartImport( IMPORT_PATH + methodName + ":" + methodName )()
			objClass.initData( data )
			self._datas[ scriptID ] = objClass
	
	def getObject( self, scriptID ):
		return self._datas.get( scriptID )

g_trapFactory = TrapFactory()