# -*- coding: utf-8 -*-


"""
usage:
	游戏对象script基类

attribute:
	objectType

member function:
	getObjectType
	getName

callback:
	pass

"""


#python
#engine
import KBEngine
#script
import ObjectScript.ObjectScriptBase.ScriptBase as ScriptBase

class GameScript( ScriptBase.ScriptBase ):
	"""
	游戏对象script基类
	"""
	def __init__( self ):
		ScriptBase.ScriptBase.__init__( self )
		self._entityType = ""
		self.scriptID = ""
	
	def initData( self, configData ):
		"""
		加载数据
		@param section:	数据
		"""
		self._entityType = configData[ "EntityType" ]
	
	def getEntityProperties( self, params ):
		entityDict = {}
		entityDict.update( params )
		entityDict[ "scriptID" ] = self.scriptID
		return entityDict
	
	def createLocalEntity( self, params = None ) :
		"""
		在当前baseapp创建
		"""
		return KBEngine.createEntityLocally( self._entityType, self.getEntityProperties( params ) )
	
	def createAnywhereEntity( self, params = None, callbackFunc = None ):
		"""
		找一个空闲的baseapp创建
		"""
		KBEngine.createEntityAnywhere( self._entityType, self.getEntityProperties( params ), callbackFunc )
