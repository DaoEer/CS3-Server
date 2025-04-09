# -*- coding: utf-8 -*-

# 副本事件行为
import KBEMath
import KBEDebug
import KBEngine
from ConfigObject.SpaceEvent.SpaceEventBase.SEActions.SEActionBase import SEActionBase
import csdefine
import cschannel_msgs
import csstatus

class SEAction388( SEActionBase ):
	"""
	通天塔通关成功
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.questID = int( section["param1"] )
		self.taskID = int( section["param2"] )
		self.lastLayerNumber = int( section["param3"])

	def do( self, spaceEntity, triggerID, eventParams ):
		spaceEntity.getScript().onTongTinaDaSpaceSuccess( spaceEntity, self.questID, self.taskID, self.lastLayerNumber )

class SEAction389( SEActionBase ):
	"""
	通天塔通关失败
	"""
	def init( self, section ):
		SEActionBase.init( self, section )

	def do( self, spaceEntity, triggerID, eventParams ):
		spaceEntity.getScript().onTongTinaDaSpaceFailure( spaceEntity )

SEActionBase.setActionClass("SEAction388", SEAction388)
SEActionBase.setActionClass("SEAction389", SEAction389)