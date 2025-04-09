# -*- coding: utf-8 -*-

# 副本事件行为
import KBEMath
import KBEDebug
import KBEngine
from ConfigObject.SpaceEvent.SpaceEventBase.SEActions.SEActionBase import SEActionBase
import csdefine
import csstatus

class SEAction420( SEActionBase ):
	"""
	试炼之地 随机顺序播放石板
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self._effect = section["param1"]
		self._amount = int(section["param2"])
		self._intervalTime = float(section["param3"])

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		spaceEntity.randomFlagstonePlayEffect(self._effect, self._amount, self._intervalTime)
		


SEActionBase.setActionClass("SEAction420", SEAction420)