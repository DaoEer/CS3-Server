# -*- coding: utf-8 -*-


import KBEDebug
import KBEngine
import Math
import KBEMath
import Functions
import csdefine
import csstatus

from ObjectScript.Space.SpaceCopy import SpaceCopy
from ImpInterface.SpaceStageExtInterface import SpaceStageExtInterface

class SpaceCopyTongPlunder( SpaceStageExtInterface, SpaceCopy ):
	"""
	CST-11602 帮会掠夺
	"""
	def __init__( self ):
		SpaceCopy.__init__( self )
		SpaceStageExtInterface.__init__( self )

		self.playerReviveTimerIDList = {}

		self.attackTongDBID = -1
		self.attackTongName = ""
		self.attackTongLevel = 0

		self.protectTongDBID = -1
		self.protectTongLevel = 0
		self.protectTongName = ""

		self.reviveRadius = 0.0
		self.enterPos = {}
		self.defaultReviveInfo = {}
		self.belongAttackScriptIDs = []
		self.belongProtectScriptIDs = []
		self.plunderBoxScriptIDList = []
		self.reviveTime = 0.0
		self.autoReviveTime = 0.0
		self.maxReviveNum = 0
		self.delayCloseTime = 0
		
		self._leaveTongSpaceScriptID = ""
		self._leaveTongSpacePos = Math.Vector3(0.0, 0.0, 0.0)
		self._leaveTongSpaceDir = Math.Vector3(0.0, 0.0, 0.0)
	
	def initData( self, configData ):
		"""
		virtual method
		"""
		SpaceCopy.initData( self, configData )
		self.reviveRadius = configData["SpaceData"].get( "reviveRadius", 0.0 )
		attackEnterPosStr = configData["SpaceData"].get( "attackEnterPos", "")
		protectEnterPosStr = configData["SpaceData"].get( "attackEnterPos", "")
		if attackEnterPosStr:
			self.enterPos[csdefine.BELONG_SIDE_ATTACK] = []
			posStr, dirStr = attackEnterPosStr.split("|")
			self.enterPos[csdefine.BELONG_SIDE_ATTACK].append(Math.Vector3(KBEMath.Unreal2KBEnginePosition(Functions.vector3TypeConvert(posStr))))
			self.enterPos[csdefine.BELONG_SIDE_ATTACK].append(Math.Vector3(KBEMath.Unreal2KBEngineDirection(Functions.vector3TypeConvert(dirStr))))
		if protectEnterPosStr:
			self.enterPos[csdefine.BELONG_SIDE_PROTECT] = []
			posStr, dirStr = protectEnterPosStr.split("|")
			self.enterPos[csdefine.BELONG_SIDE_PROTECT].append(Math.Vector3(KBEMath.Unreal2KBEnginePosition(Functions.vector3TypeConvert(posStr))))
			self.enterPos[csdefine.BELONG_SIDE_PROTECT].append(Math.Vector3(KBEMath.Unreal2KBEngineDirection(Functions.vector3TypeConvert(dirStr))))
		
		self.belongAttackScriptIDs = configData["SpaceData"].get( "belongAttackScriptIDs","" ).split("|")
		self.belongProtectScriptIDs = configData["SpaceData"].get( "belongProtectScriptIDs","" ).split("|")

		self.reviveTime = float(configData["SpaceData"].get("reviveTime", 0))
		self.autoReviveTime = float(configData["SpaceData"].get("autoReviveTime", 0))
		self.maxReviveNum = int(configData["SpaceData"].get("maxReviveNum", 0))
		self.delayCloseTime = float(configData["SpaceData"].get("delayCloseTime", 0))

		plunderBoxScriptID = configData["SpaceData"].get("plunderBoxScriptIDs", "")
		if plunderBoxScriptID:
			self.plunderBoxScriptIDList = plunderBoxScriptID.split("|")

		if "leaveTongSpaceData" in configData["SpaceData"]:
			self._leaveTongSpaceScriptID = configData["SpaceData"]["leaveTongSpaceData"].get("ScriptID", "")
			posStr = configData["SpaceData"]["leaveTongSpaceData"].get("Position", "")
			pos = Functions.vector3TypeConvert(posStr)
			if pos:
				self._leaveTongSpacePos = KBEMath.Unreal2KBEnginePosition(pos)
			dirStr = configData["SpaceData"]["leaveTongSpaceData"].get("Direction", "")
			dir = Functions.vector3TypeConvert(dirStr)
			if dir:
				self._leaveTongSpaceDir = KBEMath.Unreal2KBEngineDirection(dir)

		attackStageFile = configData["SpaceData"].get("attackStageFile", "")
		protectStageFile = configData["SpaceData"].get("protectStageFile", "")
		
		if attackStageFile and protectStageFile:
			self.initAckAndPctSpaceStages(protectStageFile, attackStageFile)
			
		attackRevivePosStr = configData["SpaceData"].get( "attackRevivePos", "")
		protectRevivePosStr = configData["SpaceData"].get( "protectRevivePos", "")
		if attackRevivePosStr:
			self.defaultReviveInfo[csdefine.BELONG_SIDE_ATTACK] = []
			posStr, dirStr = attackRevivePosStr.split("|")
			self.defaultReviveInfo[csdefine.BELONG_SIDE_ATTACK].append(Math.Vector3(KBEMath.Unreal2KBEnginePosition(Functions.vector3TypeConvert(posStr))))
			self.defaultReviveInfo[csdefine.BELONG_SIDE_ATTACK].append(Math.Vector3(KBEMath.Unreal2KBEngineDirection(Functions.vector3TypeConvert(dirStr))))
		if protectRevivePosStr:
			self.defaultReviveInfo[csdefine.BELONG_SIDE_PROTECT] = []
			posStr, dirStr = protectRevivePosStr.split("|")
			self.defaultReviveInfo[csdefine.BELONG_SIDE_PROTECT].append(Math.Vector3(KBEMath.Unreal2KBEnginePosition(Functions.vector3TypeConvert(posStr))))
			self.defaultReviveInfo[csdefine.BELONG_SIDE_PROTECT].append(Math.Vector3(KBEMath.Unreal2KBEngineDirection(Functions.vector3TypeConvert(dirStr))))
		
	def setBothSidesInfo(self, tongInfo):
		self.attackTongDBID = tongInfo["attackTongInfo"]["dbid"]
		self.attackTongLevel = tongInfo["attackTongInfo"]["level"]
		self.attackTongName = tongInfo["attackTongInfo"]["name"]

		self.protectTongDBID = tongInfo["protectTongInfo"]["dbid"]
		self.protectTongLevel = tongInfo["protectTongInfo"]["level"]
		self.protectTongName = tongInfo["protectTongInfo"]["name"]

	def getBothSidesDBID(self):
		return (self.attackTongDBID, self.protectTongDBID)

	def getBothSidesLevel(self):
		return (self.attackTongLevel, self.protectTongLevel)

	def getLeaveTongSpaceInfo(self):
		return (self._leaveTongSpaceScriptID, self._leaveTongSpacePos, self._leaveTongSpaceDir)

	def getPlunderBoxScriptID(self):
		return self.plunderBoxScriptIDList
	
	def setReviveType( self ):
		"""
		设置复活类型  CST-2208
		"""
		pass
		
	def getBelongAttackScriptIDs(self):
		"""
		进攻方兵营scriptID
		"""
		return self.belongAttackScriptIDs

	def getBelongProtectScriptIDs(self):
		"""
		防守方兵营scriptID
		"""
		return self.belongProtectScriptIDs
		
	def getReviveRadius(self):
		"""
		随机复活位置半径
		"""
		return self.reviveRadius
	
	def getDefaultRevivePos(self, belongType, player):
		return [self.defaultReviveInfo.get(belongType, [player.position])[0]]

	def getReviveTime(self):
		"""
		获取复活时间
		"""
		return self.reviveTime

	def getMaxReviveNum(self):
		"""
		获取最大复活次数
		"""
		return self.maxReviveNum

	def getDelayCloseTime(self):
		"""
		胜负结果出来后多久关闭副本
		"""
		return self.delayCloseTime
		
	def onPlayerEnterSpace(self, selfEntity, playerRole, packArgs):
		"""
		"""
		if not playerRole:
			return

		belongSide = 0
		if playerRole.tongDBID == self.attackTongDBID:
			belongSide = csdefine.BELONG_SIDE_ATTACK
		elif playerRole.tongDBID == self.protectTongDBID:
			belongSide = csdefine.BELONG_SIDE_PROTECT
		else:
			KBEDebug.ERROR_MSG("this copy space is attack(%s) and protect(%s), but player is %s" % 
				(self.attackTongDBID, self.protectTongDBID, playerRole.tongDBID))
			return

		playerRole.setBelongSide(belongSide)
		playerRole.remainYXLMReviveTime = self.getReviveTime()
		playerRole.remainReviveNum = self.getMaxReviveNum() - selfEntity.recordRoleReviveData.get(playerRole.playerDBID, 0)
		selfEntity.recordRoleBelongSide(playerRole.getBelongSide(), playerRole.playerDBID)

		selfEntity.addPlunderMember(playerRole.playerDBID, playerRole, playerRole.getName(), belongSide)

		selfEntity.delayTransferDataToClient(playerRole)

	def onLogin(self, selfEntity, playerRole):
		self.onPlayerEnterSpace(selfEntity, playerRole, {})
		SpaceCopy.onLogin(self, selfEntity, playerRole)


	def onEnter(self, selfEntity, playerRole, packArgs):
		self.onPlayerEnterSpace(selfEntity, playerRole, packArgs)
		SpaceCopy.onEnter( self, selfEntity, playerRole, packArgs )

	def onLeave(self, selfEntity, playerRole, packArgs):
		"""
		virtual method
		玩家离开副本
		"""
		SpaceCopy.onLeave(self, selfEntity, playerRole, packArgs)
		#离开副本销毁部队
		playerRole.setCallArmyIndex(-1)
		#玩家主动离开副本，不能再次进入，即不能通过NPC对话进入。掉线重连不需要通过NPC对话
		if not selfEntity.activeIsEnd():
			KBEngine.globalData["TongPlunderManager"].onPlayerLeaveSpace(playerRole.playerDBID)
		selfEntity.onRoleLeaveSpace(playerRole)

	def onTeleportCompleted(self, selfEntity, playerRole):
		"""
		"""
		SpaceCopy.onTeleportCompleted(self, selfEntity, playerRole)
		
		#召唤部队
		if len(playerRole.getRoleArmyDatas()) > 0:
			armyIndex = selfEntity.getRoleRecordCallArmy( playerRole.playerDBID )
			if armyIndex == -1:		#等于-1说明玩家之前没有进过副本或没有部队
				armyIndex = playerRole.getDefaultArmyIndex()
			if armyIndex != -1:
				playerRole.callIDArmyToWar( armyIndex )

	def onPlayerCallArmy( self, selfEntity, playerID, playerDBID, armyIndex ):
		"""
		玩家点击了出战
		"""
		selfEntity.updateRoleRecordCallArmy( playerDBID, armyIndex )

	def getPackDomainData(self, playerEntity, args):
		packDict = SpaceCopy.getPackDomainData(self, playerEntity, args)
		packDict["playerDBID"] = playerEntity.playerDBID
		packDict["attackTongDBID"] = self.attackTongDBID
		packDict["protectTongDBID"] = self.protectTongDBID
		return packDict
		
	def onPlayerRevive(self, selfEntity, playerRole):
		"""
		玩家复活
		"""
		if playerRole.playerDBID in self.playerReviveTimerIDList and self.playerReviveTimerIDList[playerRole.playerDBID]:
			playerRole.popTimer(self.playerReviveTimerIDList[playerRole.playerDBID])
			self.playerReviveTimerIDList[playerRole.playerDBID] = 0

	def spaceStage_onSpaceInit( self, selfEntity ):
		"""
		"""
		selfEntity.spaceStage = None	# 初始值需要为None，而因为是define属性，此值会是一个SpaceStageDataType对象，不为None，因此手动赋一下值。
		selfEntity.attackSpaceStages = None
		if len( self.spaceStages ) and self.beginOnInit:
			self.setSpaceStage( selfEntity, self.spaceStages[0].stageIndex )

	def spaceStage_onPlayerLeave( self, selfEntity, roleCell ):
		"""
		玩家出副本
		"""
		if roleCell.getClient():
			roleCell.client.CLIENT_hideSpaceStageWin()		#没有stage也要隐藏一下，因为stage完成后界面还在
		if not self.hasSpaceStage( selfEntity ):
			return
		if roleCell.getClient():
			roleCell.client.CLIENT_ClearSpaceStageTaskArea()
		changedTasks = selfEntity.spaceStage.updateGetItemTask( selfEntity )	#获取物品类目标在玩家离开副本的时候要刷一下已完成数量
		self.updateSpaceStage( selfEntity, changedTasks, roleCell.belongSide )

	def onPlayerDie( self, selfEntity, playerID, playerMB ):
		"""
		玩家死亡
		"""
		SpaceCopy.onPlayerDie(self, selfEntity, playerID, playerMB)

		playerRole = KBEngine.entities.get(playerID)

		reviveNum = 0
		if playerRole.playerDBID in selfEntity.recordRoleReviveData:
			reviveNum = selfEntity.recordRoleReviveData[playerRole.playerDBID]
		remainReviveNum = self.getMaxReviveNum() - reviveNum
		if remainReviveNum == 0:
			#是由于客户端播完死亡动作后会弹出复活框会将改提示框覆关闭, 需要加四秒延迟
			playerRole.addTimerCallBack(4.0, "inquireMessage",((csstatus.TONG_PLUNDER_REVIVE_NUM_USE_UP, [self.getMaxReviveNum()], "leaveTongPlunderSpace")))
			#playerRole.inquireMessage(csstatus.TONG_PLUNDER_REVIVE_NUM_USE_UP, [self.getMaxReviveNum()], "leaveTongPlunderSpace")
			return

		if playerRole and self.autoReviveTime > 0:
			if playerRole.playerDBID in self.playerReviveTimerIDList and self.playerReviveTimerIDList[playerRole.playerDBID]:
				playerRole.popTimer(self.playerReviveTimerIDList[playerRole.playerDBID])

			self.playerReviveTimerIDList[playerRole.playerDBID] = playerRole.addTimerCallBack(self.autoReviveTime, "reviveOnTongPlunder", ())

		