# -*- coding: utf-8 -*-

import random
import KBEDebug
from SpaceCopy import SpaceCopy
import Math
import math
import KBEngine
import csdefine
import csstatus
import Const
import time
import KBEMath
import Functions

class SpaceCopyTrainingGround( SpaceCopy ):
	"""
	练兵场
	"""
	def __init__( self ) :
		SpaceCopy.__init__( self )
		self.belongDBID = self.createArgs.get( "belongDBID",0 )						# 归宿玩家DBID
		self.isCopyOver = False							# 副本结束
		self.teleportTime = 0
		self.barrackInfo= {}							# 兵营据点等信息{ belongSide : { scriptID : pos},}
		self.barrackInfo[csdefine.TRAP_BARRACKS_BELONG_ATTACK] = {}
		self.barrackInfo[csdefine.TRAP_BARRACKS_BELONG_PROTECT] = {}
		self.batteryInfo = {}							# 器械等信息 { entityID : [scriptID, state, pos] }
		self.recordRoleCalledArmy = {}	#记录玩家在此副本召唤的部队的索引 {dbid:armyIndex}

	def addEntityMailBoxRecord( self, scriptID, entityMailBox ):
		"""
		增加entityMailBox 记录
		"""
		SpaceCopy.addEntityMailBoxRecord( self, scriptID, entityMailBox )
		if entityMailBox.getEntityFlagExt() == csdefine.ENTITY_FLAG_EXT_TRAP_BATTLEFLAG:
			entityMailBox.setBarracksBelongType( csdefine.TRAP_BARRACKS_BELONG_PROTECT )

		if entityMailBox.getEntityFlag() != csdefine.ENTITY_FLAG_ROLE and entityMailBox.scriptID in self.getScript().getBelongAttackScriptIDs():
			if entityMailBox.getEntityFlagExt() == csdefine.ENTITY_FLAG_EXT_TRAP_BARRACKS:
				entityMailBox.setBarracksBelongType( csdefine.TRAP_BARRACKS_BELONG_ATTACK )
				self.barrackInfo[csdefine.TRAP_BARRACKS_BELONG_ATTACK].update( { scriptID : KBEMath.KBEngine2UnrealPosition( entityMailBox.position) } )
			else:
				entityMailBox.setBelongSide( csdefine.BELONG_SIDE_ATTACK )
		if entityMailBox.getEntityFlag() != csdefine.ENTITY_FLAG_ROLE and entityMailBox.scriptID in self.getScript().getBelongProtectScriptIDs():
			if entityMailBox.getEntityFlagExt() == csdefine.ENTITY_FLAG_EXT_TRAP_BARRACKS:
				entityMailBox.setBarracksBelongType( csdefine.TRAP_BARRACKS_BELONG_PROTECT )
				self.barrackInfo[csdefine.TRAP_BARRACKS_BELONG_PROTECT].update( { scriptID : KBEMath.KBEngine2UnrealPosition( entityMailBox.position )} )
			else:
				entityMailBox.setBelongSide( csdefine.BELONG_SIDE_PROTECT )
		
		if entityMailBox.getEntityFlagExt() == csdefine.ENTITY_FLAG_EXT_MONSTER_EXT_BATTERY:
			self.batteryInfo[entityMailBox.id] = [scriptID, 1, KBEMath.KBEngine2UnrealPosition( entityMailBox.position ) ]
			
	def delEntityMailBoxRecord( self, scriptID, entityMailBox ):
		"""
		删除entityMailBox 记录
		"""
		SpaceCopy.delEntityMailBoxRecord( self, scriptID, entityMailBox )
		
		if entityMailBox.getEntityFlagExt() == csdefine.ENTITY_FLAG_EXT_MONSTER_EXT_BATTERY:
			self.batteryInfo[entityMailBox.id][1] = 0
			for role in self._spaceRoles:
				if role.isBelongSide( csdefine.BELONG_SIDE_PROTECT ):
					role.client.onDestroyGTBattery( entityMailBox.id )
		
	def delayTransferDataToClient( self, roleCell ):
		"""延迟传送时间，因为怪物还没创建好"""
		self.addTimerCallBack(2, "transferDataToClient", (roleCell,))
		
	def transferDataToClient( self, roleCell ):
		"""
		传输数据到客户端
		"""
		if not roleCell or not roleCell.client:return
		barrackDict = {}
		barrackDict["dictDatas"] = []
		for side, datas in self.barrackInfo.items():
			temp = {}
			temp["belongSide"] = side
			temp["datas"] = []
			for key, value in datas.items():
				_dict = {}
				_dict["key"] = key
				_dict["value"] = value
				temp["datas"].append( _dict )
			barrackDict["dictDatas"].append( temp )
		if roleCell.isBelongSide( csdefine.BELONG_SIDE_ATTACK ):
			roleCell.client.InitGTAttackDatas( barrackDict )
		else:
			batteryDict = {}
			batteryDict["dictDatas"] = []
			for id, datas in self.batteryInfo.items():
				temp = {}
				temp["entityID"] = id
				temp["scriptID"] = datas[0]
				temp["state"] = datas[1]
				temp["pos"] = datas[2]
				batteryDict["dictDatas"].append( temp )
			spaceObj = self.getScript()
			roleCell.client.InitGTProtectDatas( barrackDict, batteryDict, spaceObj.teleportPosList, spaceObj.teleportCD )

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
	
	def onRequestSpaceNPCInfo( self, spaceData ):
		"""
		<define method>
		请求保存的数据回调
		"""
		transformScriptIDs = self.getScript().transformScriptIDs
		for data in spaceData:
			self.createEntityByScriptID( transformScriptIDs.get(data["scriptID"]), data["position"], data["direction"], data["createArgs"])
			
			
	def changeRviverPosition( self, entityID, belongType, position, oldBelongType ):
		"""
		增加复活信息(兵营被占领)
		"""
		if belongType == csdefine.TRAP_BARRACKS_BELONG_ATTACK:
			self.revivePosInfos.append(position)
		
		battackEntity = KBEngine.entities.get( entityID )
		if battackEntity and oldBelongType in self.barrackInfo and battackEntity.scriptID in self.barrackInfo[oldBelongType]:
			pos = self.barrackInfo[oldBelongType].pop( battackEntity.scriptID )
			self.barrackInfo[belongType] = { battackEntity.scriptID : pos } 
			for roleCell in self._spaceRoles:
				roleCell.client.occupyGTBarrack( belongType, battackEntity.scriptID )
			
			
	def getRevivePosition( self, role ):
		"""
		获取副本动态复活点
		"""
		playerBelongSide = role.getBelongSide()
		position = Math.Vector3(0,0,0)
		direction =  Math.Vector3(0,0,0)
		minDist = 0
		for entityMBs in self.getAllEntityMailBoxRecord().values():
			for entityMB in entityMBs:
				if entityMB.isEntityFlagExt( csdefine.ENTITY_FLAG_EXT_TRAP_BARRACKS ):
					if entityMB.getBarracksBelongType() == playerBelongSide:
						if minDist == 0:
							position = entityMB.position
							direction = entityMB.direction
							minDist = entityMB.position.distTo( role.position )
						else:
							dist = entityMB.position.distTo( role.position )
							if dist < minDist:
								minDist = dist
								position = entityMB.position
								direction = entityMB.direction
		position += (random.randint(-3,3), random.randint(-3,3), 0)
		return position, direction
		
	def requestAttckPos( self, roleCell ):
		"""守方获取攻方在战斗状态下的位置"""
		pos = None
		for player in self._spaceRoles:
			if player.isBelongSide( csdefine.BELONG_SIDE_ATTACK ) and player.isState( csdefine.ENTITY_STATE_FIGHT ):
				pos = KBEMath.KBEngine2UnrealPosition( player.position )
		if pos:
			roleCell.client.onRequestAttackPos( pos )
		else:
			roleCell.client.onRequestAttackPosNone()
			
	def requestTeleportPos( self, roleCell, pos ):
		"""守方请求 传送"""
		spaceObj = self.getScript()
		if self.teleportTime - time.time() > spaceObj.teleportCD:
			KBEDebug.ERROR_MSG("teleport pos cd now!!")
			return
		pos,dir = spaceObj.getTeleportInfo( pos )
		if pos and dir:
			self.teleportTime = time.time()
			roleCell.gotoSpace( self.scriptID, pos, dir )