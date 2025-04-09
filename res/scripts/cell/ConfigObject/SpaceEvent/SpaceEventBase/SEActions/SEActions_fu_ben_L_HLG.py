# -*- coding: utf-8 -*-

# 副本事件行为
import KBEMath
import KBEDebug
import KBEngine
from ConfigObject.SpaceEvent.SpaceEventBase.SEActions.SEActionBase import SEActionBase

class SEAction322( SEActionBase ):
	"""
	浩灵谷副本内所有玩家播放指定镜头	
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.failSceneID  = section["param1"]
		self.successSceneID = section["param2"]
		self.qteNum = int(section["param3"])
	
	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		for num in spaceEntity.completeQTENum.values():
			if num != self.qteNum:
				for e in spaceEntity._spaceRoles:
					e.client.StartPlayStory( self.failSceneID, 1 )
				return

		for e in spaceEntity._spaceRoles:
			e.client.StartPlayStory( self.successSceneID, 1 )

SEActionBase.setActionClass("SEAction322", SEAction322)
