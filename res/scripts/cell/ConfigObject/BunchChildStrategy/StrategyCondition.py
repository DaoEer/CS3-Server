# -*- coding: utf-8 -*-
"""
策略条件脚本
"""
class ConditionBase:
	"""
	基类
	"""
	def __init__( self ):
		pass
	
	def init( self, dict ):
		pass
	
	def check( self, bunchObj, spaceEntity, playerEntity ):
		return False

class ConditionIsFirstIn( ConditionBase ):
	"""
	第一次进入
	只能配在第一层
	"""
	def check( self, bunchObj, spaceEntity, playerEntity ):
		return bunchObj.scriptID not in playerEntity.enteredBunchRecord

class ConditionNotIsFirstIn( ConditionBase ):
	"""
	不是第一次进入
	只能配在第一层
	"""
	def check( self, bunchObj, spaceEntity, playerEntity ):
		return bunchObj.scriptID in playerEntity.enteredBunchRecord

class ConditionBeforeIsBig( ConditionBase ):
	"""
	前一层是大副本
	只能配在非第一层
	"""
	def check( self, bunchObj, spaceEntity, playerEntity ):
		return bunchObj.isBigChildSpace( spaceEntity.bunchChildSpaceIndex )		#当前副本就是前一层

class ConditionBeforeIsSmall( ConditionBase ):
	"""
	前一层是小副本
	只能配在非第一层
	"""
	def check( self, bunchObj, spaceEntity, playerEntity ):
		return not bunchObj.isBigChildSpace( spaceEntity.bunchChildSpaceIndex )		#当前副本就是前一层