# -*- coding: utf-8 -*-

import KBEDebug
from SpaceCopy import SpaceCopy
import csdefine
import copy
import Math
import time
import KBEngine
import csarithmetic
from MsgLogger import g_logger
import LogDefine

class SpaceCopyAttackCityWar( SpaceCopy ):
	"""
	攻城战 CST-8954
	"""
	def __init__( self ) :
		SpaceCopy.__init__( self )
		self.roleDefaultArmyDatas = {}
		self.revivePosInfos = []
		self.recordNotOccupyBarracks = {}
		self.recordRoleReviveData = {}
		self.recordBossCmdSoldierIDs = {}  # 记录Boss 带领的小兵
		self.recordRoleCalledArmy = {}	#记录玩家在此副本召唤的部队的索引 {dbid:armyIndex}

	def getAerialLadderOccurInfo( self, pos ):
		"""
		获得云梯搭建的信息
		"""
		aerialLadderPosDict = copy.copy(self.getScript().getAerialLadderPosInfo())
		for index in self.recordAerialLadderOccurIndexList:
			if index in aerialLadderPosDict:
				del aerialLadderPosDict[index]
		
		recordIndex = []
		recordDis = []
		for index, aerialLadderPos in aerialLadderPosDict.items():
			recordIndex.append(index)
			dis = Math.Vector3(aerialLadderPos).flatDistTo( pos )
			recordDis.append( dis )

		dis = min( recordDis )
		number = recordDis.index(dis)
		index = recordIndex[number]
		return index, aerialLadderPosDict[index]

	def addAerialLadderPosIndex( self, index ):
		"""
		增加云梯已搭建的位置
		"""
		if index not in self.recordAerialLadderOccurIndexList:
			self.recordAerialLadderOccurIndexList.append( index )

	def removeAerialLadderPosIndex( self, index ):
		"""
		"""
		if index in self.recordAerialLadderOccurIndexList:
			self.recordAerialLadderOccurIndexList.remove(index)

	def getAerialLadderUpPosByIndex( self, index ):
		"""
		获得云梯上方对应的坐标
		"""
		if index in self.getScript().getAerialLadderUpPosInfo():
			return self.getScript().getAerialLadderUpPosInfo()[index]
		return None

	def getGCZRoleDefultArmyData( self, playerDBID, id ):
		"""
		获得攻城战的默认部队数据
		"""
		if playerDBID in self.roleDefaultArmyDatas and id < len( self.roleDefaultArmyDatas[playerDBID] ):
			return self.roleDefaultArmyDatas[playerDBID][id]
		return None

	def getGCZRoleDefultArmyIndex( self, role ):
		"""
		获得玩家某个默认部队数据
		"""
		if role.playerDBID not in self.roleDefaultArmyDatas:
			return -1

		for armyData in self.roleDefaultArmyDatas[role.playerDBID]:
			if armyData.firstGuardScriptID or armyData.secondGuardScriptID or armyData.soldierIDs:
				return armyData.id
		return -1

	def getRrecordBossNameBySoldierID( self, soldierID ):
		"""
		通过士兵ID获得bossID 
		"""
		for bossName, soldierIDs in self.recordBossCmdSoldierIDs.items():
			if soldierID in soldierIDs:
				return bossName
		return -1

	def recordOpterationMachine(self, id):
		"""记录被操作的器械"""
		self.machineWarList.append(id)
		
	def removeOpterationMachine(self, id):
		"""移除被操作的器械"""
		if id in self.machineWarList:
			self.machineWarList.remove(id)

	def addEntityMailBoxRecord( self, scriptID, entityMailBox ):
		"""
		增加entityMailBox 记录
		"""
		SpaceCopy.addEntityMailBoxRecord( self, scriptID, entityMailBox )
		self.getScript().addEntityMailBoxRecord( self,scriptID, entityMailBox )
		if entityMailBox.getEntityFlagExt() == csdefine.ENTITY_FLAG_EXT_TRAP_BATTLEFLAG:
			entityMailBox.setBarracksBelongType( csdefine.TRAP_BARRACKS_BELONG_PROTECT )
		if entityMailBox.getEntityFlagExt() == csdefine.ENTITY_FLAG_EXT_TRAP_BARRACKS:
			entityMailBox.setBarracksBelongType( csdefine.TRAP_BARRACKS_BELONG_PROTECT )
			if entityMailBox.id not in self.recordNotOccupyBarracks:
				self.recordNotOccupyBarracks[entityMailBox.id] = entityMailBox.position

		if entityMailBox.getEntityFlag() != csdefine.ENTITY_FLAG_ROLE and entityMailBox.scriptID in self.getScript().getBelongAttackScriptIDs():
			entityMailBox.setBelongSide( csdefine.BELONG_SIDE_ATTACK )
		if entityMailBox.getEntityFlag() != csdefine.ENTITY_FLAG_ROLE and entityMailBox.scriptID in self.getScript().getBelongProtectScriptIDs():
			entityMailBox.setBelongSide( csdefine.BELONG_SIDE_PROTECT )

		if scriptID in self.getScript().getNotReviveBossScriptID():
			if entityMailBox.getUname() not in self.recordBossCmdSoldierIDs:
				self.recordBossCmdSoldierIDs[entityMailBox.getUname()] = []

		if entityMailBox.getEntityFlagExt() == csdefine.ENTITY_FLAG_EXT_MONSTER_SOLDIER:
			cmder =entityMailBox.getCmder()
			if not cmder:
				return
			if cmder.getUname() in self.recordBossCmdSoldierIDs:
				self.recordBossCmdSoldierIDs[cmder.getUname()].append( entityMailBox.id )

	def addGCZMember( self, id,mailBox,name, belongSide, protectName, attackName ):
		"""
		增加攻城战成员
		"""
		self.GCZMemberDatas.addMember( id,mailBox,name, belongSide, protectName, attackName )

	def getRoleRecordCallArmy( self, dbid ):
		"""
		获取玩家召唤的部队记录
		"""
		return self.recordRoleCalledArmy.get( dbid, -1 )

	def updateRoleRecordCallArmy( self, dbid, armyIndex ):
		"""
		更新玩家召唤的部队记录
		"""
		self.recordRoleCalledArmy[dbid] = armyIndex

	def changeRviverPosition( self, entityID, belongType, position, oldBelongType ):
		"""
		增加复活信息
		"""
		if belongType == csdefine.TRAP_BARRACKS_BELONG_ATTACK:
			self.revivePosInfos.append(position)

	def getRevivePosition( self, role ):
		"""
		获取副本动态复活点
		"""
		if not len(self.revivePosInfos):
			return role.position
		positionList = []
		for revivePosInfo in self.revivePosInfos:
			positionList.append( revivePosInfo )

		distList = []
		for position in positionList:
			dist = position.flatDistTo( role.position )
			distList.append(dist)
		minDist = min(distList)
		index = distList.index(minDist)

		position = csarithmetic.getPositionByCircular( positionList[index],self.getScript().getReviveRadius() )
		return position

	def onMonsterBeKill( self, killEntity, dieEntity, range ):
		"""
		小怪或者Boss被击杀
		"""
		if dieEntity.getEntityFlagExt() == csdefine.ENTITY_FLAG_EXT_MONSTER_COMMANDER: #将领被击杀
			# id = dieEntity.id
			# if dieEntity.scriptID in self.getScript().getNotReviveBossScriptID():
			# 	id = 0
			member = self.GCZMemberDatas.getMemberByName( dieEntity.getUname() )
			if member:
				self.GCZMemberDatas.addMemberDeadNum( member.roleDBID )
			#self.reviveBoss( dieEntity )
			if killEntity.getEntityFlagExt() == csdefine.ENTITY_FLAG_EXT_ROLE: # 玩家击杀奖领
				self.GCZMemberDatas.addMemberKillEnemyNum( killEntity.playerDBID )
				#self.searchKillBossAssistsMembers( killEntity.id, dieEntity, range ) 	# CST-11481 删除助攻
			elif killEntity.getEntityFlagExt() == csdefine.ENTITY_FLAG_MONSTER_CTRL_BY_CLIENT: #如果是玩家带领的小兵
				id = self.GCZMemberDatas.getIDByEntityID( killEntity.controlEntityID )
				self.GCZMemberDatas.addMemberKillEnemyNum(id)
				#self.searchKillBossAssistsMembers( killEntity.controlledBy.id, dieEntity, range )

		elif dieEntity.getEntityFlagExt() == csdefine.ENTITY_FLAG_EXT_MONSTER_SOLDIER: #将领带领的小怪被击杀
			bossName = self.getRrecordBossNameBySoldierID( dieEntity.id )
			member = self.GCZMemberDatas.getMemberByName( bossName )
			if member:
				self.GCZMemberDatas.addMemberSoldierDeadNum(member.roleDBID)

			if killEntity.getEntityFlagExt() == csdefine.ENTITY_FLAG_EXT_ROLE:
				self.GCZMemberDatas.addMemberKillSoldierNum( killEntity.playerDBID )
			elif killEntity.getEntityFlagExt() == csdefine.ENTITY_FLAG_MONSTER_CTRL_BY_CLIENT: #如果是玩家带领的小兵
				id = self.GCZMemberDatas.getIDByEntityID( killEntity.controlEntityID )
				self.GCZMemberDatas.addMemberKillSoldierNum( id )

		elif dieEntity.getEntityFlagExt() == csdefine.ENTITY_FLAG_MONSTER_CTRL_BY_CLIENT: # 玩家带领的小怪被击杀
			id = self.GCZMemberDatas.getIDByEntityID( dieEntity.controlEntityID )
			self.GCZMemberDatas.addMemberSoldierDeadNum(id)
			if killEntity.getEntityFlagExt() == csdefine.ENTITY_FLAG_EXT_MONSTER_SOLDIER:
				bossName = self.getRrecordBossNameBySoldierID( killEntity.id )
				member = self.GCZMemberDatas.getMemberByName( bossName )
				if member:
					self.GCZMemberDatas.addMemberKillSoldierNum( member.roleDBID )

			elif killEntity.getEntityFlagExt() == csdefine.ENTITY_FLAG_EXT_MONSTER_COMMANDER:
				member = self.GCZMemberDatas.getMemberByName( killEntity.getUname() )
				if member:
					self.GCZMemberDatas.addMemberKillSoldierNum( member.roleDBID )
			elif killEntity.getEntityFlag() == csdefine.ENTITY_FLAG_MONSTER and killEntity.scriptID in self.getScript().getCommonMonsterScriptIDs() or killEntity.scriptID in self.getScript().getQiXieScriptIDs():
				self.GCZMemberDatas.addMemberKillSoldierNum( 0 )

		elif dieEntity.scriptID in self.getScript().getCommonMonsterScriptIDs():
			self.GCZMemberDatas.addMemberSoldierDeadNum(0)
			if killEntity.getEntityFlagExt() == csdefine.ENTITY_FLAG_EXT_ROLE:
				self.GCZMemberDatas.addMemberKillSoldierNum( killEntity.playerDBID )
			elif killEntity.getEntityFlagExt() == csdefine.ENTITY_FLAG_MONSTER_CTRL_BY_CLIENT: #如果是玩家带领的小兵
				id = self.GCZMemberDatas.getIDByEntityID( killEntity.controlEntityID )
				self.GCZMemberDatas.addMemberKillSoldierNum( id )

		elif dieEntity.scriptID in self.getScript().getQiXieScriptIDs():
			self.GCZMemberDatas.addMemberDeadNum(0)
			if killEntity.getEntityFlagExt() == csdefine.ENTITY_FLAG_EXT_ROLE:
				self.GCZMemberDatas.addMemberKillEnemyNum( killEntity.playerDBID )
			elif killEntity.getEntityFlagExt() == csdefine.ENTITY_FLAG_MONSTER_CTRL_BY_CLIENT: #如果是玩家带领的小兵
				id = self.GCZMemberDatas.getIDByEntityID( killEntity.controlEntityID )
				self.GCZMemberDatas.addMemberKillEnemyNum( id )

	def searchKillBossAssistsMembers( self, killId, dieEntity, range ):
		"""
		搜索获得助攻数据的成员
		"""
		entitys = dieEntity.entitiesInRangeExtCircle( range )
		assistsIDs = []
		for entity in entitys:
			if entity.getEntityFlagExt() == csdefine.ENTITY_FLAG_MONSTER_CTRL_BY_CLIENT and entity.controlledBy.id != killId and entity.id in dieEntity.damageList.keys():
				if entity.controlledBy.id not in assistsIDs:
					assistsIDs.append( entity.controlledBy.id )
			if entity.getEntityFlagExt() == csdefine.ENTITY_FLAG_EXT_ROLE and entity.id != killId and entity.id in dieEntity.damageList.keys():
				if entity.id not in assistsIDs:
					assistsIDs.append(entity.id)
		for assistsID in assistsIDs:
			id = self.GCZMemberDatas.getIDByEntityID( assistsID )
			self.GCZMemberDatas.addMemberAssistsNum( id )

	def onRoleBeKill( self, killEntity, dieEntity, range ):
		"""
		玩家被击杀
		"""
		self.GCZMemberDatas.addMemberDeadNum( dieEntity.playerDBID )
		if killEntity.getEntityFlagExt() == csdefine.ENTITY_FLAG_EXT_MONSTER_COMMANDER:
			member = self.GCZMemberDatas.getMemberByName( killEntity.getUname() )
			if member:
				self.GCZMemberDatas.addMemberKillEnemyNum( id )
			#self.searchKillRoleAssistsMembers( killEntity.id, dieEntity, range )

		elif killEntity.getEntityFlagExt() == csdefine.ENTITY_FLAG_EXT_MONSTER_SOLDIER:
			bossName = self.getRrecordBossNameBySoldierID( killEntity.id )
			member = self.GCZMemberDatas.getMemberByName( bossName )
			if member:
				self.GCZMemberDatas.addMemberKillEnemyNum( member.roleDBID )

		elif killEntity.getEntityFlag() == csdefine.ENTITY_FLAG_MONSTER and (killEntity.scriptID in self.getScript().getCommonMonsterScriptIDs() or killEntity.scriptID in self.getScript().getQiXieScriptIDs()):
			self.GCZMemberDatas.addMemberKillEnemyNum(0)


	def searchKillRoleAssistsMembers( self, killId, dieEntity, range ):
		"""
		搜索获得助攻数据的成员
		"""
		entitys = dieEntity.entitiesInRangeExtCircle( range )
		assistsIDs = []
		for entity in entitys:
			if entity.getEntityFlagExt() == csdefine.ENTITY_FLAG_EXT_MONSTER_COMMANDER and entity.id != killId and entity.id in dieEntity.damageList.keys():
				id = entity.id
				if entity.scriptID in self.getScript().getNotReviveBossScriptID():
					id = 0
				if id not in assistsIDs:
					assistsIDs.append(id)
			if entity.getEntityFlagExt() == csdefine.ENTITY_FLAG_EXT_MONSTER_SOLDIER and entity.getCmder() and entity.getCmder().id != killId and entity.id in dieEntity.damageList.keys():
				id = entity.getCmder().id
				if entity.getCmder().scriptID in self.getScript().getNotReviveBossScriptID():
					id = 0
				if id not in assistsIDs:
					assistsIDs.append( id )
		for id in assistsIDs:
			self.GCZMemberDatas.addMemberAssistsNum( id )

	def setGCZIsWin( self, isWin ):
		"""
		设置攻城战是否胜利
		"""
		self.isWin = isWin
		self.showGCZSettlementWnd()

	def showGCZSettlementWnd( self ):
		"""
		"""
		self.destroyEntity()
		members = self.GCZMemberDatas.getMembersBySide( csdefine.BELONG_SIDE_ATTACK )
		useTime = int(time.time() - self.lifeStartTime)
		for m in members:
			if m.roleMB and m.roleMB.getClient():
				m.roleMB.client.CLIENT_ShowGCZSettlementWnd( self.isWin, useTime, self.getScript().delyCloseTime )

		if self.isWin:
			action_status = LogDefine.ACTIVE_STATE_TYPE_SUCCESS
		else:
			action_status = LogDefine.ACTIVE_STATE_TYPE_FAIL
		for role in self._spaceRoles:
			g_logger.roleActiveRecord( LogDefine.ACTIVE_SPACE_TYPE_DEFAULT,role.accountDBID,role.playerDBID,role.getLevel(),
			"","",self.lifeStartTime, useTime,action_status,self.scriptID)

	def destroyEntity( self ):
		"""
		"""
		entitysList = copy.copy( list(self.getAllEntityRecord().values()) ) 
		for entityIDs in entitysList:
			for entityID in entityIDs:
				entity = KBEngine.entities.get( entityID, None)
				if entity and entity.getEntityFlagExt() != csdefine.ENTITY_FLAG_MONSTER_CTRL_BY_CLIENT:
					entity.destroySelf()

	def removeRecordNotOccupyBarracks( self, entityID ):
		"""
		移除被占领的兵营
		"""
		if entityID in self.recordNotOccupyBarracks:
			del self.recordNotOccupyBarracks[entityID]

	def getRecordNotOccupyBarracks( self, entityID ):
		"""
		获得未被占领的兵营
		"""
		if entityID in self.recordNotOccupyBarracks:
			return self.recordNotOccupyBarracks[entityID]
		return None

	def getAllNotOccupyBarracks( self ):
		"""
		"""
		return self.recordNotOccupyBarracks

	def removeRoleArmyDefaultData( self, role, callIndex, soldierType, scriptID, id ):
		"""
		移除玩家副本默认部队数据
		"""
		if role.playerDBID not in self.roleDefaultArmyDatas:
			return

		roleDefaultArmyData = self.roleDefaultArmyDatas[role.playerDBID][callIndex]
		if soldierType == csdefine.BARRACKS_SOLDIER_GUARD_TYPE:
			if roleDefaultArmyData.firstGuardScriptID == scriptID:
				roleDefaultArmyData.firstGuardScriptID = ""
			elif roleDefaultArmyData.secondGuardScriptID == scriptID:
				roleDefaultArmyData.secondGuardScriptID = ""
		elif soldierType == csdefine.BARRACKS_SOLDIER_COMMON_TYPE:
			if roleDefaultArmyData.soldierScriptID == scriptID and id in roleDefaultArmyData.soldierIDs:
				roleDefaultArmyData.soldierIDs.remove(id)

	def getRoleDefaultArmyData( self, role ):
		"""
		"""
		if role.playerDBID in self.roleDefaultArmyDatas:
			return self.roleDefaultArmyDatas[role.playerDBID]
		return []

	def reviveBoss( self, dieEntity ):
		"""
		boss复活
		"""
		if dieEntity.scriptID in self.getScript().getReviveBossScriptID():
			notOccupyBarracks =self.getAllNotOccupyBarracks()
			posList = list( notOccupyBarracks.values() )
			if not len( posList ):
				return
			dists = []
			for pos in posList:
				dist = dieEntity.position.flatDistTo( pos )
				dists.append( dist )

			dist = min( dists )
			index = dists.index(dist)
			pos = posList[index]
			scriptID = dieEntity.scriptID
			self.addTimerCallBack( self.getScript().getBossReviveTime(),"createEntityByScriptID",( scriptID,pos,Math.Vector3(0,0,0),{} ) )

	def addRecordRoleReviveNum( self, playerDBID ):
		"""
		增加记录玩家复活次数
		"""
		if playerDBID not in self.recordRoleReviveData:
			self.recordRoleReviveData[playerDBID] = (0,0) #（复活次数，下次复活时间）
		reviveNum, tempNextReviveTime = self.recordRoleReviveData[playerDBID]
		self.recordRoleReviveData[playerDBID] = ( reviveNum+1,tempNextReviveTime )

	def updateRoleNextReviveTime( self, playerDBID, nextReviveTime ):
		"""
		更新玩家下次复活的时间
		"""
		if playerDBID not in self.recordRoleReviveData:
			self.recordRoleReviveData[playerDBID] = (0,0)
		reviveNum, tempNextReviveTime = self.recordRoleReviveData[playerDBID]
		self.recordRoleReviveData[playerDBID] = ( reviveNum,nextReviveTime )

	def getRecordRoleReviveData( self, playerDBID ):
		"""
		获得玩家复活数据次数
		"""
		if playerDBID in self.recordRoleReviveData:
			return self.recordRoleReviveData[playerDBID]

		return 0,0

