# -*- coding: utf-8 -*-
import csdefine
import ConfigObject.Item.ItemSpell as ItemSpell

class ItemTianJiMiTu( ItemSpell.ItemSpell ):
	"""
	天机秘图 CST-12052
	"""
	def __init__(self, srcData):
		ItemSpell.ItemSpell.__init__(self, srcData)
		