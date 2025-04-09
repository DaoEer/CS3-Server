# -*- coding: utf-8 -*-
#
import Math
import time
import KBEngine
import KBEDebug
import csdefine
import SpellBoxSpecial


class SpellBoxHit( SpellBoxSpecial.SpellBoxSpecial ):
	"""
	支持碰撞开门物件
	"""
	def __init__(self):
		SpellBoxSpecial.SpellBoxSpecial.__init__(self)