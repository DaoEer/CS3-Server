# -*- coding: utf-8 -*-

# 副本事件行为
import KBEDebug
import KBEngine
from ConfigObject.SpaceEvent.SpaceEventBase.SEActions.SEActionBase import SEActionBase

class SEAction288( SEActionBase ):
	"""
	藏功殿:开始答题
	"""
	def init( self, section ):
		SEActionBase.init( self, section )

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return

		spaceEntity.onStartAnswerQuestions()

SEActionBase.setActionClass("SEAction288", SEAction288)