# -*- coding: utf-8 -*-

from ObjectScript.ObjectScriptBase import ScriptFactory
from SmartImport import smartImport
import LoadModule
from ObjectScript.Monster import Monster

class MonsterFactory( ScriptFactory.ScriptFactory ):
	def __init__( self ):
		ScriptFactory.ScriptFactory.__init__( self )
		self._datas = {}
	
	def loadData( self, pathUrl ):
		jsFileObj = LoadModule. openJsonCfg( pathUrl )
		for scriptID, npcData in jsFileObj.items():
			methodName = npcData[ "EntityScript" ]
			objClass = smartImport( "ObjectScript.Monster."+methodName + ":" + methodName )()
			objClass.initData( npcData )
			self._datas[ scriptID ] = objClass
	
	def getObject( self, scriptID ):
		return self._datas.get( scriptID )

g_monsterFactory = MonsterFactory()