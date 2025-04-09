# -*- coding: utf-8 -*-

import SpellBox

class SpellBoxHasCreator( SpellBox.SpellBox ):
	"""
	专属SpellBox
	"""
	def __init__(self):
		SpellBox.SpellBox.__init__(self)