# -*- coding: utf-8 -*-
#
import KBEngine
import NPCTrainSoldierGround
import csdefine
import NPC
import Const

class NPCSeniorTrainSoldierGround(NPCTrainSoldierGround.NPCTrainSoldierGround):
	"""
	高级练兵场
	"""
	def __init__(self):
		self.trainGroundType = csdefine.NPCTRAINSOLDIERGROUND_TYPE_HIGH_LEVEL
		self.index = self.group
		self.lineNumber = int(self.getCurrentSpaceData( Const.SPACE_DATA_LINE_NUMBER ))
		spaceEntity = self.getCurrentSpace()
		if spaceEntity and spaceEntity.getScript().getSpaceChildType() == csdefine.SPACE_TYPE_CHILD_STAND_MAP:
			spaceEntity.addTrainSoldierGroundData(self.lineNumber,self.index,self.occupyPlayerDBID,self.occupyPlayerName, self.occupyPlayerProfession ,self.declareWarState,self.declareWarTime, self.declarePlayerName,self.declarePlayerDBID,self.declarePlayerProfession )
		
		NPC.NPC.__init__( self )
		
		self.checkDeclareTrainSoldierGround()
