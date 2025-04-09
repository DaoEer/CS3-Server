# -*- coding: utf-8 -*-

# 副本事件行为
import KBEDebug
import KBEngine
from ConfigObject.SpaceEvent.SpaceEventBase.SEActions.SEActionBase import SEActionBase

class SEAction319( SEActionBase ):
	"""
	冥气人参果 通知开始刷人参果
	"""
	def init( self, section ):
		SEActionBase.init( self, section )

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		for player in spaceEntity._spaceRoles:
			if player.getClient():
				player.client.InitRefreshCiku( spaceEntity.cikuCoordXList, spaceEntity.cikuCoordYList, spaceEntity.cikuCoordZList )
				player.client.InitRefreshNormalCiku( spaceEntity.cikuCoordXList1, spaceEntity.cikuCoordYList1, spaceEntity.cikuCoordZList1 )

class SEAction320( SEActionBase ):
	"""
	冥气人参果 通知开始爆发冥气
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.initialValue = int( section["param1"] )
		self.radius = float(section["param2"])
		self.time = float(section["param3"])
		self.epsilon = int(section["param4"])

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		for player in spaceEntity._spaceRoles:
			if player.getClient():
				player.client.StartSendOutGhostGas( self.initialValue, self.radius, self.time, self.epsilon )

SEActionBase.setActionClass("SEAction319", SEAction319)
SEActionBase.setActionClass("SEAction320", SEAction320)