# -*- coding: utf-8 -*-

from ObjectScript.ObjectScriptBase import ScriptFactory
from SmartImport import smartImport
import LoadModule
from ObjectScript.SpellBox import SpellBox
from ObjectScript.SpellBox import MultiAreaSpellBox

class SpellBoxFactory( ScriptFactory.ScriptFactory ):
	def __init__( self ):
		ScriptFactory.ScriptFactory.__init__( self )
		self._datas = {}

	
	def loadData( self, pathUrl, MultiAreaPathUrl ):
		jsFileObj = LoadModule.openJsonCfg( pathUrl )
		for scriptID, npcData in jsFileObj.items():
			methodName = npcData[ "EntityScript" ]
			objClass = smartImport( "ObjectScript.SpellBox."+methodName + ":" + methodName )()
			objClass.initData( npcData )
			self._datas[ scriptID ] = objClass

		jsAreaObj = LoadModule.openJsonCfg( MultiAreaPathUrl )
		for scriptID, npcData in jsAreaObj.items():
			methodName = npcData[ "EntityScript" ]
			objClass = smartImport( "ObjectScript.SpellBox."+methodName + ":" + methodName )()
			objClass.initData( npcData )
			self._datas[ scriptID ] = objClass
			
	def getObject( self, scriptID ):
		return self._datas.get( scriptID )
		
g_spellBoxFactory = SpellBoxFactory()