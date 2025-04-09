# -*- coding: utf-8 -*-

# 副本事件条件

from ConfigObject.SpaceEvent.SpaceEventBase.SEConditions.SEConditionBase import SEConditionBase

class SECondition50( SEConditionBase ):
	"""
	CST-6262 蟠龙秘境 是否为真的奇晶
	"""
	def init( self, section ):
		SEConditionBase.init( self, section )
		self.isTrue = int(section["param1"])  # 填0 或者 1
	
	def check( self, entity, eventParams ):
		return entity.getIsTrue() == bool(self.isTrue)

SEConditionBase.setConditionClass("SECondition50", SECondition50)

