# -*- coding: utf-8 -*-
#
import Math
import time
import KBEngine
import KBEDebug
import csdefine
import SpellBoxSpecial


class SpellBoxDoor( SpellBoxSpecial.SpellBoxSpecial ):
	"""
	支持某体积形状范围内检测开门
	"""
	def __init__(self):
		SpellBoxSpecial.SpellBoxSpecial.__init__(self)