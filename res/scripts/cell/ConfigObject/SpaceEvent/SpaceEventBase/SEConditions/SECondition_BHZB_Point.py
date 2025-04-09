# -*- coding: utf-8 -*-

from ConfigObject.SpaceEvent.SpaceEventBase.SEConditions.SEConditionBase import SEConditionBase

class SECondition65( SEConditionBase ):
	"""
	帮会争霸 判断是否为布防副本
	"""
	def init( self, section ):
		SEConditionBase.init( self, section )
		self.isTrue = False
		if section["param1"]:
			self.isTrue = bool(int(section["param1"]))  # 填0 或者 1
		
	def check( self, spaceEntity, eventParams ):
		return bool(spaceEntity.createArgs.get("isEnterDefense",0)) == self.isTrue

SEConditionBase.setConditionClass("SECondition65", SECondition65)