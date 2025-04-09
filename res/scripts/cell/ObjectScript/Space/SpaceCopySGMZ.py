# -*- coding: utf-8 -*-


from ObjectScript.Space.SpaceCopy import SpaceCopy
import KBEngine
import KBEMath
import Functions
import KBEDebug
import csdefine
import csstatus
import random
import Define

FINAL_STAGE_IS_COMPLETE = 7
class SpaceCopySGMZ( SpaceCopy ):
	"""
	上古密阵
	"""
	def __init__( self ):
		SpaceCopy.__init__( self )
		self.revivePosDict = {}
		self.reviveDirDict = {}
		self.monsterDict = {}
		self.modelNumberList = []
		self.stageListStr = []
		self.FinalBossScriptID = ""
		self.killRoleRewardFeats = 0
		self.killRoleExpRate = 0.0
		self.rewardExpRate = 0.0
		self.successRewardFeats = 0
		self.failRewardFeats = 0
		self.killRoleRewardExploit = 0
		self.successRewardExploit = 0
		self.failRewardExploit = 0
		self.succRewardMailToLogonOutPlayer = ""
		self.failRewardMailToLogonOutPlayer = ""

	def initData( self, configData ):
		"""
		virtual method
		"""
		SpaceCopy.initData( self, configData )
		self.spaceUseLevel = configData["SpaceData"].get( "spaceUseLevel", 0 )
		self.revivePosDict = configData["SpaceData"].get( "revivePosDict", {} )
		self.reviveDirDict = configData["SpaceData"].get( "reviveDirDict", {} )
		self.monsterDict = configData["SpaceData"].get( "monsterDict", {} )
		self.FinalBossScriptID = list(self.monsterDict.values())[0].split("|")[-1]		#自动获取最终大BOSS的scriptID
		modelNumberList = configData["SpaceData"].get( "modelNumberList", [] )
		if modelNumberList:
			self.modelNumberList = modelNumberList.split("|")
		self.stageListStr = configData["SpaceData"].get("stageListStr","").split("|")		#["1 2 3","4 5 6"]

		self.killRoleRewardFeats = configData["SpaceData"].get("killRoleRewardFeats",0)
		self.killRoleExpRate = float( configData["SpaceData"].get("killRoleExpRate",0.0) ) 	#击杀玩家奖励系数
		self.rewardExpRate = float( configData["SpaceData"].get("rewardExpRate",0.0) ) #通过奖励经验系数
		self.successRewardFeats = configData["SpaceData"].get("successRewardFeats",0) #胜利奖励的功勋
		self.failRewardFeats = configData["SpaceData"].get("failRewardFeats",0) #失败奖励的功勋
		self.killRoleRewardExploit = configData["SpaceData"].get("killRoleRewardExploit",0) # 击败玩家奖励军功
		self.successRewardExploit = configData["SpaceData"].get("successRewardExploit",0) # 胜利奖励军功
		self.failRewardExploit = configData["SpaceData"].get("failRewardExploit",0) #失败奖励军功
		self.succRewardMailToLogonOutPlayer = configData["SpaceData"].get("succRewardMailToLogonOutPlayer","") # 胜利意外掉线玩家奖励
		self.failRewardMailToLogonOutPlayer = configData["SpaceData"].get("failRewardMailToLogonOutPlayer","") # 失败意外掉线玩家奖励

	def initEntity( self, selfEntity ):
		"""
		virtual method
		初始化space entity要做的事情
		"""
		selfEntity.initSpaceData( self.monsterDict, self.stageListStr, self.FinalBossScriptID  )
		selfEntity.spaceLevel = self.spaceUseLevel
		SpaceCopy.initEntity( self, selfEntity )
		
	def setReviveType( self ):
		"""
		设置复活类型
		"""
		pass

	def getRewardExpRate( self ):
		return self.rewardExpRate

	def getKillRoleRewardFeats( self ):
		return self.killRoleRewardFeats

	def getKillRoleExpRate( self ):
		return self.killRoleExpRate

	def getSuccessRewardFeats( self ):
		return self.successRewardFeats

	def getFailRewardFeats( self ):
		return self.failRewardFeats

	def getKillRoleRewardExploit( self ):
		return self.killRoleRewardExploit

	def getSuccessRewardExploit( self ):
		return self.successRewardExploit

	def getFailRewardExploit( self ):
		return self.failRewardExploit

	def getSuccRewardMailToLogonOutPlayer( self ):
		return self.succRewardMailToLogonOutPlayer

	def getFailRewardMailToLogonOutPlayer( self ):
		return self.failRewardMailToLogonOutPlayer

	def getReviveInfos( self, selfEntity, palyer ):
		"""
		复活方式
		"""
		route = selfEntity.member[palyer.getCamp()]
		monsterList = self.monsterDict[ route ].split("|")
		posList = self.revivePosDict[ route ].split("|")
		dirList = self.reviveDirDict[ route ].split("|")
		if len( selfEntity.getEntityRecord( monsterList[0] ) ) > 0:
			return KBEMath.Unreal2KBEnginePosition( Functions.vector3TypeConvert( posList[0] )), KBEMath.Unreal2KBEngineDirection( Functions.vector3TypeConvert( dirList[0] ))
		elif len( selfEntity.getEntityRecord( monsterList[0] ) ) == 0 and len( selfEntity.getEntityRecord( monsterList[1] ) ) > 0:
			return KBEMath.Unreal2KBEnginePosition( Functions.vector3TypeConvert( posList[1] )), KBEMath.Unreal2KBEngineDirection( Functions.vector3TypeConvert( dirList[1] ))
		else:
			return KBEMath.Unreal2KBEnginePosition( Functions.vector3TypeConvert( posList[2] )), KBEMath.Unreal2KBEngineDirection( Functions.vector3TypeConvert( dirList[2] ))
			
	def onSpaceSuccess( self, selfEntity, isShowTimeCountDown = True ):
		"""
		副本通关
		isShowTimeCountDown 是否显示倒计时提示 见JIRA-3404
		"""
		selfEntity.popTimer(selfEntity.timeID)
		self.stopSpaceLife( selfEntity )
		self.spaceEvent_onSpaceSuccess( selfEntity )
		self.spaceBunch_onSpaceSuccess( selfEntity )
		self.spaceSettlement_onSpaceSuccess( selfEntity )	#必须在stopSpaceLife后调用
		selfEntity.addTimerCallBackForScript( 1.0,"onSpaceSuccessSpaceSettlement",() )
		if isShowTimeCountDown:
			selfEntity.addTimerCallBack( 60, "closeSpace", () )
			if self.getSpaceType() == csdefine.SPACE_TYPE_STORY_COPY:
				selfEntity.addTimerCallBackForScript( 50, "showTimeCountDown", ( csstatus.SPACE_PLANE_CLOSE_NOTIFY, 10 ) )
			else:
				selfEntity.addTimerCallBackForScript( 50, "showTimeCountDown", ( csstatus.SPACE_CLOSE_NOTIFY, 10 ) )
			for roleCell in selfEntity._spaceRoles:
				roleCell.statusMessage( csstatus.SPACE_SUCCESS_TELEPORT,60 )
				
	def onLastPlayerLeave( self, selfEntity, playerRole, packArgs ):
		"""
		virtual method
		最后一个玩家离开副本
		"""
		selfEntity.leaveCloseTimer = selfEntity.addTimerCallBack( 1.0, "closeSpace", () )

	def onSpaceSuccessSpaceSettlement( self, selfEntity ):
		"""
		副本通关 显示结算界面
		"""
		#计算帮贡奖励
		selfEntity.addFinalContributionReward()
		selfEntity.addFinalExploitReward()
		selfEntity.addLogoutMemberReward()
		for role in selfEntity._spaceRoles:
			if role.getClient():
				#显示阵营竞技结算奖励
				if role.playerDBID in selfEntity.zyjjRewardDatas:
					role.client.ShowZYJJReward(selfEntity.zyjjRewardDatas[role.playerDBID])
				role.client.SGMZOnWinGame( selfEntity.memberDatas )
				
	def hasSpaceStage( self, selfEntity ):
		pass

	def spaceStage_onSpaceInit( self, selfEntity ):
		"""
		"""
		selfEntity.currentStageList = []
		if self.beginOnInit:
			for camp, stageList in selfEntity.camp_stage.items():
				self.setSpaceStage( selfEntity, stageList[0], camp )

	def onMonsterHPChanged( self, selfEntity, monsterEntity ):
		"""
		怪物血量改变
		"""
		SpaceCopy.onMonsterHPChanged( self, selfEntity, monsterEntity )
		for key,val in self.monsterDict.items():			#判断是否为小BOSS（不是普通怪和最终BOSS）
			monsterList = val.split("|")
			if monsterEntity.scriptID in monsterList and monsterEntity.scriptID != self.FinalBossScriptID :
				selfEntity.onBossHPChanged( monsterEntity )				#具体的客户端表现(比分横幅界面)
				break

	def onAddExp( self, selfEntity, playerRole, exp, reason):
		"""
		增加经验
		"""
		SpaceCopy.onAddExp( self, selfEntity, playerRole, exp, reason)
		selfEntity.recordStageExp[ playerRole.camp ] = exp

	def setSpaceStage( self, selfEntity, stageIndex, camp ):
		"""
		设置副本当前阶段
		"""
		stage = self.getStageByIndex( stageIndex )
		if not stage:
			return
		if stageIndex in selfEntity.completeSpaceStages:#如果在已完成列表中就不用重新设置，否则会导致界面出现2个相同的阶段
			return
		selfEntity.currentStageList.append(stage)
		self.onCurrentStageStart( selfEntity, stage, camp )

	def onCurrentStageStart( self, selfEntity, stage, camp ):
		"""
		当前阶段开始
		"""
		selfEntity.recordStageExp[ camp ] = 0
		selfEntity.campStageStartTime[camp] = Functions.getTime()
		for role in selfEntity._spaceRoles:
			if role.getCamp() == camp:
				role.client.CLIENT_showSpaceStageWin( self.stageFileName,self.getCompleteStageNameByCamp( selfEntity, camp ), stage.packToString() )
				self.sendCurrentSpaceStageTaskArea( selfEntity, role, stage )
		#必须放在后面执行，因为updateSpaceStage可能导致阶段完成
		changedTasks = stage.updateGetItemTask( selfEntity )	#获取物品类目标在开始的时候要刷一下已完成数量
		self.updateCurrentSpaceStage( selfEntity, stage, changedTasks )

	def onStageStart( self, selfEntity ):
		"""
		阶段开始
		"""
		pass

	def updateCurrentSpaceStage( self, selfEntity, stage, changedTasks ):
		"""
		阶段目标计数更新
		"""
		if len( changedTasks ) == 0:
			return
		tempList = []
		for taskIndex, val in changedTasks:
			tempList.append( { "taskIndex":taskIndex, "val":val } )
		tempString = Functions.toJsonString( tempList )

		camp = selfEntity.getCampByStageIndex( stage.stageIndex )
		for role in selfEntity._spaceRoles:
			if role.getCamp() == camp  or stage.stageIndex == FINAL_STAGE_IS_COMPLETE:
				role.client.CLIENT_updateSpaceStageWin( stage.stageIndex, tempString )

		if stage.isCompleted():
			self.onCurrentStageComplete( selfEntity, stage )

	def updateSpaceStage( self, selfEntity, changedTasks ):
		"""
		阶段目标计数更新
		"""
		pass

	def onCurrentStageComplete( self, selfEntity, stage ):
		"""
		阶段完成
		"""
		selfEntity.completeSpaceStages.append( stage.stageIndex )
		stageCamp = selfEntity.getCampByStageIndex( stage.stageIndex )
		for role in selfEntity._spaceRoles:
			if role.getCamp() == stageCamp or stage.stageIndex == FINAL_STAGE_IS_COMPLETE:
				role.client.RefreshAroundBoxStatus( csdefine.SPELL_BOX_LISTEN_EVENT_SPACE_STAGE_COMPLETE )
				role.client.CLIENT_updateCompleteSpaceStage( self.getCompleteStageNameByCamp( selfEntity,stageCamp ) )
			
		self.spaceEvent_onStageComplete( selfEntity, stage.stageIndex )
		self.removeCurrentSpaceStage( selfEntity, stage.stageIndex )
		nextStageIndex = self.getNextStageIndex( selfEntity, stage.stageIndex, stageCamp )
		if nextStageIndex:
			if self.beginOnInit:
				self.setSpaceStage( selfEntity, nextStageIndex, stageCamp )

	def getNextStageIndex( self, selfEntity, stageIndex, stageCamp ):
		"""
		"""
		stageIndexList = selfEntity.camp_stage[ stageCamp ]
		index = stageIndexList.index(stageIndex)
		if index + 1 < len(stageIndexList):
			return stageIndexList[index + 1]
		return None

	def removeCurrentSpaceStage( self, selfEntity, stageIndex ):
		"""
		"""
		for spaceStage in selfEntity.currentStageList:
			if spaceStage.stageIndex == stageIndex:
				selfEntity.currentStageList.remove(spaceStage)
				break

	def onStageComplete( self, selfEntity ):
		"""
		阶段完成
		"""
		pass

	def getCompleteStageNameByCamp( self, selfEntity,camp ):
		"""
		获取某一camp已完成的阶段的标题 
		"""
		tempList = []
		for stageIndex in selfEntity.completeSpaceStages:
			for stage in self.spaceStages:
				stageCamp = selfEntity.getCampByStageIndex( stage.stageIndex )
				if stage.stageIndex == stageIndex and camp == stageCamp:
					tempList.append( stage.title )
					break
		return tempList

	def getCompleteSpaceStageName( self, selfEntity ):
		"""
		获取已完成的阶段的标题
		"""
		pass

	def spaceStage_onPlayerEnter( self, selfEntity, roleCell ):
		"""
		玩家进副本
		"""
		KBEngine.globalData["CampSGMZCopyMgr"].onEnterSpaceCopySGMZ( roleCell.base )
		roleCamp = roleCell.getCamp()
		currentStage = None
		for stage in selfEntity.currentStageList:
			if selfEntity.getCampByStageIndex( stage.stageIndex ) == roleCamp:
				currentStage = stage
				break
		if currentStage:
			roleCell.client.CLIENT_showSpaceStageWin( self.stageFileName, self.getCompleteStageNameByCamp( selfEntity,roleCamp), currentStage.packToString() )
			self.sendCurrentSpaceStageTaskArea( selfEntity, roleCell,currentStage )

			changedTasks = currentStage.updateGetItemTask( selfEntity )	#获取物品类目标在玩家进入副本的时候要刷一下已完成数量
			self.updateCurrentSpaceStage( selfEntity, currentStage, changedTasks )
		else:
			if len(selfEntity.completeSpaceStages) != 0:
				roleCell.client.CLIENT_showSpaceStageWin( self.stageFileName, self.getCompleteStageNameByCamp( selfEntity,roleCamp ), "" )

	def spaceStage_onPlayerLeave( self, selfEntity, roleCell ):
		"""
		玩家出副本
		"""
		roleCell.client.CLIENT_hideSpaceStageWin()		#没有stage也要隐藏一下，因为stage完成后界面还在
		currentStage = None
		for stage in selfEntity.currentStageList:
			if selfEntity.getCampByStageIndex( stage.stageIndex ) == roleCell.getCamp():
				currentStage = stage
				break
		if currentStage:
			roleCell.client.CLIENT_ClearSpaceStageTaskArea()
			changedTasks = currentStage.updateGetItemTask( selfEntity )	#获取物品类目标在玩家离开副本的时候要刷一下已完成数量
			self.updateCurrentSpaceStage( selfEntity, currentStage, changedTasks )

	#-------------------------------
	# 阶段目标区域相关
	#-------------------------------
	def sendCurrentSpaceStageTaskArea( self, selfEntity, roleCell, currentStage ):
		"""
		阶段目标区域发送到客户端，用于触发“进入某范围”阶段目标
		"""
		tempList = []
		for task in currentStage.tasks:
			if task.getType() == Define.SPACE_STAGE_TASK_ENTER_AREA:
				tempDict = { "taskIndex": task.taskIndex, "shapeType": task.param1, "areaZRange": task.param2, "areaParam": task.param3 }
				tempList.append( tempDict )
		
		if len(tempList) == 0:
			return
		roleCell.client.CLIENT_AddSpaceStageTaskArea( self.scriptID, currentStage.stageIndex, Functions.toJsonString( tempList ) )


	def sendSpaceStageTaskArea( self, selfEntity, roleCell ):
		"""
		阶段目标区域发送到客户端，用于触发“进入某范围”阶段目标
		"""
		pass

	def onEnterSpaceStageArea( self, selfEntity, stageIndex, taskIndex ):
		"""
		玩家进入阶段目标区域
		"""
		for spaceStage in selfEntity.currentStageList:
			if spaceStage.stageIndex == stageIndex:
				changedTasks = spaceStage.onEnterTaskArea( taskIndex )
				self.updateCurrentSpaceStage( selfEntity, spaceStage, changedTasks )

	#------------------------------------
	# 各种阶段目标触发接口
	#------------------------------------
	def spaceStage_onMonsterDie( self, selfEntity, monsterScriptID ):
		"""
		怪物死亡
		"""
		pass

	def spaceStage_onMonsterBeKill( self, selfEntity, monsterScriptID, killEntity ):
		"""
		怪物死亡
		"""
		for spaceStage in selfEntity.currentStageList:
			if monsterScriptID == self.FinalBossScriptID :
				changedTasks = spaceStage.onMonsterDie( monsterScriptID )
				self.updateCurrentSpaceStage( selfEntity, spaceStage, changedTasks )
				return
			else:
				camp = selfEntity.getCampByStageIndex( spaceStage.stageIndex )
				if killEntity.getCamp() == camp:
					changedTasks = spaceStage.onMonsterDie( monsterScriptID )
					self.updateCurrentSpaceStage( selfEntity, spaceStage, changedTasks )


	def spaceStage_onTriggerBox( self, selfEntity, scriptID ):
		"""
		箱子被触发
		"""
		for spaceStage in selfEntity.currentStageList:
			changedTasks = spaceStage.onTriggerBox( scriptID )
			self.updateCurrentSpaceStage( selfEntity, spaceStage, changedTasks )

	def spaceStage_onNPCObjectDestroy( self, selfEntity, enityID, entityScriptID ):
		"""
		NPCObject销毁
		"""
		for spaceStage in selfEntity.currentStageList:
			changedTasks = spaceStage.onNPCObjectDestroy( entityScriptID )
			self.updateCurrentSpaceStage( selfEntity, spaceStage, changedTasks )

	def spaceStage_onConditionChange( self, selfEntity, senderType, senderID, conditionKey, extraValue ):
		"""
		副本某条件发生改变
		"""
		for spaceStage in selfEntity.currentStageList:
			changedTasks = spaceStage.onConditionChange( senderType, senderID, conditionKey, extraValue )
			self.updateCurrentSpaceStage( selfEntity, spaceStage, changedTasks )

	def spaceStage_onPlayerGetItem( self, selfEntity, itemID, amount ):
		"""
		玩家获得物品
		"""
		for spaceStage in selfEntity.currentStageList:
			changedTasks = spaceStage.onPlayerGetItem( itemID, amount )
			self.updateCurrentSpaceStage( selfEntity, spaceStage, changedTasks )

	def spaceStage_onPlayerRemoveItem( self, selfEntity, itemID, amount ):
		"""
		玩家移除物品
		"""
		for spaceStage in selfEntity.currentStageList:
			changedTasks = spaceStage.onPlayerRemoveItem( selfEntity, itemID, amount )
			self.updateCurrentSpaceStage( selfEntity, spaceStage, changedTasks )

	def spaceStage_forceCompleteStageTask( self, selfEntity, taskIndex ):
		"""
		强制完成当前阶段目标
		"""
		for spaceStage in selfEntity.currentStageList:
			changedTasks = spaceStage.forceCompleteStageTask( taskIndex )
			self.updateCurrentSpaceStage( selfEntity, spaceStage, changedTasks )

	def spaceStage_forceSetCurrentStageTaskClear( self, selfEntity, taskIndex  ):
		"""
		强制设置当前阶段目标清0 具体在CST-2936有使用
		"""
		for spaceStage in selfEntity.currentStageList:
			changedTasks = spaceStage.forceSetCurrentStageTaskClear( taskIndex )
			self.updateCurrentSpaceStage( selfEntity, spaceStage, changedTasks )

	def spaceStage_onPlayerUseItem( self, selfEntity, itemID, amount ):
		"""
		玩家使用物品
		"""
		for spaceStage in selfEntity.currentStageList:
			changedTasks = spaceStage.onPlayerUseItem( selfEntity, itemID, amount )
			self.updateCurrentSpaceStage( selfEntity, spaceStage, changedTasks )

	def spaceStage_gmCompleteStageTask( self, selfEntity, taskIndex, progress ):
		"""
		gm强制完成当前阶段目标
		"""
		for spaceStage in selfEntity.currentStageList:
			changedTasks = spaceStage.gmCurrentStageTask( taskIndex, progress )
			if not changedTasks:
				return False
			self.updateCurrentSpaceStage( selfEntity, spaceStage, changedTasks )
			return True

	def getPackDomainData( self, playerEntity, args ):
		"""
		"""
		packDict = SpaceCopy.getPackDomainData( self, playerEntity, args )
		packDict["playerDBID"] = playerEntity.playerDBID
		return packDict
		
	#------------------------------------
	# 废弃
	#------------------------------------
	def onSpaceCreateEntity( self, selfEntity, scriptIDList ):
		"""
		创建NPC队伍
		"""
		robotRouteList = ["0","1","2","3"]
		for route in selfEntity.member.values():
			robotRouteList.remove( route )
		route = random.choice(robotRouteList)
		posList = self.revivePosDict[ route ].split("|")
		dirList = self.reviveDirDict[ route ].split("|")
		posStr = random.choice( posList )
		dirStr = random.choice( dirList )
		createPos = Functions.vector3TypeConvert( posStr )
		createDir = Functions.vector3TypeConvert( dirStr )
		for i in range( len(selfEntity.manMemberData) ):
			newEntity = selfEntity.createEntityByScriptID(scriptIDList[i], KBEMath.Unreal2KBEnginePosition(createPos), KBEMath.Unreal2KBEngineDirection(createDir) ,{ "spawnPos":KBEMath.Unreal2KBEnginePosition(createPos),"spawnDir":KBEMath.Unreal2KBEngineDirection(createDir)})
			newEntity.robotName = selfEntity.manMemberData[i]["name"]
			newEntity.robotLevel = selfEntity.manMemberData[i]["level"]
			newEntity.robotCamp = selfEntity.manMemberData[i]["camp"]
			newEntity.occupation = selfEntity.manMemberData[i]["profession"]
			if newEntity.occupation == csdefine.CLASS_FIGHTER:
				newEntity.setModelNumber( self.modelNumberList[0] )
			elif newEntity.occupation == csdefine.CLASS_SWORDMAN:
				newEntity.setModelNumber( self.modelNumberList[1] )
			elif newEntity.occupation == csdefine.CLASS_ARCHER:
				newEntity.setModelNumber( self.modelNumberList[2] )
			else:
				newEntity.setModelNumber( self.modelNumberList[3] )
