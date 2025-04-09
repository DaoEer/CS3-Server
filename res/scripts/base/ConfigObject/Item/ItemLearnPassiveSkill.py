# -*- coding: utf-8 -*-

import ConfigObject.Item.ItemUse as ItemUse

class ItemLearnPassiveSkill(ItemUse.ItemUse):
	"""
	学习被动技能道具
	"""
	def __init__(self, srcData):
		"""
		"""
		ItemUse.ItemUse.__init__(self, srcData)