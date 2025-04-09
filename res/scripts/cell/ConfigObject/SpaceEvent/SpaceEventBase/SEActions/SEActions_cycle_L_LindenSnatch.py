# -*- coding: utf-8 -*-

# 副本事件行为
import KBEDebug
import KBEngine
from ConfigObject.SpaceEvent.SpaceEventBase.SEActions.SEActionBase import SEActionBase

class SEAction276( SEActionBase ):
	"""
	送宝任务：开始随机本体与分身位置
	"""
	def init ( self, section ):
		SEActionBase.init( self, section )
		
	def do( self, spaceEntity, triggerID, eventParams ):
		if spaceEntity:
			spaceEntity.initRandomCreateXTDL()

SEActionBase.setActionClass("SEAction276", SEAction276)