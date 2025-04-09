# -*- coding: utf-8 -*-
import KBEngine
import KBEDebug

from PlayerAI.Base.AIBase import AIBase

class OldAI( AIBase ):
	"""
	旧的AI对接进来
	"""
	def __init__(self):
		AIBase.__init__(self)
		
	def attache(self, owner):
		"""
		"""
		AIBase.attache(self, owner)
		KBEngine.callback( 3, self.owner.initBehaviour )
		self.owner.reset()

AIBase.setClass("OldAI", OldAI)		
	