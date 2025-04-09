# -*- coding: utf-8 -*-

#common
import KBEDebug
#cell
import ConfigObject.Item.ItemUse as ItemUse
#data
import csstatus


class ItemSpellPosAndDirAssist(ItemUse.ItemUse):
	"""
	玩家可以手动调整怪物刷出的 位置 和 朝向
	"""
	def __init__(self, srcData):
		"""
		"""
		ItemUse.ItemUse.__init__(self, srcData)
