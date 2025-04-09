# -*- coding: utf-8 -*-

from ObjectScript.ObjectScriptBase import ScriptFactory
from SmartImport import smartImport
import LoadModule

class SceneFactory( ScriptFactory.ScriptFactory ):
	def __init__( self ):
		ScriptFactory.ScriptFactory.__init__( self )
		self._datas = {}
	
	def loadData( self, pathUrl ):
		jsFileObj = LoadModule. openJsonCfg( pathUrl )
		for scriptID, pfData in jsFileObj.items():
			methodName = pfData[ "EntityScript" ]
			objClass = smartImport( "ObjectScript.Scene."+methodName + ":" + methodName )()
			objClass.initData( pfData )
			self._datas[ scriptID ] = objClass
	
	def getObject( self, scriptID ):
		return self._datas.get( scriptID )

g_SceneFactory = SceneFactory()