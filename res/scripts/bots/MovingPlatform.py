# -*- coding: utf-8 -*-
from Interface.GameObject import GameObject
from Interface.NPCAmbulantInterface import NPCAmbulantInterface
from Monster import Monster
class MovingPlatform( Monster ,
	NPCAmbulantInterface,
	GameObject,
	):
	pass
