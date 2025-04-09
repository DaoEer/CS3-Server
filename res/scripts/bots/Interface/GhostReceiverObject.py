# -*- coding: utf-8 -*-
from Interface.GameObject import GameObject
from Interface.StateInterface import StateInterface
from Interface.SkillInterface import SkillInterface
class GhostReceiverObject( GameObject, SkillInterface, StateInterface ):
	
	def __init__(self):
		GameObject.__init__( self )
		SkillInterface.__init__( self )
		StateInterface.__init__( self )
