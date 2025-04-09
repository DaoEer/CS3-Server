# -*- coding: utf-8 -*-
import KBEngine
from Interface.GameObject import GameObject
class NPCShop(
	KBEngine.Entity,
	GameObject,
	):
	def __init__(self):
		KBEngine.Entity.__init__(self)
		GameObject.__init__(self)
		
