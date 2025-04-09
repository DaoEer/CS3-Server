# -*- coding: utf-8 -*-
# 副本事件行为
import KBEDebug
import KBEngine
from ConfigObject.SpaceEvent.SpaceEventBase.SEActions.SEActionBase import SEActionBase

class SEAction240( SEActionBase ):
	"""
	环任务副本 巧取熔岩晶--对道具进行充能
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.itemID = int( section["param1"] )		# 物品ID
		self.count = int( section["param2"] )		# 数量

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		for e in spaceEntity._spaceRoles:
			itemInstList = e.getItemInstsByID( self.itemID )
			for itemInst in itemInstList:
				itemInst.addUseNumber( self.count, e )

class SEAction342( SEActionBase ):
	"""
	环任务副本 巧取熔岩晶--修改副本的辅助模式
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
	
	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		for e in spaceEntity._spaceRoles:
			e.client.ModifySwitchHomingSpellAtt()

SEActionBase.setActionClass("SEAction240", SEAction240)
SEActionBase.setActionClass("SEAction342", SEAction342)