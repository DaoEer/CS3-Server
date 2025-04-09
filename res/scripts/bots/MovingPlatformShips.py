# -*- coding: utf-8 -*-
import KBEngine
from Interface.GameObject import GameObject
from Interface.NPCAmbulantInterface import NPCAmbulantInterface
class MovingPlatformShips(KBEngine.Entity, 
	NPCAmbulantInterface, 
	GameObject, ):
	def __init__(self):
		KBEngine.Entity.__init__(self)
		GameObject.__init__(self)
		NPCAmbulantInterface.__init__(self)
		
