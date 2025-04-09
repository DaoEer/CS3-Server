# -*- coding: utf-8 -*-

from ObjectScript.ObjectScriptBase import ScriptFactory
from SmartImport import smartImport
import LoadModule

class PetFactory( ScriptFactory.ScriptFactory ):
	def __init__( self ):
		ScriptFactory.ScriptFactory.__init__( self )
		self._datas = {}
	
	def loadData( self, pathUrl ):
		jsFileObj = LoadModule. openJsonCfg( pathUrl )
		for scriptID, petData in jsFileObj.items():
			methodName = petData[ "EntityScript" ]
			objClass = smartImport( "ObjectScript.Pet."+methodName + ":" + methodName )()
			objClass.initData( petData )
			self._datas[ scriptID ] = objClass
	
	def getObject( self, scriptID ):
		return self._datas.get( scriptID )

g_petFactory = PetFactory()