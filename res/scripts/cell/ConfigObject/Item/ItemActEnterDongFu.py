# -*- coding: utf-8 -*-
import csdefine
import ConfigObject.Item.ItemSpell as ItemSpell
import Functions
import csstatus

class ItemActEnterDongFu( ItemSpell.ItemSpell ):
	"""
	轮回秘境  进入洞府
	"""
	def __init__(self, srcData):
		ItemSpell.ItemSpell.__init__(self, srcData)
		

	def checkUse(self, owner):
		"""
		使用前检测
		"""
		if not owner.hasDongFu():
			return csstatus.LHMJ_HAS_NOT_DONGFU
		return ItemSpell.ItemSpell.checkUse(self, owner)

	def use(self, owner, target):
		ItemSpell.ItemSpell.use(self, owner, target)
		
		
		