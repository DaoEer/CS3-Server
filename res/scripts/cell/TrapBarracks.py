# -*- coding: utf-8 -*-

import KBEngine
import KBEDebug
from TrapBattleFlag import TrapBattleFlag
import csdefine
import csarithmetic
import csstatus

class TrapBarracks( TrapBattleFlag ):
	"""
	兵营
	"""
	def __init__( self ):
		TrapBattleFlag.__init__( self )

	def setSelfEntityFlagExt(self):
		"""
		virtual method
		"""
		self.setEntityFlagExt(csdefine.ENTITY_FLAG_EXT_TRAP_BARRACKS)

	def setBarracksBelongType( self, barracksBelongType ):
		"""
		"""
		oldBelongType = self.getBarracksBelongType()
		tempList = [csdefine.SPACE_CHILD_TYPE_GCZ, csdefine.SPACE_CHILD_TYPE_LBC, csdefine.SPACE_TYPE_CHILD_TONG_PLUNDER]
		TrapBattleFlag.setBarracksBelongType( self, barracksBelongType )
		if self.getBarracksBelongType() == csdefine.TRAP_BARRACKS_BELONG_ATTACK:	#进攻方
			spaceEntity = self.getCurrentSpace()
			if spaceEntity and spaceEntity.getScript().getSpaceChildType() in tempList:
				spaceEntity.changeRviverPosition(self.id, csdefine.TRAP_BARRACKS_BELONG_ATTACK, self.position, oldBelongType)
		elif self.getBarracksBelongType() == csdefine.TRAP_BARRACKS_BELONG_PROTECT:	#防守方
			spaceEntity = self.getCurrentSpace()
			if spaceEntity and spaceEntity.getScript().getSpaceChildType() in tempList:
				spaceEntity.changeRviverPosition(self.id, csdefine.TRAP_BARRACKS_BELONG_PROTECT, self.position, oldBelongType)
		
	def barracksReviveCheck( self, args ):
		"""
		回血检测
		"""
		if not len( self.enterIDs ):
			return
		spaceEntity = self.getCurrentSpace()
		tempList = [csdefine.SPACE_CHILD_TYPE_GCZ, csdefine.SPACE_CHILD_TYPE_LBC]
		if spaceEntity and spaceEntity.getScript().getSpaceChildType() in tempList:
			self.barracksGCZReviveCheck( args )
		elif spaceEntity and spaceEntity.getScript().getSpaceChildType() ==  csdefine.SPACE_TYPE_CHILD_TONG_PLUNDER:
			self.barracksTongPlunderReviveCheck(args)

	def barracksGCZReviveCheck( self, args ):
		"""
		攻城战回复检测
		"""
		for enterID in self.enterIDs:
			entity = KBEngine.entities.get( enterID, None )
			if not entity:
				continue
			if entity.getEntityFlag() == csdefine.ENTITY_FLAG_GHOST_RECEIVER:
				continue
			if entity.getState() != csdefine.ENTITY_STATE_FIGHT and entity.getBelongSide() == self.getBarracksBelongType() and len(entity.findBuffsByBuffID( int(args["param2"]) )) <= 0:
				entity.addBuff( entity, int(args["param2"]) )
				
	def barracksTongPlunderReviveCheck(self, args):
		"""
		帮会掠夺战回复检测
		"""
		for enterID in self.enterIDs:
			entity = KBEngine.entities.get(enterID, None)
			if entity and entity.getBelongSide() != self.getBarracksBelongType(): #兵营内有敌人，则不能回复
				return
		
		for enterID in self.enterIDs:
			entity = KBEngine.entities.get( enterID, None )
			if not entity:
				continue
			if entity.getEntityFlag() == csdefine.ENTITY_FLAG_GHOST_RECEIVER or entity.getEntityFlag() == csdefine.ENTITY_FLAG_SPELL:
				continue
			if entity.getState() != csdefine.ENTITY_STATE_FIGHT and entity.getBelongSide() == self.getBarracksBelongType() and len(entity.findBuffsByBuffID( int(args["param2"]) )) <= 0:
				entity.addBuff( entity, int(args["param2"]) )
				
	def checkCanCallArmy(self, player):
		"""
		帮会掠夺战检查是否能够更换部队
		"""
		if player.getBelongSide() != self.getBarracksBelongType(): #不同归属
			return False
		for enterID in self.enterIDs:
			entity = KBEngine.entities.get( enterID, None )
			if entity and player.isEnemyRelation(entity):
				return False
		return True

	def checkCanRevivePlayer(self, player):
		"""
		帮会掠夺战检查是否能在此战旗复活
		"""
		if player.getBelongSide() != self.getBarracksBelongType(): #不同归属
			return False
		for enterID in self.enterIDs:
			entity = KBEngine.entities.get(enterID, None)
			if entity and entity.getBelongSide() != self.getBarracksBelongType() and hasattr(entity, "getState") and entity.getState() != csdefine.ENTITY_STATE_DEAD: #兵营内有敌人
				return False
		return True
		
	def openBarracksArmyWin( self, scrEntityID ):
		"""
		打开玩家更换部队界面
		"""
		player = KBEngine.entities.get( scrEntityID )
		if player is None:
			return
			
		spaceEntity = self.getCurrentSpace()
		if spaceEntity and spaceEntity.getScript().getSpaceChildType() == csdefine.SPACE_TYPE_CHILD_TONG_PLUNDER:
			if not self.checkCanCallArmy(player):
				return
			
		if len(player.getRoleArmyDatas()) > 0:
			armyIndex = player.getDefaultArmyIndex()
			if armyIndex == -1:		#部队成员全死亡
				player.statusMessage(csstatus.BARRACKS_SOLDIER_ALL_DIE)
				return
			if player.getClient():
				player.client.CLIENT_OnOpenBarracksArmyWin(list(player.getRoleArmyDatas().values()),armyIndex)
				return
		
		tempList = [csdefine.SPACE_CHILD_TYPE_GCZ,]
		if spaceEntity and spaceEntity.getScript().getSpaceChildType() in tempList:
			roleDefaultArmyDatas = spaceEntity.getRoleDefaultArmyData( player )
			armyIndex = spaceEntity.getGCZRoleDefultArmyIndex( player )
			if player.getClient():
				player.client.CLIENT_OnOpenBarracksArmyWin( roleDefaultArmyDatas,armyIndex )
