# -*- coding: utf-8 -*-

# 副本事件行为
import KBEDebug
import KBEngine
from ConfigObject.SpaceEvent.SpaceEventBase.SEActions.SEActionBase import SEActionBase

class SEAction277( SEActionBase ):
	"""
	送宝任务：开始随机莫何位置
	"""
	def init ( self, section ):
		SEActionBase.init( self, section )
		
	def do( self, spaceEntity, triggerID, eventParams ):
		if spaceEntity:
			spaceEntity.initRandomCreateMoHe()

SEActionBase.setActionClass("SEAction277", SEAction277)