# -*- coding: utf-8 -*-

#急速穿梭 副本事件条件

from ConfigObject.SpaceEvent.SpaceEventBase.SEConditions.SEConditionBase import SEConditionBase

class SECondition51( SEConditionBase ):
	"""
	CST-6021 急速穿梭:副本传送门是否封锁
	"""
	def init( self, section ):
		SEConditionBase.init( self, section )
		self._isTrue = bool(int(section["param1"]))  # 填0 或者 1
		
	def check( self, spaceEntity, eventParams ):
		return spaceEntity.isCloseDoor == self._isTrue

SEConditionBase.setConditionClass("SECondition51", SECondition51)