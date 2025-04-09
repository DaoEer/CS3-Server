# -*- coding: utf-8 -*-

import csdefine
import KBEDebug
import QuestEventDefine
from RoleActivityRecordMgr import g_activityRecordMgr
from ObjectScript.ObjectScriptFactory import g_objFactory
import ActivityBunchModule
import csstatus
import KST
import Const
import KBEngine
import ItemFactory
import KBEMath
import Functions


class RoleActivityInterface:
	"""
	玩家活动接口
	"""
	def __init__( self ):
		"""
		"""
		self.isMatchCampRandomFit = False
		self.isMatchBattleActivity = False
		self.isDeclarePointBHZB = False
		self.recordPointIndex = 0

	def beforeDestroy( self ):
		"""
		销毁前做一些事
		"""
		if self.isMatchCampRandomFit:
			KBEngine.globalData["CampActivityRandomFitMgr"].randomFit_onPlayerLoginOff( self.base, self.getName() )
		if self.isMatchBattleActivity:
			KBEngine.globalData['BattleActivityMgr'].onPlayerLoginOff(self.base)
		if self.isDeclarePointBHZB:
			KBEngine.globalData["BHZBManager"].cancelDeclareBHZBPoint( self.tongDBID,self.camp,self.recordPointIndex,self.base,self.playerDBID )
			self.recordPointIndex = 0
		
	def getActivityTimes( self ):
		"""
		define method
		获取活动次数
		"""
		data = []
		for actType in csdefine.ACTIVITY_TYPE_LIST:
			data.append({"type":actType, "times": self.getActivityDegree(actType)})
		self.client.recvActivityTimesData(Functions.toJsonString(data))
	
	#--------------------------活动参与次数相关-----------------------------
	def isExceedActivityDegree( self, activityType ):
		"""
		某活动参与次数是否超过额定值
		"""
		return g_activityRecordMgr.isExceedActivityDegree( self, activityType )
	
	def getActivityDegree( self, activityType ):
		"""
		获取某活动参与次数
		"""
		return g_activityRecordMgr.getActivityDegree( self, activityType )
	
	def addActivityDegree( self, activityType ):
		"""
		<define method>
		增加某活动参与记录
		"""
		g_activityRecordMgr.addActivityDegree( self, activityType )
		if self.getClient(): self.getClient().updateActivityTimesData(activityType, self.getActivityDegree(activityType))
	
	def clearActivityDegree( self, activityType ):
		"""
		清除某活动参与记录
		"""
		g_activityRecordMgr.clearActivityDegree( self, activityType )

	def getMaxDegree( self, activityType ):
		"""
		清除某活动参与记录
		"""
		return g_activityRecordMgr.getMaxDegree( self, activityType )
	
	#----------------------------副本串----------------------------------
	def onEnterBunchSpace( self, bunshSpaceScriptID, isFirstEnter, activityType ):
		"""
		<define method>
		进副本串
		"""
		if isFirstEnter:
			if bunshSpaceScriptID not in self.enteredBunchRecord:
				self.enteredBunchRecord.append( bunshSpaceScriptID )
		
		bunchObj = g_objFactory.getBunchSpaceObject( bunshSpaceScriptID )
		# 潜能副本串
		if bunchObj.bunchType == csdefine.SPACE_BUNCH_TYPE_POTENTAIL:
			if isFirstEnter:
				self.addActivityDegree( csdefine.ACTIVITY_TYPE_POTENTAIL_SPACE )
			self.triggerQuestEvent( QuestEventDefine.EVENT_ENTER_POTENTIAL_COPY, None )
		
		# 传承副本串
		elif bunchObj.bunchType == csdefine.SPACE_BUNCH_TYPE_CHUANCHENG:
			if isFirstEnter:
				self.addActivityDegree( activityType )
			self.triggerQuestEvent( QuestEventDefine.EVENT_ENTER_CHUAN_CHENG_COPY, None )


	#---------------------------活动串接口----------------------------------
	def actBunch_signUp( self, bunchName ):
		"""
		申请参加某个活动串
		"""
		ActivityBunchModule.signUp( bunchName, self )

	def actBunch_joinNotarize( self, bunchName,actName,activityKey ):
		"""
		申请参加活动的回调
		"""
		self.bunchName = bunchName
		self.actName = actName
		self.activityKey = activityKey
		self.client.CLIENT_ShowEnterActBunchWindow()

	def actBunch_join( self, bunchName, actName, activityKey ):
		"""
		参加某个活动串
		"""
		ActivityBunchModule.join( bunchName, actName, self, {} )
		
	def actBunch_joinNext( self, bunchName, actName, params ):
		"""
		参加下一个活动
		"""
		ActivityBunchModule.joinNext( bunchName, actName, self, params )

	def actBunch_onAddJoinner( self, bunchName, actName, result ):
		"""
		参加活动回调
		"""
		ActivityBunchModule.onAddJoinner( bunchName, actName, self, result )

	def actBunch_abandon( self, bunchName, actName, activityKey ):
		"""
		放弃活动
		"""
		KBEngine.globalData["ActivityBunchManager"].abandon( self.base , bunchName, actName, activityKey, self.playerDBID )

	def enterActBunch( self, exposed ):
		"""
		exposed
		玩家点击进入
		"""
		if not self.validateClientCall( exposed ):
			return
		if self.isInTeam():
			return
		self.actBunch_join( self.bunchName, self.actName, self.activityKey )

	def abandonActBunch( self, exposed ):
		"""
		玩家放弃比赛
		"""
		if not self.validateClientCall( exposed ):
			return
		self.actBunch_abandon( self.bunchName, self.actName, self.activityKey )

	def onYeZhanFengQiEnd( self ):
		"""
		血斗凤栖镇结束
		"""
		if self.getClient():
			self.client.CLIENT_ShowFengQiRank()
		self.addTimerCallBack(5.0,"inquireMessage",( (( csstatus.YE_ZHAN_FENG_QI_END_MESSAGE,[10],"isExitYeZhanFengQi" )) ))

	def isExitYeZhanFengQi( self, reply ):
		"""
		是否退出血斗凤栖镇
		"""
		if reply:
			self.gotoExitSpacePos()

	def fengQiMemberOut( self ):
		"""
		血斗凤栖镇玩家积分为0提示
		#这里加四秒延迟  是由于客户端播完死亡动作后会弹出复活框会将改提示框覆盖掉
		"""
		self.addTimerCallBack( 4.0,"inquireMessage",(  ( csstatus.YE_ZHAN_FENG_QI_MEMBER_OUT,[10],"onfengQiMemberOut" )) )

	def onfengQiMemberOut( self, reply ):
		"""
		是否退出血斗凤栖镇
		"""
		if reply:
			self.reviveOnOrigin()
			self.addTimerCallBack( 1.0, "gotoExitSpacePos", () )

	def CELL_leaveYeZhanFengQi( self, exposed ):
		"""
		exposed method
		离开血斗凤栖镇
		"""
		if not self.validateClientCall( exposed ):
			return
		if self.getCurrentSpaceObject().getSpaceChildType() != csdefine.SPACE_CHILD_TYPE_YZFQ:
			return
		self.reviveOnOrigin()
		self.addTimerCallBack( 1.0, "gotoExitSpacePos", () )
		
	#---------------------------幻阵迷宫接口----------------------------------
	def onEnterMagicMazeSpace(self, activityType):
		"""
		define method
		记录进入幻阵迷宫次数
		"""
		self.addActivityDegree( activityType )
			
	#---------------------------帮会副本接口----------------------------------
	def onEnterTongSpaceCopy( self ):
		self.addActivityDegree( csdefine.ACTIVITY_TYPE_TONG_SPACE_COPY )

	#---------------------------帮会日常接口----------------------------------
	def onAcceptTongDailyQuest( self ):
		self.addActivityDegree( csdefine.ACTIVITY_TYPE_TONG_DAILY_QUEST )

	#--------------------------英雄王座接口----------------------------------
	def onEnterCampYXLM( self ):
		self.addActivityDegree( csdefine.ACTIVITY_TYPE_CAMP_YXLM )

	def CELL_YXLMBackToCity( self, srcEntityID ):
		"""
		英雄王座 回城
		exposed method
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		spaceEntity = self.getCurrentSpace()
		if spaceEntity and spaceEntity.getScript().getSpaceChildType() == csdefine.SPACE_CHILD_TYPE_YXLM:
			skillID = spaceEntity.getScript().getReviveSkillIDByCamp( self )
			self.useSkillToEntity( skillID, self.id )

	def CELL_YXLMBuyRandomScriptID( self, srcEntityID,scriptID ):
		"""
		随机事件中购买小兵
		exposed method
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		spaceEntity = self.getCurrentSpace()
		if spaceEntity and spaceEntity.getScript().getSpaceChildType() == csdefine.SPACE_CHILD_TYPE_YXLM:
			spaceEntity.buyRandomScriptID( self ,scriptID )

	#--------------------------活动：帮会争霸----------------------------------
	def tongStarcraft_firstSignUp( self, srcEntityID, firstTeamNames,secondTeamNames,thirdTeamNames,fourTeamNames ):
		"""
		exposed method
		报名帮会争霸
		"""
		if not self.validateClientCall(srcEntityID):
			return
		if not self.isTongLeader():
			self.statusMessage( csstatus.TONG_STARCRAFT_SIGNUP_HASNOT_GRADE,"" )
			return
		totalSignUpNames = []
		totalSignUpNames.extend(firstTeamNames)
		totalSignUpNames.extend(secondTeamNames)
		totalSignUpNames.extend(thirdTeamNames)
		totalSignUpNames.extend(fourTeamNames)
		if len(totalSignUpNames) != Const.TONG_STARCRAFT_JOIN_MEMBER:
			KBEDebug.ERROR_MSG("Member is not enough")
			return

		if self.tongMB:
			self.tongMB.tongStarcraft_firstSignUp( self.base,self.playerDBID,firstTeamNames,secondTeamNames,thirdTeamNames,fourTeamNames )

	def tongStarcraft_SecondSignUp( self, srcEntityID, signupNames ):
		"""
		exposed method
		报名帮会争霸第二场
		"""
		if not self.validateClientCall(srcEntityID):
			return

		if not self.isTongLeader():
			self.statusMessage( csstatus.TONG_STARCRAFT_SIGNUP_HASNOT_GRADE,"" )
			return

		if len( signupNames ) != Const.TONG_STARCRAFT_JOIN_MEMBER:
			KBEDebug.ERROR_MSG("Member is not enough")
			return

		if self.tongMB:
			self.tongMB.tongStarcraft_SecondSignUp( self.base, self.playerDBID, signupNames )

	def firstTongStarcraftSignUp( self, srcEntityID, signUpPlayerNames ):
		"""
		exposed mehtod
		报名帮会争霸第一场
		"""
		if not self.validateClientCall( srcEntityID ):
			return

		if not self.isTongLeader():
			self.statusMessage( csstatus.TONG_STARCRAFT_SIGNUP_HASNOT_GRADE,"" )
			return

		if len( signUpPlayerNames ) != Const.TONG_STARCRAFT_JOIN_MEMBER:
			KBEDebug.ERROR_MSG("Member is not enough")
			return

		if self.tongMB:
			self.tongMB.firstTongStarcraftSignUp( self.base, self.playerDBID, signUpPlayerNames )


	#------------------------------------帮会阵营战 JIRA CST-8722---------------------------------------------
	def tongCampWarSignUp( self, srcEntityID, signUpPlayerNames ):
		"""
		exposed mehtod
		报名帮会阵营战
		"""
		if not self.validateClientCall( srcEntityID ):
			return

		if not self.isTongLeader():
			self.statusMessage( csstatus.TONG_CAMP_WAR_IS_NOT_LEADER,"" )
			return

		if self.tongMB:
			self.tongMB.tongCampWarSignUp( self.base, signUpPlayerNames )

	#---------------------------灵脉战场 JIRA:CST-4054---------------------------------------------
	def telportLMZCActivity( self, key ):
		"""
		define method
		匹配成功
		"""
		spaceObj = KST.g_objFactory.getSpaceObject( Const.LMZC_SPACE_SCRIPTID )
		if spaceObj:
			pos, dir = spaceObj.getEnterInfoByCamp( self.camp )
			self.gotoSpaceUseArg( Const.LMZC_SPACE_SCRIPTID, pos, dir, {"spaceKey" : "lingmai_" + str(key)})
		else:
			KBEDebug.ERROR_MSG("Can not find space scriptID(%s)"%Const.LMZC_SPACE_SCRIPTID)

	def CELL_requestSameCampPos( self, srcEntityID ):
		"""
		exposed method
		获取
		"""
		if not self.validateClientCall(srcEntityID):
			return
		space = self.getCurrentSpace()
		if space:
			space.requestSameCampPos( self, self.camp )

	#---------------------------冰雪之战 JIRA:CST-4056---------------------------------------------
	def telportFrozenFightActivity( self, key ):
		"""
		define method
		匹配成功
		"""
		spaceObj = KST.g_objFactory.getSpaceObject( Const.FROZEN_FIGHT_SPACE_SCRIPTID )
		if spaceObj:
			pos, dir = spaceObj.getEnterInfoByCamp( self.camp )
			self.gotoSpaceUseArg( Const.FROZEN_FIGHT_SPACE_SCRIPTID, pos, dir, {"spaceKey" : "frozenfight_" + str(key)})
		else:
			KBEDebug.ERROR_MSG("Can not find space scriptID(%s)"%Const.FROZEN_FIGHT_SPACE_SCRIPTID)

	def leaveFrozenFight(self, exposed):
		"""
		Exposed method
		退出战场
		"""
		if not self.validateClientCall( exposed ):
			return
		spaceEntity = self.getCurrentSpace()
		if not spaceEntity:
			return
		self.gotoExitSpacePos()

	#---------------------------十方城---------------------------------------------
	def shiFangChengJoinNotice( self, activityKey ):
		"""
		"""
		self.activityKey = activityKey
		self.client.CLIENT_ShowEnterActBunchWindow()

	def CELL_enterShiFangCheng( self, exposed ):
		"""
		进入十方城
		"""
		if not self.validateClientCall( exposed ):
			return
		if self.isInTeam():
			self.base.leaveTeamFB( self.id )
		KBEngine.globalData["PersonStarcraftMgr"].gotoShiFangCheng( self.base,self.activityKey, self.playerDBID )

	def CELL_abandonShiFangeCheng( self, exposed ):
		"""
		放弃十方城
		"""
		if not self.validateClientCall( exposed ):
			return
		KBEngine.globalData["PersonStarcraftMgr"].abandonShiFangeCheng( self.activityKey, self.playerDBID )

	def yeZhanFengQiJoinNotice( self ):
		"""
		"""
		self.client.ShowEnterYeZhanFengQiWindow()

	def enterYeZhanFengQi( self, srcEntityID ):
		"""
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		if self.isInTeam():
			self.base.leaveTeamFB( self.id )
		activityKey = int(self.getLevel() / 10)
		KBEngine.globalData["PersonStarcraftMgr"].gotoYeZhanFengQi( self.base,activityKey,self.playerDBID )

	#---------------------------福袋活动---------------------------------------------
	def CELL_onUseItemJZYT(self, exposed, uid, spaceStr):
		"""
		选择使用金枝玉庭物品后
		"""
		if not self.validateClientCall( exposed ):
			return
		item = self.getItemInstByUid(int(uid))
		self.removeItemByAmount( item, 1, csdefine.ITEM_REMOVE_BY_USE )
		argList = spaceStr.split()
		position  = KBEMath.Unreal2KBEnginePosition((float(argList[1]) , float(argList[2]) , float(argList[3])))
		direction = KBEMath.Unreal2KBEngineDirection((float(argList[4]), float(argList[5]), float(argList[6])))
		self.gotoSpace( argList[0], position, direction )

	def beginUseZBN(self, gItemID, uid, itemID, greyBuff, buffID):
		"""
		开始使用珍宝囊
		"""
		self.inquireMessage( csstatus.ZHEN_BAO_NANG_USE , [], "onUseZBN", gItemID, uid, itemID, buffID)

	def onUseZBN(self, isuse, gItemID, uid, itemID, greyBuff, buffID):
		"""
		使用珍宝囊后的回调
		"""
		if not isuse:
			return
		self.statusMessage( csstatus.ZHEN_BAO_NANG_USE_END )
		item = self.getItemInstByUid(int(uid))
		self.removeItemByAmount( item, 1, csdefine.ITEM_REMOVE_BY_USE )
		additemInst = ItemFactory.ItemFactoryInst.createDynamicItem( int(gItemID) )
		self.addItem( itemInst, csdefine.ITEM_ADD_BY_SYS )
		self.client.CLIENT_GreyItem(itemID)
		self.addBuff(self, buffID)
		self.addBuff(self, greyBuff)

	def startLLBZ(self):
		"""
		开始玲珑宝珠
		"""
		self.getCurrentSpaceObject().startLLBZ(self)	

	def beginUseZBH(self, gItemID, uid, greyBuff, param):
		"""
		开始使用珍宝盒
		"""
		self.inquireMessage( csstatus.ZHEN_BAO_HE_USE , [], "onUseZBH", gItemID, uid, itemID, param)

	def onUseZBH(self, isuse,gItemID, uid, greyBuff, param):
		"""
		使用珍宝盒后的回调
		"""
		if not isuse:
			return
		self.statusMessage( csstatus.ZHEN_BAO_HE_USE_END )
		item = self.getItemInstByUid(int(uid))
		self.removeItemByAmount( item, 1, csdefine.ITEM_REMOVE_BY_USE )
		additemInst = ItemFactory.ItemFactoryInst.createDynamicItem( int(gItemID) )
		self.addItem( itemInst, csdefine.ITEM_ADD_BY_SYS )
		self.addBuff(self.greyBuff)
		self.client.CLIENT_ShowAreaInBigMapUI(param[0], param[1], param[2][0])
		for i in param[2:]:
			self.client.CLIENT_AddActivityCircleArea(param[0], param[1], i[0], i[1])

	def CELL_onEnterActivityCircleArea(self, exposed, areaIndex):
		"""
		Exposed method
		进入活动圆形区域
		"""
		if not self.validateClientCall( exposed ):
			return
		self.getCurrentSpaceObject().onEnterActivityCircleArea(self, areaIndex)

		
	def CELL_onLeaveActivityCircleArea(self, exposed, areaIndex):
		"""
		Exposed method
		离开活动圆形区域
		"""
		if not self.validateClientCall( exposed ):
			return	
		self.getCurrentSpaceObject().onLeaveActivityCircleArea(self, areaIndex)

#---------------------------虚空探宝活动---------------------------------------------
	def onUseItemXKTB( self, exposed, uid, spaceStr ):
		"""
		选择使用虚空探宝物品后
		"""
		if not self.validateClientCall( exposed ):
			return
		item = self.getItemInstByUid(int(uid))
		self.removeItemByAmount( item, 1, csdefine.ITEM_REMOVE_BY_USE )
		argList = spaceStr.split()
		position  = KBEMath.Unreal2KBEnginePosition((float(argList[1]) , float(argList[2]) , float(argList[3])))
		direction = KBEMath.Unreal2KBEngineDirection((float(argList[4]), float(argList[5]), float(argList[6])))
		self.gotoSpace( argList[0], position, direction )

#--------------------------上古密阵接口----------------------------------
	def onEnterCampSGMZ( self ):
		self.addActivityDegree( csdefine.ACTIVITY_TYPE_CAMP_SGMZ )

	def onManMachineData( self, manMemberData, route ):
		spaceEntity = self.getCurrentSpace()
		if not spaceEntity:
			return
		spaceEntity.manMemberData = manMemberData
		spaceEntity.route = route

#---------------------------神秘福袋玩法---------------------------------------------
	def CELL_onUseItemTJP(self, exposed, uid, spaceStr):
		"""
		选择使用天机盘物品后
		"""
		if not self.validateClientCall( exposed ):
			return
		item = self.getItemInstByUid(int(uid))
		self.removeItemByAmount( item, 1, csdefine.ITEM_REMOVE_BY_USE )
		argList = spaceStr.split()
		position  = KBEMath.Unreal2KBEnginePosition((float(argList[1]) , float(argList[2]) , float(argList[3])))
		direction = KBEMath.Unreal2KBEngineDirection((float(argList[4]), float(argList[5]), float(argList[6])))
		self.gotoSpace( argList[0], position, direction )

#---------------------------烽火连天副本---------------------------------------------
	def telportFHLTActivity( self, key ):
		"""
		define method
		匹配成功
		"""
		spaceObj = KST.g_objFactory.getSpaceObject( Const.FHLT_SPACE_SCRIPTID )
		if spaceObj:
			pos, dir = spaceObj.getEnterInfoByCamp( self.camp )
			self.gotoSpaceUseArg( Const.FHLT_SPACE_SCRIPTID, pos, dir, {"spaceKey" : "FHLT_" + str(key)})
		else:
			KBEDebug.ERROR_MSG("Can not find space scriptID(%s)"%Const.FHLT_SPACE_SCRIPTID)

	def onLeaveActivityFHLTCopy( self, exposed ):
		"""
		Exposed method
		退出烽火连天副本
		"""
		if not self.validateClientCall( exposed ):
			return
		self.addBuff( self, Const.FHLT_PUNISH_BUFF )
		self.gotoExitSpacePos()

#---------------------------锦绣莲池玩法---------------------------------------------
	def CELL_onUseItemWSYC(self, exposed, uid, spaceStr):
		"""
		选择使用五色鱼叉物品回调
		"""
		if not self.validateClientCall( exposed ):
			return
		item = self.getItemInstByUid(int(uid))
		self.removeItemByAmount( item, 1, csdefine.ITEM_REMOVE_BY_USE )
		argList = spaceStr.split()
		position  = KBEMath.Unreal2KBEnginePosition((float(argList[1]) , float(argList[2]) , float(argList[3])))
		direction = KBEMath.Unreal2KBEngineDirection((float(argList[4]), float(argList[5]), float(argList[6])))
		self.gotoSpace( argList[0], position, direction )


#--------------------------阵营战场“勇闯绝命岛” ------------------------------------
	def onEnterCampYCJMD( self ):
		"""
		记录进阵营战场“勇闯绝命岛”
		"""
		self.addActivityDegree( csdefine.ACTIVITY_TYPE_CAMP_YCJMD )

#--------------------------阵营战场“勇闯绝命岛”（5人）------------------------------------
	def onEnterCampFiveYCJMD( self ):
		"""
		记录进阵营战场“勇闯绝命岛”（5人）
		"""
		self.addActivityDegree( csdefine.ACTIVITY_TYPE_CAMP_FIVE_YCJMD )
		
#--------------------------“勇闯绝命岛”（近战）------------------------------------
	def onEnterCampCopyYCJMD( self ):
		"""
		记录进“勇闯绝命岛”（近战）
		"""
		self.addActivityDegree( csdefine.ACTIVITY_TYPE_CAMP_COPY_YCJMD )
		
#--------------------------“勇闯绝命岛”（远程）------------------------------------
	def onEnterCampShootYCJMD( self ):
		"""
		记录进“勇闯绝命岛”（远程）
		"""
		self.addActivityDegree( csdefine.ACTIVITY_TYPE_CAMP_SHOOT_YCJMD )
		
#--------------------------攻城战------------------------------------
	def onEnterAttackCityWar( self ):
		"""
		记录进攻城战
		"""
		self.addActivityDegree( csdefine.ACTIVITY_TYPE_COPY_ACCTACK_CITY_WAR )

#-------------------------晶石狩猎场-----------------------------------------
	def onEnterCampJSSLC( self ):
		"""
		记录进晶石狩猎场
		"""
		self.addActivityDegree( csdefine.ACTIVITY_TYPE_CAMP_JSSLC )

#-----------------------至尊争霸------------------------------------------
	def onEnterZZZB( self ):
		"""
		记录进 至尊争霸
		"""
		self.addActivityDegree( csdefine.ACTIVITY_TYPE_CAMP_ZZZB )

#--------------------------灵脉战场 ------------------------------------
	def onEnterLMZC( self ):
		"""
		记录进阵营战场“勇闯绝命岛”
		"""
		self.addActivityDegree( csdefine.ACTIVITY_TYPE_CAMP_LING_MAI )

#----------------------------------------阵营战场随机匹配--------------------------------------------
	def campRandomFitJoin( self ):
		"""
		define method
		进入随机匹配排队
		"""
		self.isMatchCampRandomFit = True

	def campRandomFitQuit( self ):
		"""
		define method
		退出随机匹配排队
		"""
		self.isMatchCampRandomFit = False

	def isHasMatchCampRandomFit(self):
		"""
		是否在随机匹配排队
		"""
		return self.isMatchCampRandomFit


#----------------------------------------团队竞技战场随机匹配--------------------------------------------
	def battleActivitySignUp(self):
		"""
		define method
		进入随机匹配排队
		"""
		self.isMatchBattleActivity = True

	def battleActivitySignOut(self):
		"""
		define method
		退出随机匹配排队
		"""
		self.isMatchBattleActivity = False

	def isHasMatchBattleActivity(self):
		"""
		是否在随机匹配排队
		"""
		return self.isMatchBattleActivity

#-------------------------------------CST-9910 帮会争霸战 ------------------------------------------
	def setIsDeclarePointBHZB( self, isDeclarePointBHZB ):
		"""
		设置是否宣战据点
		"""
		self.isDeclarePointBHZB = isDeclarePointBHZB

	def getIsDeclarePointBHZB( self ):
		"""
		"""
		return self.isDeclarePointBHZB

	def declareBHZBPoint( self, srcEntityID, pointIndex, groupID ):
		"""
		exposed method
		宣战据点
		"""
		if not self.validateClientCall( srcEntityID ):
			return

		if not self.tongMB:
			return

		if self.tongTitle not in [csdefine.TONG_TITLE_1,csdefine.TONG_TITLE_3]:
			return

		self.tongMB.declareBHZBPoint( pointIndex,groupID,self.base )

		#KBEngine.globalData["BHZBManager"].declareBHZBPoint( self.tongDBID,self.camp,pointIndex,self.base,self.playerDBID,self.getName(),self.tongName )


	def cancelDeclareBHZBPoint( self, srcEntityID, pointIndex ):
		"""
		exposed method
		取消宣战
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		
		if not self.tongMB:
			return

		if self.tongTitle not in [csdefine.TONG_TITLE_1,csdefine.TONG_TITLE_3]:
			return

		self.tongMB.cancelDeclareBHZBPoint( pointIndex )

		#KBEngine.globalData["BHZBManager"].cancelDeclareBHZBPoint( self.tongMB,self.camp,pointIndex )

	def joinBHZBPointFight( self, srcEntityID, pointIndex, groupID ):
		"""
		exposed method
		参与据点争夺战斗
		"""
		if not self.validateClientCall( srcEntityID ):
			return

		if not self.tongMB:
			return

		if self.tongTitle not in [csdefine.TONG_TITLE_1,csdefine.TONG_TITLE_3]:
			return

		self.tongMB.joinBHZBPointFight( pointIndex, groupID, self.base )

		#KBEngine.globalData["BHZBManager"].joinBHZBPointFight( self.tongDBID, self.getCamp(),pointIndex,self.base,self.playerDBID )

	def cancelJoinBHZBPointFight( self, srcEntityID, pointIndex ):
		"""
		exposed method
		撤销回防
		"""
		if not self.validateClientCall( srcEntityID ):
			return

		if not self.tongMB:
			return

		if self.tongTitle not in [csdefine.TONG_TITLE_1,csdefine.TONG_TITLE_3]:
			return

		self.tongMB.cancelJoinBHZBPointFight( pointIndex )

	def requestGotoNPCExtPointWar( self, pointIndex, spaceScriptID ,occupyPlayerDBID, declareTongDBID,occupyTongDBID, pointType, npcName,npcEntity, declareTongName,declarePlayerDBID,declarePlayerName ):
		"""
		"""
		spaceObj = KST.g_objFactory.getSpaceObject( spaceScriptID )
		if not spaceObj:
			return
		self.gotoNPCExtPointWar( pointIndex, spaceScriptID ,occupyPlayerDBID, declareTongDBID,occupyTongDBID,pointType,npcName,declareTongName,declarePlayerDBID,declarePlayerName )

	def gotoNPCExtPointWar( self, pointIndex, spaceScriptID ,occupyPlayerDBID, declareTongDBID,occupyTongDBID, pointType,npcName,declareTongName,declarePlayerDBID,declarePlayerName ):
		"""
		进入据点争夺战
		"""
		spaceObj = KST.g_objFactory.getSpaceObject( spaceScriptID )
		if not spaceObj:
			return
		if self.tongDBID == declareTongDBID:
			enterInfo = spaceObj.getAttackEnterPosInfo()
		else:
			enterInfo = spaceObj.getProtectEnterPosInfo()
		packArgs = {}
		packArgs["pointIndex"] = pointIndex
		packArgs["pointType"] = pointType
		packArgs["belongDBID"] = occupyPlayerDBID
		packArgs["belongTongDBID"] = occupyTongDBID
		packArgs["declareTongDBID"] = declareTongDBID
		packArgs["npcName"] = npcName
		packArgs["declareTongName"] = declareTongName
		packArgs["declarePlayerDBID"] = declarePlayerDBID
		packArgs["declarePlayerName"] = declarePlayerName
		packArgs["camp"] = self.getCamp()
		self.gotoSpaceUseArg( spaceScriptID, enterInfo[0], enterInfo[1],packArgs)

	def requestGotoStandMapPoint( self, srcEntityID, position ):
		"""
		exposed method
		请求传送到沙盘某个据点附近
		"""
		if not self.validateClientCall( srcEntityID ):
			return

		packArgs = {}
		packArgs["spaceKey"] = str(self.tongDBID)
		packArgs["playerDBID"] = self.playerDBID
		packArgs["belongType"] = csdefine.SPACE_BELONG_NORMAL
		packArgs["groupID"] = -1
		spaceEntity = self.getCurrentSpace()
		if spaceEntity and spaceEntity.getScript().getSpaceChildType() == csdefine.SPACE_TYPE_CHILD_BHZB_HOME_BARRACKS:
			packArgs["groupID"] = spaceEntity.getMemberGroupIDByPlayerDBID( self )
		pos = KBEMath.Unreal2KBEnginePosition( position )
		KBEngine.globalData["BHZBManager"].enterBHZBStandMap( self.getCamp(), self.tongDBID,self.playerDBID,self.base,pos,self.direction,packArgs )

	def callTeamToProtect( self, srcEntityID, groupTeamID, pointIndex,pointName ):
		"""
		exposed method
		召唤某一个队去防守
		"""
		pass
		# if not self.validateClientCall( srcEntityID ):
		# 	return
		# if not self.tongMB:
		# 	return
		
		# spaceEntity = self.getCurrentSpace()
		# if not spaceEntity:
		# 	return
		# # 这里应该还需要判断下是否被同一只队伍防守
		# if spaceEntity.getScript().getSpaceChildType() != csdefine.SPACE_TYPE_CHILD_BHZB_HOME_BARRACKS:
		# 	return
		# if spaceEntity.isTeamToProtect( self.tongDBID, groupTeamID, pointIndex ):
		# 	return
		# spaceEntity.callTeamToProtect( self.tongDBID, groupTeamID, pointIndex,pointName )

	def callTeamToAttack( self, srcEntityID, groupTeamID, pointIndex,pointName ):
		"""
		exposed method
		召唤某一队去进攻
		"""
		pass
		# if not self.validateClientCall( srcEntityID ):
		# 	return
		# if not self.tongMB:
		# 	return
		
		# spaceEntity = self.getCurrentSpace()
		# if not spaceEntity:
		# 	return
		# if spaceEntity.getScript().getSpaceChildType() != csdefine.SPACE_TYPE_CHILD_BHZB_HOME_BARRACKS:
		# 	return
		# if spaceEntity.isTeamToAttack( self.tongDBID, groupTeamID, pointIndex ):
		# 	return

		# spaceEntity.callTeamToAttack( self.tongDBID, groupTeamID, pointIndex,pointName )

	def requestGotoBHZBHomeBarrack( self, srcEntityID, tongDBID ):
		"""
		exposed method
		请求传送到大本营
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		if self.tongDBID != int(tongDBID):
			return

		KBEngine.globalData["BHZBManager"].requestGotoBHZBHomeBarrack( self.getCamp(),self.base )

	def onEnterBHZBPointWar( self, spaceScriptID, pointDict ):
		"""
		进入帮会争霸据点争夺地图
		"""
		spaceObj = KST.g_objFactory.getSpaceObject( spaceScriptID )
		if not spaceObj:
			return
		declareTongDBID = pointDict.get("declareTongDBID")
		if self.tongDBID == declareTongDBID:
			enterInfo = spaceObj.getAttackEnterInfo()
			pointDict.update( {"belongSide":csdefine.BELONG_SIDE_ATTACK} )
		else:
			enterInfo = spaceObj.getProtectEnterInfo()
			pointDict.update( {"belongSide":csdefine.BELONG_SIDE_PROTECT} )

		self.gotoSpaceUseArg( spaceScriptID, enterInfo[0], enterInfo[1],pointDict)

	def requestPointDetails( self, srcEntityID, pointIndex ):
		"""
		请求帮会争霸某个据点详情
		"""
		if not self.validateClientCall( srcEntityID ):
			return

		KBEngine.globalData["BHZBManager"].requestPointDetails( self.getCamp(), pointIndex, self.base )

	def defenseBHZBPoint( self, srcEntityID, pointIndex, groupID ):
		"""
		布防帮会争霸据点
		"""
		if not self.validateClientCall( srcEntityID ):
			return

		if not self.tongMB:
			return

		if self.tongTitle not in [csdefine.TONG_TITLE_1,csdefine.TONG_TITLE_3]:
			return

		self.tongMB.defenseBHZBPoint( pointIndex, groupID, self.base )
		#KBEngine.globalData["BHZBManager"].defenseBHZBPoint( self.tongDBID, self.getCamp(), pointIndex, self.base, self.playerDBID )

	def requestOpenBHZBIntegralRank( self, srcEntityID ):
		"""
		请求打开帮会争霸积分排行
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		KBEngine.globalData["BHZBManager"].openBHZBIntegralRank( self.getCamp(), self.base )

	def requestOpenBHZBNpcPointMap( self, srcEntityID ):
		"""
		请求打开据点大地图
		"""
		if not self.validateClientCall( srcEntityID ):
			return

		KBEngine.globalData["BHZBManager"].requestOpenBHZBNpcPointMap( self.getCamp(),self.base )

	def statusLeaveBHZBSpace( self ):
		"""
		发送离开帮会争霸PVP据点消息
		"""
		self.inquireMessage( csstatus.LEAVE_BHZB_PVP_SPACE,[],"leaveBHZBSpace" )
		timeID = self.addTimerCallBack(self.getCurrentSpaceObject().getDieKickOutTim() ,"leaveBHZBSpace",(1,))
		self.setTemp( "leaveTimeID", timeID )

	def leaveBHZBSpace( self, reply ):
		"""
		离开帮会争霸PVPspace
		"""
		if reply:
			if self.isState( csdefine.ENTITY_STATE_DEAD ):
				self.reviveOnOrigin()
			self.gotoExitSpacePos()
			timeID = self.queryTemp("leaveTimeID",None)
			if timeID != None:
				self.popTimer( timeID )
				self.removeTemp("leaveTimeID")

