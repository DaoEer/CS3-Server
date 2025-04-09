# -*- coding: utf-8 -*-

# 副本事件行为
import KBEMath
import KBEDebug
import KBEngine
from ConfigObject.SpaceEvent.SpaceEventBase.SEActions.SEActionBase import SEActionBase

class SEAction357( SEActionBase ):
	"""
	禁地采药：随机位置刷新灵仙草	
	"""
	def __init__( self ):
		SEActionBase.__init__( self )
		self._amount = 1

	def init( self, section ):
		SEActionBase.init( self, section )
		if section["param1"]:
			self._amount  = int(section["param1"])
	
	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		spaceEntity.randomRefreshXLC(self._amount)

class SEAction358( SEActionBase ):
	"""
	禁地采药：灵仙草销毁	
	"""
	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		trigger = KBEngine.entities.get(triggerID,None)
		if not trigger:
			return
		spaceEntity.onDestoryXLC(trigger.scriptID)


SEActionBase.setActionClass("SEAction357", SEAction357)
SEActionBase.setActionClass("SEAction358", SEAction358)
