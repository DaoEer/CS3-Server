# -*- coding: utf-8 -*-
import csdefine
import ConfigObject.Item.ItemUse as ItemUse

class ItemMysteriousBox( ItemUse.ItemUse ):
	"""
	神秘宝盒
	"""
	def __init__(self, srcData):
		ItemUse.ItemUse.__init__(self, srcData)
		