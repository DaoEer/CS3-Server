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

class SpaceCopyYXLM( SpaceCopy ):
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
		self.endWinFeats = configData["SpaceData"].get("endWinFeats",0)#功勋
		self.endFailFeats = configData["SpaceData"].get("endFailFeats",0)	
		self.endWinExploit = configData["SpaceData"].get("endWinExploit",0)	#军功
		self.endFailExploit = configData["SpaceData"].get("endFailExploit",0)
		
		#邮件ID
		self.endWinMailIDs = {}
		endWinMailIDDict = configData["SpaceData"].get("endWinMailID", {})
		for k, v in endWinMailIDDict.items():
			levelList = [int(level) for level in k.split("-")]
			self.endWinMailIDs[k] = (levelList, v)
		
		self.endFailMailIDs = {}
		endFailMailIDDict = configData["SpaceData"].get("endFailMailID", {})
		for k, v in endFailMailIDDict.items():
			levelList = [int(level) for level in k.split("-")]
			self.endFailMailIDs[k] = (levelList, v)
			
		#不在线邮件ID
		self.endWinOffLineMailIDs = {}
		endWinOffLineMailIDDict = configData["SpaceData"].get("endWinOffLineMailID", {})
		for k, v in endWinOffLineMailIDDict.items():
			levelList = [int(level) for level in k.split("-")]
			self.endWinOffLineMailIDs[k] = (levelList, v)
		
		self.endFailOffLineMailIDs = {}
		endFailOffLineMailIDDict = configData["SpaceData"].get("endFailOffLineMailID", {})
		for k, v in endFailOffLineMailIDDict.items():
			levelList = [int(level) for level in k.split("-")]
			self.endFailOffLineMailIDs[k] = (levelList, v)
		
		#经验
		self.endWinRewardExp = {}
		endWinRewardExpDict = configData["SpaceData"].get("endWinRewardExp",{})
		for k, v in endWinRewardExpDict.items():
			levelList = [int(level) for level in k.split("-")]
			self.endWinRewardExp[k] = (levelList, v)
		
		self.endFailRewardExp = {}
		endFailRewardExpDict = configData["SpaceData"].get("endFailRewardExp",{})
		for k, v in endFailRewardExpDict.items():
			levelList = [int(level) for level in k.split("-")]
			self.endFailRewardExp[k] = (levelList, v)
		
	def getWinFinalRewardExp(self, level):
		"""
		"""
		for levelList, exp in list(self.endWinRewardExp.values()):
			if levelList[0] <= level and level < levelList[1]:
				return exp
		return 0
		
	def getFailFinalRewardExp(self, level):
		"""
		"""
		for levelList, exp in list(self.endFailRewardExp.values()):
			if levelList[0] <= level and level < levelList[1]:
				return exp
		return 0
		
	def getWinFinalMailID(self, level):
		"""
		"""
		for levelList, mailID in list(self.endWinMailIDs.values()):
			if levelList[0] <= level and level < levelList[1]:
				return mailID
		return ""
		
	def getFailFinalMailID(self, level):
		"""
		"""
		for levelList, mailID in list(self.endFailMailIDs.values()):
			if levelList[0] <= level and level < levelList[1]:
				return mailID
		return ""
		
	def getWinOffLineFinalMailID(self, level):
		"""
		"""
		for levelList, mailID in list(self.endWinOffLineMailIDs.values()):
			if levelList[0] <= level and level < levelList[1]:
				return mailID
		return ""
		
	def getFailOffLineFinalMailID(self, level):
		"""
		"""
		for levelList, mailID in list(self.endFailOffLineMailIDs.values()):
			if levelList[0] <= level and level < levelList[1]:
				return mailID
		return ""
		
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
		副本时间到达
		"""
		xianDestroyBuildingList = []
		for i in selfEntity.xianDestroyBuildingData.values():
			xianDestroyBuildingList.extend( i )
		moDestroyBuildingList = []
		for i in selfEntity.moDestroyBuildingData.values():
			moDestroyBuildingList.extend( i )
		if len(xianDestroyBuildingList) > len(moDestroyBuildingList):
			self.setWinCamp( selfEntity,csdefine.CAMP_DEMON,csstatus.SPACECOPY_CAMP_YXLM_DESTROY_BUILDING_LESS_WIN,csstatus.SPACECOPY_CAMP_YXLM_ENEMY_BUILIDING_DESTROY )
		elif len(xianDestroyBuildingList) < len(moDestroyBuildingList):
			self.setWinCamp(selfEntity, csdefine.CAMP_TAOSIM, csstatus.SPACECOPY_CAMP_YXLM_DESTROY_BUILDING_LESS_WIN,csstatus.SPACECOPY_CAMP_YXLM_ENEMY_BUILIDING_DESTROY )
		else:
			xianJadeValue = selfEntity.memberDatas.getMembersAllJadeValueByCamp( csdefine.CAMP_TAOSIM  )
			moJadeValue = selfEntity.memberDatas.getMembersAllJadeValueByCamp( csdefine.CAMP_DEMON  )
			if xianJadeValue >= moJadeValue:
				self.setWinCamp( selfEntity,csdefine.CAMP_TAOSIM,csstatus.SPACECOPY_CAMP_YXLM_TIME_JADE_MOVE_WIN,csstatus.SPACECOPY_CAMP_YXLM_TIME_JADE_FAILURE )
			elif xianJadeValue < moJadeValue:
				self.setWinCamp( selfEntity,csdefine.CAMP_DEMON,csstatus.SPACECOPY_CAMP_YXLM_TIME_JADE_MOVE_WIN,csstatus.SPACECOPY_CAMP_YXLM_TIME_JADE_FAILURE )

	def onEnter( self, selfEntity, playerRole, packArgs ):
		SpaceCopy.onEnter( self, selfEntity, playerRole, packArgs )
		playerRole.onEnterCampYXLM()
		playerRole.jade = self.initJade
		selfEntity.addYXLMMemberData( playerRole )

	def getReviveSkillIDByCamp( self, role ):
		camp = role.getCamp()
		if camp == csdefine.CAMP_TAOSIM:
			return self.xianReviveSkillID
		elif camp == csdefine.CAMP_DEMON:
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

		camp = None
		if monsterScriptID == self.xianBaseBuilding:
			camp = csdefine.CAMP_DEMON
		if monsterScriptID == self.moBaseBuilding:
			camp = csdefine.CAMP_TAOSIM
		if camp == None:
			return
		self.setWinCamp( selfEntity, camp, csstatus.SPACECOPY_CAMP_YXLM_ENEMY_BUILIDING_DESTROY ,csstatus.SPACECOPY_CAMP_YXLM_BASE_BUILIDING_DESTROY )

	def onPlayerGetItem( self, selfEntity, playerRole, itemInstID, amount ):
		"""
		玩家获得物品
		"""
		SpaceCopy.onPlayerGetItem( self, selfEntity, playerRole, itemInstID, amount )
		itemInstList = playerRole.getItemInstsByID( itemInstID )
		if len(itemInstList) and itemInstList[0].getType() == ItemTypeEnum.ITEM_TYPE_COPY_YXWZ1 and not selfEntity.winCamp:
			selfEntity.onMemberAddItem( playerRole, itemInstID )

	def onPlayerRemoveItem( self, selfEntity, playerRole, itemInstID, amount ):
		"""
		玩家移除物品
		"""
		SpaceCopy.onPlayerRemoveItem( self, selfEntity, playerRole, itemInstID, amount )
		itemInst = ItemFactory.ItemFactoryInst.createDynamicItem(itemInstID)
		if itemInst and itemInst.getType() == ItemTypeEnum.ITEM_TYPE_COPY_YXWZ1 and not selfEntity.winCamp:
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
		camp = player.getCamp()
		route = -1
		dir = (0,0,0)
		if camp == csdefine.CAMP_TAOSIM:
			route = self.specialXianRouteList[index]
			dir = self.specialXianDirList[index]
		elif camp == csdefine.CAMP_DEMON:
			route = self.specialMoRouteList[index]
			dir = self.specialMoDirList[index]
		routeInfo = PatrolRouteLoader.g_patrolRouteLoader.getPatrolRoute( selfEntity.scriptID, route )
		if len(routeInfo):
			param.update( { "spawnPos": Math.Vector3(routeInfo[1]["position"]), "patrolList":route,"spawnDir":dir, "camp":camp,"way":(index + 1) } )
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
			memberList = selfEntity.memberDatas.getMembersByCamp( monsterEntity.getCamp() )
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

	def setWinCamp( self, selfEntity,camp, winStatusID, loseStatusID ):
		"""
		设置赢的队伍
		"""
		KBEDebug.DEBUG_MSG("SET winCamp")
		if selfEntity.winCamp:
			return
		if selfEntity.jadeGetTimer:
			selfEntity.popTimer( selfEntity.jadeGetTimer )
			selfEntity.jadeGetTimer = 0
		selfEntity.winCamp = camp
		selfEntity.addEndReward()
		selfEntity.addFinalContributionReward()
		selfEntity.addTimerCallBackForScript( 3.0,"showYXLMBattlefieldWin",(camp,winStatusID,loseStatusID) )
		selfEntity.addTimerCallBack( self.delayCloseSpaceTime, "closeSpace", () )
		self.showTimeCountDown( selfEntity,csstatus.SPACE_CLOSE_NOTIFY, self.delayCloseSpaceTime )
		self.onConditionChange( selfEntity, "", selfEntity.id, "Win", "" )
		for member in selfEntity.memberDatas.getAllMembers():
			if member.roleMB.getCamp() == camp:
				g_mailContentDataLoader.sendActivityReward( self.scriptID,1,member.roleName )
			else:
				g_mailContentDataLoader.sendActivityReward( self.scriptID,2,member.roleName )

	def showYXLMBattlefieldWin( self, selfEntity, camp, winStatusID, loseStatusID ):
		"""
		"""
		selfEntity.memberDatas.setWinCamp(camp, winStatusID, loseStatusID, selfEntity.zyjjRewardDatas )

	def onLeave( self, selfEntity, playerRole, packArgs ):
		"""
		virtual method
		玩家离开副本
		"""
		if packArgs[ "leaveReason" ] == Define.LEAVE_SPACE_REASON_TELEPORT:
			selfEntity.removeYXLMMemberData(playerRole)
			camp = playerRole.getCamp()
			memberList = selfEntity.memberDatas.getMembersByCamp( camp )
			if len(memberList):
				return
			winCamp = None
			if camp == csdefine.CAMP_TAOSIM:
				winCamp = csdefine.CAMP_DEMON
			elif camp == csdefine.CAMP_DEMON:
				winCamp = csdefine.CAMP_TAOSIM
			if winCamp:
				self.setWinCamp( selfEntity, winCamp,csstatus.SPACECOPY_CAMP_YXLM_ENEMY_LEVEL_SPACE,0 )
		elif packArgs[ "leaveReason" ] == Define.LEAVE_SPACE_REASON_LOGOUT:
			member = selfEntity.memberDatas.getMemberByPlayerDBID( playerRole.playerDBID )
			member.roleJade = playerRole.jade

		SpaceCopy.onLeave( self, selfEntity, playerRole, packArgs )
		
	def onLogin( self, selfEntity, playerRole ):
		"""
		"""
		SpaceCopy.onLogin( self, selfEntity, playerRole )
		selfEntity.addYXLMMemberData( playerRole )

	def buyRandomScriptID( self, selfEntity,role,scriptID ):
		"""
		随机事件 购买小兵
		"""
		if scriptID not in selfEntity.randomEventScriptIDDict:
			return
		if role.jade < selfEntity.randomEventScriptIDDict[scriptID]:
			return
		camp = role.getCamp()
		if camp == csdefine.CAMP_TAOSIM:
			route = random.choice(self.specialXianRouteList)
			index = self.specialXianRouteList.index(route)
			dir = self.specialXianDirList[index]
		elif camp == csdefine.CAMP_DEMON:
			route = random.choice(self.specialMoRouteList)
			index = self.specialMoRouteList.index(route)
			dir = self.specialMoDirList[index]
		routeInfo = PatrolRouteLoader.g_patrolRouteLoader.getPatrolRoute( selfEntity.scriptID, route )
		if len(routeInfo):
			param = { "spawnPos": Math.Vector3(routeInfo[1]["position"]), "patrolList":route,"spawnDir":dir, "camp":camp,"way":(index + 1) }
			entity = selfEntity.createEntityByScriptID( scriptID, Math.Vector3(routeInfo[1]["position"]), dir, param )
			if entity:
				role.addJade( -selfEntity.randomEventScriptIDDict[scriptID] )

	