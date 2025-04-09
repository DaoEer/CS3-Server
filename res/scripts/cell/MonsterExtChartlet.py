# -*- coding: utf-8 -*-

import KBEngine
import KBEDebug
import csdefine

import Monster



class MonsterExtChartlet(Monster.Monster):
	"""
	画卷贴图，CST-3790
	"""
	def __init__(self):
		"""
		"""
		Monster.Monster.__init__(self)

	def displayChartlet(self, effectID):
		"""
		贴图显示
		"""
		self.allClients.onDisplayChartlet(effectID,)
		
	def disappearChartlet(self, disappearType):
		"""
		贴图消失
		@param1 disappearType: 消失类型， 1 逐渐消失，2 扭成一团然后消失
		"""
		self.allClients.onDisappearChartlet(disappearType,)
		
	def onDestroyChartlet(self, exposed):
		"""
		<exposed method>
		贴图销毁
		"""
		self.destroySelf()