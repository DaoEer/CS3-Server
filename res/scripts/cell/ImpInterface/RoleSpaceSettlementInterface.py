# -*- coding: utf-8 -*-

#玩家副本结算接口

import csdefine

class RoleSpaceSettlementInterface:
	"""
	"""
	def spaceSettlement_addEvent( self, eventList ):
		"""
		define method
		记录结算相关事件
		"""
		self.spaceSettlementEvents = eventList
	
	def spaceSettlement_clearEvent( self ):
		"""
		define method
		清除结算相关事件
		"""
		self.spaceSettlementEvents = []
	
	def onReceiveDamage( self, damage ):
		"""
		接受伤害回调
		"""
		#副本结算
		if csdefine.SPACE_STMT_RECEIVE_DAMAGE in self.spaceSettlementEvents:	#加个判断，避免每次受伤害都通知副本
			spaceEntity = self.getCurrentSpace()
			if spaceEntity:
				spaceEntity.remoteScriptCall( "spaceSettlement_onReceiveDamage", ( damage, ) )
	
	def openSpaceSettlementRewdBox( self, srcEntityID, index ):
		"""
		exposed method
		玩家打开宝箱
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		spaceEntity = self.getCurrentSpace()
		if spaceEntity:
			spaceEntity.remoteScriptCall( "spaceSettlement_openRewdBox", ( self.base, self.getName(), index ) )