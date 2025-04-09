# -*- coding: utf-8 -*-
from Interface.GameObject import GameObject
from Interface.EntitySpaceEventInterface import EntitySpaceEventInterface
from Interface.StateInterface import StateInterface
from Interface.SkillInterface import SkillInterface
	
class NPCBaseObject( GameObject, EntitySpaceEventInterface ):
	def __init__( self ):
		GameObject.__init__(self)		
		EntitySpaceEventInterface.__init__(self)
		
	def getFinalCamp( self ):
		"""
		获取最终阵营：有临时阵营则返回临时阵营，否则返回原阵营
		"""
		if self.tempCamp:
			return self.tempCamp
		return self.camp
		
	def CLIENT_StartMoveJump( self ):
		pass
	def CLIENT_EndMoveJump( self ):
		pass
		
class SpellObject( NPCBaseObject,
				SkillInterface,
				StateInterface,
				 ):
	def __init__( self ):
		NPCBaseObject.__init__(self)
		SkillInterface.__init__(self)
		StateInterface.__init__(self)
	
