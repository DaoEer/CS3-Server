# -*- coding: utf-8 -*-

import KBEDebug
import ConfigObject.Item.Equip as Equip

class Armor(Equip.Equip):
	"""
	防具基类
	"""
	def __init__(self, srcData):
		Equip.Equip.__init__(self, srcData)