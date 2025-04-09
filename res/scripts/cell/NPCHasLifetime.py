# -*- coding: utf-8 -*-
#
import NPC




class NPCHasLifetime( NPC.NPC ):
	"""
	拥有生命时间的npc
	"""
	def __init__(self):
		NPC.NPC.__init__(self)
		self.delayDestroySelf()
		
		
	def delayDestroySelf(self):
		"""
		"""
		if self.lifetime>0:
			self.addTimerCallBack(self.lifetime, "destroySelf",())
