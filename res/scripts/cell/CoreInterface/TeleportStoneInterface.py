# -*- coding: utf-8 -*-

"""
"""
import KBEDebug
import KBEngine
import csdefine
from LoadJsonData import g_JsonData

class TeleportStoneInterface:
	"""
	测试示例类
	"""
	def __init__(self):
		pass
		
	def CELL_onEnterTriggerRange( self, srcEntityID ):
		"""
		Exposed method
		玩家进入触发范围内
		"""
		if self.id == srcEntityID: return
		script = self.getScript()
		script.onEnterTriggerRange(self, srcEntityID)
		
	def CELL_onLeaveTriggerRange( self, srcEntityID ):
		"""
		Exposed method
		玩家离开触发范围
		"""
		if self.id == srcEntityID: return
		script = self.getScript()
		script.onLeaveTriggerRange(self, srcEntityID)
	
	
