# -*- coding: utf-8 -*-

# 急速穿梭 副本事件行为
import KBEDebug
import KBEngine
from ConfigObject.SpaceEvent.SpaceEventBase.SEActions.SEActionBase import SEActionBase

class SEAction308( SEActionBase ):
	"""
	灵气迷宫 显示箭头划过效果
	"""
	def init ( self, section ):
		SEActionBase.init( self, section )
		
	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		for roleCell in spaceEntity._spaceRoles:
			roleCell.client.OnArrowCrossoverEffect()

SEActionBase.setActionClass("SEAction308", SEAction308)