#------------------------------------攻城战-------------------------------------
	def signUpGCZ( self, srcEntityID, number, npcID ):
		"""
		exposed method
		报名攻城战
		"""
		if not self.validateClientCall( srcEntityID ):
			return

		npcEntity = KBEngine.entities.get( npcID, None )
		if not npcEntity:
			return
		if self.getLevel() < npcEntity.getScript().getReqLevel():
			self.statusMessage( csstatus.GCZ_SIGN_UP_FORBID_LEVEL, npcEntity.getScript().getReqLevel() )
			return
		if self.getRoleBarracksSoldierAmount() < npcEntity.getScript().getReqSoldierNum():
			self.statusMessage( csstatus.GCZ_SIGN_UP_FORBID_SOLDIER_AMOUNT, npcEntity.getScript().getReqSoldierNum() )
			return

		maxJoinNum = npcEntity.getScript().getMaxJoinNumByNum(number)
		startTime = npcEntity.getScript().getGCZStartTimeByNum( number )
		KBEngine.globalData["GCZManager"].signUpGCZ( number, self.base, self.playerDBID, maxJoinNum,startTime )

	def matchGCZSuccess( self, spaceScriptID ):
		"""
		匹配攻城战成功
		"""
		self.inquireMessage( csstatus.GCZ_MATCH_SUCCESS_IS_TO_ENTER,[],"onMatchGCZSuccess", spaceScriptID )

	def onMatchGCZSuccess( self, reply, spaceScriptID ):
		"""
		是否进入攻城战
		"""
		if reply:
			self.onEnterGCZSpace( spaceScriptID )

	def onEnterGCZSpace( self, spaceScriptID ):
		"""
		进入攻城战space
		"""
		if not self.isInTeam():
			KBEDebug.ERROR_MSG(" Enter GCZ Space need team ")
			return
		self.gotoSpaceEnterPos( spaceScriptID,{} )


