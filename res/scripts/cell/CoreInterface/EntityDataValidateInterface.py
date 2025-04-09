# -*- coding: utf-8 -*-
import csdefine
import Math
import math
import KBEngine
import KBEDebug

class EntityDataValidateInterface( object ):
	def __init__( self ):
		object.__init__( self )
		
	def validateClientCall( self, callEntityID ):
		"""
		验证玩家客户端调用自己的方法
		callEntityID:调用客户端ID
		"""
		if self.inDestroying(): #在销毁中
			return False
		
		if self.id != callEntityID:
			return False
			
		return True
	
	def validatePlayerClientCall( self, callPlayerID ):
		"""
		验证玩家客户端调用别Entity
		"""
		if self.inDestroying(): #在销毁中
			return False
			
		callPlayerEntity = KBEngine.entities.get( callPlayerID, None )
		if not callPlayerEntity:
			return
		if callPlayerEntity.getEntityFlag() != csdefine.ENTITY_FLAG_ROLE: #不是玩家
			return
			
		if not callPlayerEntity or callPlayerEntity.inDestroying(): #找不到玩家/玩家被销毁，调用无效
			return False
		
		viewRadius = (callPlayerEntity.getViewRadius() + callPlayerEntity.getViewHystArea())/math.sin(math.pi/180.0*45)
		if self.position.flatDistTo( callPlayerEntity.position ) > viewRadius: #超过视野范围，调用无效
			return False
		
		return True
	
	def validateTriggerPosition( self, triggerID, triggerPosition, validRange ):
		"""
		验证触发坐标是否正常
		triggerPosition：触发坐标点
		validRange：有准备范围
		"""
		if not self.validatePlayerClientCall( triggerID ):
			return False
			
		if self.position.distTo( triggerPosition ) > validRange:
			return False
		
		return True
			
