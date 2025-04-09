# -*- coding: utf-8 -*-

import KBEngine


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
import Math
#script

class GameScript:
	"""
	游戏对象script基类
	"""
	def __init__( self ):
		self.scriptID = ""
		self._entityType = ""
	
	def initData( self, configData ):
		"""
		初始化数据
		@param section:	数据
		"""
		self.scriptID = configData["scriptID"]
		self._entityType = configData["EntityType"]
		
	def createEntity( self, spaceEntity, position, direction, params ) :
		"""
		在当前baseapp创建
		"""
		return KBEngine.createEntity( self._entityType, spaceEntity.spaceID, tuple(Math.Vector3(position)), direction, self.getEntityProperties( params ) )
	