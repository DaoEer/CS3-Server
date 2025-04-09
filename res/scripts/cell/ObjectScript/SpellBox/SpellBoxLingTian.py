# -*- coding: utf-8 -*-

import csdefine
import KBEDebug
import KBEngine
from SmartImport import smartImport
from ObjectScript.SpellBox import SpellBox
import csstatus

class SpellBoxLingTian( SpellBox.SpellBox ):
	"""
	灵田
	"""
	def __init__( self ):
		SpellBox.SpellBox.__init__( self )
		self.skillList = []

	def initData( self, data ):
		"""
		初始化数据
		@param data: dict
		"""
		SpellBox.SpellBox.initData( self, data )
		self.setEntityProperty( "lingTianNum", int(data["Param1"]) )
		if data["Param2"]:
			self.skillList = [ int(i) for i in data["Param2"].split("|") ]
			
	def __checkGossipCondition( self, selfCell, playerEntity ):
		"""
		检测交互条件
		"""
		for obj in self.gossipConditions:
			if not obj.check( selfCell, playerEntity ):
				return False
		return True
		
	def gossipWithForwardCB( self, selfCell, playerEntity ):
		"""
		玩家交互
		"""
		if not self.__checkGossipCondition( selfCell, playerEntity ):
			return
			
		if not self.canMountPetGossip and playerEntity.isMountOnPet():
			playerEntity.transformPet( playerEntity.id )
			
		state_ = selfCell.getPlantState()
		if state_ > len(self.skillList) - 1:
			KBEDebug.ERROR_MSG( "SpellBox::gossipWith:Can't found skill by entity %i!" % self.id )
			return
		playerEntity.useSkillToEntityFC( playerEntity.id, self.skillList[state_], selfCell.id )
