# -*- coding: utf-8 -*-


from ObjectScript.Space.SpaceCopy import SpaceCopy
import csdefine
from ConfigObject import PatrolRouteLoader
import Math
import KBEngine
import csstatus
import Define
import csconst
import Functions
import Const
import time
import ItemFactory
import KBEMath
import random
import ItemTypeEnum
from ConfigObject.MailContentDataLoader import g_mailContentDataLoader
import KBEDebug
import ConfigObject.Reward.RewardBase.RewardMgr as RewardMgr

class SpaceCopyLBCBase( SpaceCopy ):
	"""
	英雄联盟
	"""
	def __init__( self ):
		SpaceCopy.__init__( self )
		self.xianBuildingScriptIDList = []
		self.moBuildingScriptIDList = []
		self.specialXianRouteList = []
		self.specialMoRouteList = []
		self.xianReviveSkillID = 0
		self.moReviveSkillID = 0
		self.xianBaseBuilding = ""
		self.moBaseBuilding	= ""
		self.delayCloseSpaceTime = 0
		self.initJade = 0 #初始化魂玉值
		self.jadeGetTime = 0 #每隔几秒魂玉获得
		self.jadeGetValue = 0 #每隔几秒获得魂玉值
		self.specialXianDirList = [] # 仙道特殊小兵路线朝向
		self.specialMoDirList = [] #魔道特殊小兵路线朝向
		self.showScriptID = [] # 【仙道，魔道】
		self.jadeScriptID = "" # 阵营动态
		self.attrScriptID = "" # 阵营动态
		self.showTime = 0.0			# 显示敌对位置的时间
		self.jadeScriptIDRewardJade = 0 #xx精英在场时所有友方玩家每秒额外获得1个魂玉
		self.jadeScriptIDRewardRadius = 0.0 #xx精英半径10米内的友方玩家
		self.jadeScriptIDRewardJadeMultiple = 0.0 #通过击杀获得的魂玉数量为1.5倍
		self.attrScriptIDRewardBuff = 0	#xx精英在战场时，战场内的所有友方单位，攻击力、防御力增加xx%
		self.killRewardExpUpper = 0 # 击杀奖励经验上限
		self.endWinRewardExp = 0 # 结算胜利方奖励
		self.endFailRewardExp = 0 # 结算失败方奖励
		self.rewardExploitID = "" 	# 胜利奖励军功ID

	def initData( self, configData ):
		"""
		virtual method
		"""
		SpaceCopy.initData( self, configData )

		xianBuildingScriptIDStr = configData["SpaceData"].get("xianBuildingData","")
		self.xianBuildingScriptIDList = xianBuildingScriptIDStr.split("|")
		moBuildingScriptIDStr = configData["SpaceData"].get( "moBuildingData","" )
		self.moBuildingScriptIDList = moBuildingScriptIDStr.split("|")
		self.specialXianRouteList = [int(i) for i in configData["SpaceData"].get("specialXianRouteData","").split("|")]
		self.specialMoRouteList = [int(i) for i in configData["SpaceData"].get("specialMoRouteData","").split("|")]
		self.xianReviveSkillID = configData["SpaceData"].get("xianReviveSkillID",0)
		self.moReviveSkillID = configData["SpaceData"].get("moReviveSkillID",0)
		self.xianBaseBuilding = configData["SpaceData"].get("xianBaseBuilding","")
		self.moBaseBuilding = configData["SpaceData"].get("moBaseBuilding","")
		self.spaceUseLevel = configData["SpaceData"].get("spaceUseLevel",0)
		self.delayCloseSpaceTime = configData["SpaceData"].get("delayCloseSpaceTime",0)
		self.initJade = configData["SpaceData"].get("initJade",0)
		self.jadeGetTime = configData["SpaceData"].get("jadeGetTime",0)
		self.jadeGetValue = configData["SpaceData"].get("jadeGetValue",0)
		specialXianDirList = configData["SpaceData"].get( "specialXianDirData","" ).split("|")
		for specialXianDir in specialXianDirList:
			xianDir = Functions.vector3TypeConvert(specialXianDir)
			if not xianDir is None:						# (0,0,0) 也要考虑
				self.specialXianDirList.append(KBEMath.Unreal2KBEngineDirection( xianDir ))

		specialMoDirList = configData["SpaceData"].get( "specialMoDirData","" ).split("|")
		for specialMoDir in specialMoDirList:
			moDir = Functions.vector3TypeConvert(specialMoDir)
			if not moDir is None:
				self.specialMoDirList.append(KBEMath.Unreal2KBEngineDirection( moDir ))

		self.showScriptID = configData["SpaceData"].get("showScriptID","").split("|")
		self.jadeScriptID = configData["SpaceData"].get("jadeScriptID","")
		self.attrScriptID = configData["SpaceData"].get("attrScriptID","")
		self.showTime = configData["SpaceData"].get("showTime",0.0)
		self.jadeScriptIDRewardJade = configData["SpaceData"].get("jadeScriptIDRewardJade",0)
		self.jadeScriptIDRewardRadius = configData["SpaceData"].get("jadeScriptIDRewardRadius",0.0)
		self.jadeScriptIDRewardJadeMultiple = configData["SpaceData"].get("jadeScriptIDRewardJadeMultiple",0.0)
		self.attrScriptIDRewardBuff = configData["SpaceData"].get("attrScriptIDRewardBuff",0)
		self.killRewardExpUpper = configData["SpaceData"].get("killRewardExpUpper",0)
		self.endWinRewardExp = configData["SpaceData"].get("endWinRewardExp",0)
		self.endFailRewardExp = configData["SpaceData"].get("endFailRewardExp",0)
		self.rewardExploitID = configData["SpaceData"].get( "rewardExploitID","" )

	def setReviveType( self ):
		"""
		设置复活类型  CST-2208
		"""
		pass

	def initEntity( self, selfEntity ):
		"""
		virtual method
		初始化space entity要做的事情
		"""
		SpaceCopy.initEntity( self, selfEntity )
		selfEntity.spaceLevel = self.spaceUseLevel

	def startSpaceLife( self, selfEntity ):
		"""
		开始计时
		"""
		selfEntity.lifeTime = self.spaceLife		# 副本时长
		selfEntity.lifeStartTime = time.time()		# 副本计时开始时间
		selfEntity.spaceLifeTimer = selfEntity.addTimerCallBackForScript(self.spaceLife, "onSpaceLifeEnd",())
		selfEntity.jadeGetTimer = selfEntity.addTimerRepeatForScript( self.jadeGetTime,"timerAddJade",() )
		for e in selfEntity._spaceRoles:
			if e.getClient():
				e.client.CLIENT_ShowYXLMSpaceLife( str(self.spaceLife * csconst.TIME_ENLARGE_MULTIPLE + Functions.getTime()) )

	def stopSpaceLife( self, selfEntity ):
		"""
		停止计时
		"""
		pass

	def changeSpaceLife( self, selfEntity, dynamicTime ):
		"""
		改变计时
		"""
		pass

	def showSpaceLifeTime( self, selfEntity, playerRole ):
		"""
		玩家显示副本剩余时间
		"""
		if selfEntity.lifeTime <= 0:
			return

		remainTime = selfEntity.lifeTime - int( time.time() - selfEntity.lifeStartTime ) + selfEntity.dynamicTime
		if playerRole.getClient():
			playerRole.client.CLIENT_ShowYXLMSpaceLife( str(remainTime * csconst.TIME_ENLARGE_MULTIPLE + Functions.getTime()) )

	def timerAddJade( self, selfEntity ):
		"""
		"""
		for role in selfEntity._spaceRoles:
			role.addJade(self.jadeGetValue)

	def onSpaceLifeEnd( self, selfEntity ):
		"""
		副本时间到达 如果进攻方未获胜则防守方获胜
		"""
		if selfEntity.winCamp:
			return

		self.setWinCamp(selfEntity, csdefine.BELONG_SIDE_PROTECT, csstatus.SPACECOPY_CAMP_YXLM_DESTROY_BUILDING_LESS_WIN, csstatus.SPACECOPY_CAMP_YXLM_TIME_KILL_FAILURE)


	def onEnter( self, selfEntity, playerRole, packArgs ):
		SpaceCopy.onEnter( self, selfEntity, playerRole, packArgs )
		playerRole.jade = self.initJade
		belongSide = packArgs.get("belongSide", csdefine.BELONG_SIDE_ATTACK)
		playerRole.setBelongSide(belongSide)
		selfEntity.addPlayerBelongSide(playerRole.playerDBID, belongSide)
		selfEntity.addYXLMMemberData( playerRole )

	def getReviveSkillIDByCamp( self, role ):
		belongSide = role.getBelongSide()
		if belongSide == csdefine.BELONG_SIDE_ATTACK:
			return self.xianReviveSkillID
		elif belongSide == csdefine.BELONG_SIDE_PROTECT:
			return self.moReviveSkillID
		return 0

	def onMonsterDie( self, selfEntity, monsterID, monsterScriptID ):
		"""
		怪物死亡
		"""
		SpaceCopy.onMonsterDie( self, selfEntity, monsterID, monsterScriptID )
		if monsterScriptID in self.xianBuildingScriptIDList:
			entityTower = KBEngine.entities.get( monsterID,None )
			if not entityTower:
				return
			if entityTower.wayType not in selfEntity.xianDestroyBuildingData:
				selfEntity.xianDestroyBuildingData[entityTower.wayType] = []
			selfEntity.xianDestroyBuildingData[entityTower.wayType].append( monsterScriptID )
		if monsterScriptID in self.moBuildingScriptIDList:
			entityTower = KBEngine.entities.get( monsterID,None )
			if not entityTower:
				return
			if entityTower.wayType not in selfEntity.moDestroyBuildingData:
				selfEntity.moDestroyBuildingData[entityTower.wayType] = []
			selfEntity.moDestroyBuildingData[entityTower.wayType].append( monsterScriptID )

		belongSide = -1
		if monsterScriptID == self.xianBaseBuilding:
			belongSide = csdefine.BELONG_SIDE_PROTECT
		if monsterScriptID == self.moBaseBuilding:
			belongSide = csdefine.BELONG_SIDE_ATTACK
		if belongSide == -1:
			return
		self.setWinCamp( selfEntity, belongSide, csstatus.SPACECOPY_CAMP_YXLM_ENEMY_BUILIDING_DESTROY ,csstatus.SPACECOPY_CAMP_YXLM_BASE_BUILIDING_DESTROY )

	def onPlayerGetItem( self, selfEntity, playerRole, itemInstID, amount ):
		"""
		玩家获得物品
		"""
		SpaceCopy.onPlayerGetItem( self, selfEntity, playerRole, itemInstID, amount )
		itemInstList = playerRole.getItemInstsByID( itemInstID )
		if len(itemInstList) and itemInstList[0].getType() == ItemTypeEnum.ITEM_TYPE_COPY_YXWZ1 and selfEntity.winCamp <0:
			selfEntity.onMemberAddItem( playerRole, itemInstID )

	def onPlayerRemoveItem( self, selfEntity, playerRole, itemInstID, amount ):
		"""
		玩家移除物品
		"""
		SpaceCopy.onPlayerRemoveItem( self, selfEntity, playerRole, itemInstID, amount )
		itemInst = ItemFactory.ItemFactoryInst.createDynamicItem(itemInstID)
		if itemInst and itemInst.getType() == ItemTypeEnum.ITEM_TYPE_COPY_YXWZ1 and selfEntity.winCamp <0:
			selfEntity.onMemberRemoveItem( playerRole, itemInstID )

	def getPackDomainData( self, playerEntity, args ):
		"""
		"""
		packDict = SpaceCopy.getPackDomainData( self, playerEntity, args )
		if playerEntity.teamMailbox:
			packDict["teamID"] = playerEntity.teamMailbox.id
		packDict["playerDBID"] = playerEntity.playerDBID
		return packDict

	def getSpecialXianRouteList( self ):
		"""
		"""
		return self.specialXianRouteList

	def getSpecialMoRouteList( self ):
		"""
		"""
		return self.specialMoRouteList

	def createMonsterByShop( self, selfEntity, player, scriptID, index, param ):
		"""
		商店购买小兵
		"""
		belongSide = player.getBelongSide()
		route = -1
		dir = (0,0,0)
		if belongSide == csdefine.BELONG_SIDE_ATTACK:
			route = self.specialXianRouteList[index]
			dir = self.specialXianDirList[index]
		elif belongSide == csdefine.BELONG_SIDE_PROTECT:
			route = self.specialMoRouteList[index]
			dir = self.specialMoDirList[index]
		routeInfo = PatrolRouteLoader.g_patrolRouteLoader.getPatrolRoute( selfEntity.scriptID, route )
		if len(routeInfo):
			param.update( { "spawnPos": Math.Vector3(routeInfo[1]["position"]), "patrolList":route,"spawnDir":dir, "belongSide":belongSide,"way":(index + 1) } )
			selfEntity.createEntityByScriptID( scriptID, Math.Vector3(routeInfo[1]["position"]), dir, param )

	def onTeamMemberLeave( self, selfEntity, teamID, playerDBID ):
		"""
		玩家离队
		"""
		for roleCell in selfEntity._spaceRoles:
			if roleCell.playerDBID == playerDBID:
				roleCell.gotoExitSpacePos()

	def onTeamDisband( self, selfEntity, teamID, memDBIDs ):
		"""
		队伍解散
		"""
		for roleCell in selfEntity._spaceRoles:
			if roleCell.playerDBID in memDBIDs:
				roleCell.gotoExitSpacePos()

	def onMonsterHPChanged( self, selfEntity, monsterEntity ):
		"""
		怪物血量改变
		"""
		SpaceCopy.onMonsterHPChanged( self, selfEntity, monsterEntity )
		if (monsterEntity.scriptID == self.xianBaseBuilding or monsterEntity.scriptID == self.moBaseBuilding) and monsterEntity.scriptID not in selfEntity.spaceEventTimers:
			timerID = selfEntity.addTimerCallBackForScript( 15.0,"removeTimer",( monsterEntity.scriptID, ) )
			selfEntity.spaceEventTimers[monsterEntity.scriptID] = timerID
			memberList = selfEntity.memberDatas.getMembersByCamp( monsterEntity.getBelongSide() )
			monsterPersent = float( monsterEntity.HP )/monsterEntity.HP_Max
			statusID = 0
			if monsterPersent < 1.0:
				statusID = csstatus.SPACECOPY_CAMP_YXLM_BASE_BUILIDING_HP_CHANGE
			if monsterPersent < 0.5:
				statusID = csstatus.SPACECOPY_CAMP_YXLM_BASE_BUILIDING_HP_FIVITY
			if monsterPersent < 0.3:
				statusID = csstatus.SPACECOPY_CAMP_YXLM_BASE_BUILIDING_HP_THRTY
			if not statusID:
				return
			for member in memberList:
				member.roleMB.statusMessage( statusID,"" )

	def removeTimer( self, selfEntity, scriptID ):
		"""
		"""
		if scriptID in selfEntity.spaceEventTimers:
			timerID = selfEntity.spaceEventTimers[scriptID]
			selfEntity.popTimer(timerID)
			selfEntity.spaceEventTimers.pop( scriptID )

	def setWinCamp( self, selfEntity, belongSide, winStatusID, loseStatusID ):
		"""
		设置赢的队伍
		"""
		if selfEntity.winCamp >= 0:
			return
		if selfEntity.jadeGetTimer:
			selfEntity.popTimer( selfEntity.jadeGetTimer )
			selfEntity.jadeGetTimer = 0
		selfEntity.winCamp = belongSide
		selfEntity.addEndRewardExp()
		
		lbcItem = selfEntity.createArgs.get("lbcItem",None)
		#如果进攻方获胜，更新练兵场信息
		player = self.getDeclarePlayer(selfEntity, lbcItem.declarerDBID)
		if belongSide == csdefine.BELONG_SIDE_ATTACK:
			KBEngine.globalData["LbcMgr"].attackerWin(lbcItem.line, lbcItem.index, player, player.playerDBID, player.getName(), player.getProfession())
		else:
			KBEngine.globalData["LbcMgr"].attackerLose(lbcItem.line, lbcItem.index, player)
			
		selfEntity.addTimerCallBackForScript(3.0,"showLBCBattlefieldWin",(belongSide,winStatusID,loseStatusID, lbcItem.declarerName, lbcItem.occupierName, lbcItem.lbcName))
		selfEntity.addTimerCallBack(self.delayCloseSpaceTime, "closeSpace", ())
		self.showTimeCountDown(selfEntity,csstatus.SPACE_CLOSE_NOTIFY, self.delayCloseSpaceTime )
		self.onConditionChange(selfEntity, "", selfEntity.id, "Win", "")
		

	def getDeclarePlayer(self, selfEntity,declarePlayerDBID):
		"""
		"""
		for member in selfEntity.memberDatas.getAllMembers():
			if member.roleMB.playerDBID == declarePlayerDBID:
				return member.roleMB
		return None

	def showLBCBattlefieldWin( self, selfEntity, belongSide, winStatusID, loseStatusID, declarePlayerName, occupyPlayerName, trainGroundName):
		"""
		"""
		successReward = 0
		rewardDatas = RewardMgr.g_rewardMgr.getReward(self.rewardExploitID,{})
		for rewardData in rewardDatas:
			if rewardData.get("type","") == csdefine.REWARD_TYPE_EXPLOIT:
				successReward += rewardData.get("amount",0)
		selfEntity.memberDatas.setWinCamp(belongSide, winStatusID, loseStatusID, successReward, 0, declarePlayerName, occupyPlayerName, trainGroundName)

	def onLeave( self, selfEntity, playerRole, packArgs ):
		"""
		virtual method
		玩家离开副本 如果玩家中途自己退出游戏，则清除改玩家的副本数据，如果所有玩家都离开，则对方获胜，如果是掉线，记录一下jade
		"""
		if packArgs[ "leaveReason" ] == Define.LEAVE_SPACE_REASON_TELEPORT:
			selfEntity.removeYXLMMemberData(playerRole)
			belongSide = playerRole.getBelongSide()
			memberList = selfEntity.memberDatas.getMembersByCamp( belongSide )
			if len(memberList):
				return
			#进攻方的人跑完了 防守方获胜，反之亦然
			winCamp = csdefine.BELONG_SIDE_PROTECT if belongSide == csdefine.BELONG_SIDE_ATTACK else csdefine.BELONG_SIDE_ATTACK
			self.setWinCamp( selfEntity, winCamp,csstatus.SPACECOPY_CAMP_YXLM_ENEMY_LEVEL_SPACE,0 )

		elif packArgs[ "leaveReason" ] == Define.LEAVE_SPACE_REASON_LOGOUT:
			member = selfEntity.memberDatas.getMemberByPlayerDBID( playerRole.playerDBID )
			member.roleJade = playerRole.jade

		SpaceCopy.onLeave( self, selfEntity, playerRole, packArgs )
		
	def onLogin( self, selfEntity, playerRole ):
		"""
		"""
		SpaceCopy.onLogin( self, selfEntity, playerRole )
		belongSide = selfEntity.getPlayerBelongSide(playerRole.playerDBID)
		playerRole.setBelongSide(belongSide)
		selfEntity.addYXLMMemberData( playerRole )

	def buyRandomScriptID( self, selfEntity,role,scriptID ):
		"""
		随机事件 购买小兵
		"""
		if scriptID not in selfEntity.randomEventScriptIDDict:
			return
		if role.jade < selfEntity.randomEventScriptIDDict[scriptID]:
			return
		belongSide = role.getBelongSide()

		if belongSide == csdefine.BELONG_SIDE_ATTACK:
			route = random.choice(self.specialXianRouteList)
			index = self.specialXianRouteList.index(route)
			dir = self.specialXianDirList[index]
		else:
			route = random.choice(self.specialMoRouteList)
			index = self.specialMoRouteList.index(route)
			dir = self.specialMoDirList[index]
		routeInfo = PatrolRouteLoader.g_patrolRouteLoader.getPatrolRoute( selfEntity.scriptID, route )
		if len(routeInfo):
			param = { "spawnPos": Math.Vector3(routeInfo[1]["position"]), "patrolList":route,"spawnDir":dir, "belongSide":belongSide,"way":(index + 1) }
			entity = selfEntity.createEntityByScriptID( scriptID, Math.Vector3(routeInfo[1]["position"]), dir, param )
			if entity:
				role.addJade( -selfEntity.randomEventScriptIDDict[scriptID] )

	