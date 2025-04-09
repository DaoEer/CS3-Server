# -*- coding: utf-8 -*-

import KBEDebug
import KBEngine
import csdefine
from CoreObject import MgrPersistentObject
from ObjectScript.ObjectScriptFactory import g_objFactory
import csstatus
from ConfigObject.Crond.CrondDatas import CrondDatas
g_CrondDatas = CrondDatas.instance()
import KST
import csconst
import Functions
import cschannel_msgs
import random
from ConfigObject.MailContentDataLoader import g_mailContentDataLoader

SHI_FANG_CHENG_JOIN_NUMBER = 50	#十方城参加的人数
SHI_FANG_CHENG_CLASS_NAME = "30:fu_ben_SFC|40:fu_ben_SFC_01|50:fu_ben_SFC_02"
FQZ_JOIN_NUMBER	= 30	#血斗凤栖镇的参加的人数
FQZ_CLASS_NAME = "30:fu_ben_YZFQ_02|40:fu_ben_YZFQ_03|50:fu_ben_YZFQ_04"
TIMER_OUT_ARG = 20

class PersonStarcraftMgr( MgrPersistentObject.MgrPersistentObject ):
	"""
	个人竞技至尊争霸管理类
	"""
	def __init__( self ) :
		MgrPersistentObject.MgrPersistentObject.__init__( self )
		self.register()
		self.SFCSignUpData = {}
		self.SFCClassNameDict = {}
		self.shiFangChengPassListDict = {}
		self.shiFangChengPassStage1Dict = {}
		self.shiFangChengPassStage2Dict = {}
		self.FQZClassNameDict = {}
		self.FQZMemberKickOutList = []
		self.shiFangChengClassNameDict()
		self.yeZhanFengQiClassNameDict()
		self.onCompleteInit()

	def register( self ):
		"""
		注册
		"""
		taskEvents = { "ShiFangCheng_Notice":"onShiFangChengActiveNotice",
						"ShiFangCheng_SignUpStart":"onShiFangChengActiveSignUpStart",
						"ShiFangCheng_SignUpEnd":"onShiFangChengActiveSignUpEnd",
						"ShiFangCheng_Start":"onShiFangChengActiveStart",
						"ShiFangCheng_End":"onShiFangChengActiveEnd",
						"YeZhanFengQi_Start_Notice":"onYeZhanFengQiStartNotice",
						"YeZhanFengQi_Start":"onYeZhanFengQiStart",
						"YeZhanFengQi_End":"onYeZhanFengQiEnd"
		 }
		for taskName, callbackName in taskEvents.items():
			for scriptID, cmd in g_CrondDatas.getCrondTaskCmds(taskName):
		 		KBEngine.globalData["CrondManager"].addScheme( scriptID, cmd, self, callbackName, -1,() )

	def onShiFangChengActiveNotice( self, cmd, *callbackArgs ):
		"""
		十方城 活动公告
		"""
		KST.g_baseAppEntity.globalWold( csstatus.ZHIZUNZHENBA_ACTIVITY_START,"" )

	def onShiFangChengActiveSignUpStart( self, cmd, *callbackArgs ):
		"""
		十方城 开始报名
		"""
		#KST.g_baseAppEntity.globalWold( csstatus.SHI_FANG_CHENG_ACTIVITY_SIGN_UP,"" )
		self.clearPersonStarcraftData()
		KBEngine.globalData["SFC_StateSignUp"] = 1

	def onShiFangChengActiveSignUpEnd( self, cmd, *callbackArgs ):
		"""
		十方城 结束报名
		"""
		KBEngine.globalData["SFC_StateSignUp"] = 0

	def onShiFangChengActiveStart( self, cmd, *callbackArgs ):
		"""
		十方城 活动开始
		"""
		#KST.g_baseAppEntity.globalWold( csstatus.SHI_FANG_CHENG_ACTIVITY_START,"" )
		KBEngine.globalData["SFC_StateStart"] = 1
		self.statusMsgShiFangChengJoin()
		self.notifyShiFangChengStart()

	def onShiFangChengActiveEnd( self, cmd, *callbackArgs ):
		"""
		十方城 活动结束
		"""
		KBEngine.globalData["SFC_StateStart"] = 0
		for spaceClassName in self.SFCClassNameDict.values(): #通知所有十方城活动副本，活动结束
			KBEngine.globalData["SpaceManager"].remoteCallDomain(  spaceClassName, "activityEnd", [])

	def onYeZhanFengQiStartNotice( self, cmd, *callbackArgs ):
		"""
		血斗凤栖镇 活动开始通知
		"""
		KST.g_baseAppEntity.globalWold( csstatus.YE_ZHAN_FENG_START_NOTICE,"" )

	def onYeZhanFengQiStart( self, cmd, *callbackArgs ):
		"""
		血斗凤栖镇 活动开始
		"""
		#KST.g_baseAppEntity.globalWold( csstatus.YE_ZHAN_FENG_START,"" )
		KBEngine.globalData["YZFQ_StateStart"] = 1
		self.addTimer(32.0, 0, TIMER_OUT_ARG )
		self.statusMsgYeZhanFengQiJoin()

	def onYeZhanFengQiEnd( self, cmd, *callbackArgs ):
		"""
		血斗凤栖镇 活动结束
		"""
		KBEngine.globalData["YZFQ_StateStart"] = 0
		for spaceClassName in self.FQZClassNameDict.values():
			KBEngine.globalData["SpaceManager"].remoteCallDomain( spaceClassName,"activityEnd",[] )

	def clearPersonStarcraftData( self ):
		"""
		清除个人竞技至尊争霸的数据
		"""	
		self.SFCSignUpData = {}
		self.shiFangChengPassListDict = {}
		self.shiFangChengPassStage1Dict = {}
		self.shiFangChengPassStage2Dict = {}
		self.FQZMemberKickOutList = []
		self.FQZMemberListDict = {}

	def shiFangChengClassNameDict( self ):
		"""
		十方城 等级对应space文件
		"""
		spaceClassNameList = SHI_FANG_CHENG_CLASS_NAME.split("|")
		for item in spaceClassNameList:
			itemList = item.split(":")
			self.SFCClassNameDict[ int(int(itemList[0]) / 10) ] = itemList[1]

	def yeZhanFengQiClassNameDict( self ):
		"""
		血斗凤栖镇 等级对应space文件
		"""
		spaceClassNameList = FQZ_CLASS_NAME.split("|")
		for item in spaceClassNameList:
			itemList = item.split(":")
			self.FQZClassNameDict[ int(int(itemList[0]) / 10) ] = itemList[1]

	def requestPrepareSpace( self, activityKey, playerDBID ):
		"""
		请求预创建副本
		"""
		spaceParams = {}
		spaceClassName = self.SFCClassNameDict[ activityKey ]
		spaceParams[ "spaceKey" ] = str(playerDBID)
		spaceParams["belongType"] = csdefine.SPACE_BELONG_PERSON
		KBEngine.globalData["SpaceManager"].remoteCallDomain(  spaceClassName, "createSpaceItem", (spaceParams,) )

	def shiFangChengSignUp( self, activityKey, playerMB, playerDBID, playerName ):
		"""
		十方城报名
		"""
		if not KBEngine.globalData.get("SFC_StateSignUp",0):
			playerMB.statusMessage( csstatus.ZHIZUNZHENBA_NOT_SIGN_UP_START,"" )
			return
		if activityKey not in self.SFCClassNameDict:
			playerMB.statusMessage(csstatus.ZHIZUNZHENBA_LIMIT_LEVEL,"")
			return
		if activityKey not in self.SFCSignUpData:
			self.SFCSignUpData[activityKey] = {}
		if len( self.SFCSignUpData[activityKey] ) >= SHI_FANG_CHENG_JOIN_NUMBER:
			playerMB.statusMessage( csstatus.ZHIZUNZHENBA_SIGN_UP_LIMIT_NUMBER,"" )
			return
		if playerDBID in self.SFCSignUpData[activityKey]:	#已报名
			playerMB.statusMessage( csstatus.SHI_FANG_CHENG_SIGN_UP_AREADY,"" )
		else:
			self.SFCSignUpData[activityKey][playerDBID] = playerName
			self.requestPrepareSpace( activityKey, playerDBID )
			playerMB.statusMessage( csstatus.SHI_FANG_CHENG_SIGN_UP_SUCCESS,"" )

	def notifyShiFangChengStart( self ):
		"""
		通知十方城活动开始
		"""
		spaceClassName = list(self.SFCClassNameDict.values())[0]
		spaceObj = KST.g_objFactory.getSpaceObject( spaceClassName )
		index = 0
		if spaceObj: 
			index = random.randint( 0,len(spaceObj.getStageListStr()) -1 )
		for spaceClassName in self.SFCClassNameDict.values(): #通知所有十方城活动副本，活动开始
			KBEngine.globalData["SpaceManager"].remoteCallDomain(  spaceClassName, "activityStart", (index,) )

	def statusMsgShiFangChengJoin( self ):
		"""
		"""
		for activityKey, data in self.SFCSignUpData.items():
			for playerDBID, playerName in data.items():
				KBEngine.lookUpEntityByDBID( "Role", playerDBID, Functions.Functor( self.statusMsgJoinShiFangChengCallBack, activityKey ) )

	def statusMsgJoinShiFangChengCallBack( self, activityKey,target ):
		"""
		发送消息
		"""
		if target is False:
			return
		if target is True:
			return
		target.cell.shiFangChengJoinNotice(activityKey)

	def statusMsgYeZhanFengQiJoin( self ):
		"""
		"""
		for spaceName, playerDBIDs in self.FQZMemberListDict.items():
			for playerDBID in playerDBIDs:
				KBEngine.lookUpEntityByDBID( "Role", playerDBID, Functions.Functor( self.statusMsgYeZhanFengQiJoinCallBack) )

	def statusMsgYeZhanFengQiJoinCallBack( self, target ):
		"""
		"""
		if target is False:
			return
		if target is True:
			return

		target.cell.yeZhanFengQiJoinNotice()

	def gotoShiFangCheng( self, playerMB,activityKey, playerDBID ):
		"""
		进入十方城
		"""
		if not KBEngine.globalData.get("SFC_StateStart",0):
			return
		if not self.SFCSignUpData.get(activityKey,None):
			playerMB.statusMessage( csstatus.SHI_FANG_CHENG_NOT_SIGN_UP,"" )
			return
		if not self.SFCSignUpData[activityKey].get(playerDBID,None):
			playerMB.statusMessage( csstatus.SHI_FANG_CHENG_NOT_SIGN_UP,"" )
			return
		playerMB.cell.gotoSpaceEnterPos( self.SFCClassNameDict[activityKey],{} )

	def abandonShiFangeCheng( self, activityKey, playerDBID ):
		"""
		放弃十方城
		"""
		if activityKey in self.SFCSignUpData:
			if playerDBID in self.SFCSignUpData[activityKey]:
				self.SFCSignUpData[activityKey].pop(playerDBID)

	def addYeZhanFengQiMember( self, spaceClassName,playerMB, playerName,playerDBID, passTime ):
		"""
		增加血斗凤栖镇成员
		"""
		activityKey = 0
		for sfcActivityKey, sfcSpaceClassName in self.SFCClassNameDict.items():
			if sfcSpaceClassName == spaceClassName:
				activityKey = sfcActivityKey
				break

		if spaceClassName not in self.shiFangChengPassListDict:
			self.shiFangChengPassListDict[spaceClassName] = []
		self.shiFangChengPassListDict[spaceClassName].append( ( playerName, passTime ) )

		shiFangChengPassList = self.shiFangChengPassListDict[spaceClassName]
		minutes = int(passTime/60)
		second = int(passTime%60)
		time = "%i%s%i%s"%(minutes, cschannel_msgs.MINUTE, second, cschannel_msgs.SECOND)
		playerMB.client.statusMessage(csstatus.SHI_FANG_CHENG_SPACE_SUCCESS, str(time) + "|" +  self.getChineseNumberByNumber( len( shiFangChengPassList ) ))
		msgID = 0
		if len( shiFangChengPassList ) == 1:
			msgID = csstatus.SHI_FANG_CHENG_SPACE_SUCCESS_FIRST
		elif len( shiFangChengPassList ) == 2:
			msgID = csstatus.SHI_FANG_CHENG_SPACE_SUCCESS_SECOND
		elif len( shiFangChengPassList ) == 3:
			msgID = csstatus.SHI_FANG_CHENG_SPACE_SUCCESS_THREE
		elif len( shiFangChengPassList ) %5 == 0:
			msgID = csstatus.SHI_FANG_CHENG_SPACE_SUCCESS_BEHIND_THREE
		if msgID != 0:
			self.statusPassMessageToJoinPlayer( msgID, playerName, spaceClassName )
		self.showList( spaceClassName,activityKey,playerMB )

		fqzSpaceClassName = self.FQZClassNameDict[activityKey]
		if fqzSpaceClassName not in self.FQZMemberListDict:
			self.FQZMemberListDict[fqzSpaceClassName] = []
		if len( self.FQZMemberListDict[fqzSpaceClassName] ) < FQZ_JOIN_NUMBER:
			self.FQZMemberListDict[fqzSpaceClassName].append(playerDBID)
			playerMB.client.statusMessage(csstatus.GET_JOIN_YE_ZHAN_FENG_QI,"")
		else:
			playerMB.client.statusMessage( csstatus.LOSE_JOIN_YE_ZHAN_FENG_QI,"" )

	def showList( self, spaceClassName,activityKey,passEntityMB ):
		"""
		显示排行榜
		"""
		passDataList = []
		for playerName, passTime in self.shiFangChengPassListDict[spaceClassName]:
			tempDict = {}
			tempDict["playerName"] = playerName
			tempDict["passTime"] = passTime
			passDataList.append(tempDict)

		passEntityMB.client.CLIENT_ShowShiFangChengPassList(len(self.SFCSignUpData[activityKey]), Functions.toJsonString(passDataList))

	def statusPassMessageToJoinPlayer( self, msgID, playerName, spaceClassName ):
		"""
		发送通关消息
		"""
		for activityKey, data in self.SFCSignUpData.items():
			for joinPlayerDBID, joinPlayerName in data.items():
				KBEngine.lookUpEntityByDBID( "Role", joinPlayerDBID, Functions.Functor( self.onStatusPassMessageToJoinPlayer, msgID,playerName,spaceClassName) )

	def onStatusPassMessageToJoinPlayer( self,msgID, playerName, spaceClassName,target ):
		"""
		"""
		if target is False:
			return
		if target is True:
			return
		target.statusMessage( msgID, playerName )
		if len(self.shiFangChengPassListDict[spaceClassName]) == 1:
			if hasattr(target,"client") and target.client:
				target.client.CLIENT_ShowFirstPassShiFangCheng( self.shiFangChengPassListDict[spaceClassName][0][0],self.shiFangChengPassListDict[spaceClassName][0][1] )
		else:
			if hasattr(target,"client") and target.client:
				target.client.CLIENT_ShowPassShiFangChengNumber( len(self.shiFangChengPassListDict[spaceClassName]) )
		
	def getChineseNumberByNumber( self, number ):
		"""
		"""
		if number <= 9:
			return cschannel_msgs.ChineseNumber[number]
		else:
			return cschannel_msgs.ChineseNumber[0] + cschannel_msgs.ChineseNumber[number%10]

	def completeShiFangChengStage( self, spaceClassName,playerMB, playerDBID,playerName,completeStage, useTime ):
		"""
		完成某个活动的某阶段
		"""
		if spaceClassName not in self.shiFangChengPassStage1Dict:
			self.shiFangChengPassStage1Dict[spaceClassName] = []
		if spaceClassName not in self.shiFangChengPassStage2Dict:
			self.shiFangChengPassStage2Dict[spaceClassName] = []
		minutes = int(useTime/60)
		second = int(useTime%60)
		time = "%i%s%i%s"%(minutes, cschannel_msgs.MINUTE, second, cschannel_msgs.SECOND)
		if completeStage == 1:
			self.shiFangChengPassStage1Dict[spaceClassName].append( playerDBID )
			playerMB.client.statusMessage( csstatus.SHI_FANG_CHENG_COMPLETESTAGE, self.getChineseNumberByNumber( completeStage ) + "|" + str(time)+ "|" + self.getChineseNumberByNumber( (self.shiFangChengPassStage1Dict[spaceClassName].index(playerDBID) + 1)) + "|" +self.getChineseNumberByNumber( completeStage ))
			rankIndex = self.shiFangChengPassStage1Dict[spaceClassName].index(playerDBID)
			if len(self.shiFangChengPassStage2Dict[spaceClassName]) <= 0:
				if rankIndex == 1 or rankIndex == 2 or rankIndex == 3 or rankIndex%5 == 0:
					self.statusStageMessageToJoinPlayer(playerDBID,rankIndex,playerName,completeStage,spaceClassName)
		elif completeStage == 2:
			self.shiFangChengPassStage2Dict[spaceClassName].append( playerDBID )
			playerMB.client.statusMessage( csstatus.SHI_FANG_CHENG_COMPLETESTAGE,self.getChineseNumberByNumber( completeStage ) + "|" + str(time)+ "|" + self.getChineseNumberByNumber( (self.shiFangChengPassStage2Dict[spaceClassName].index(playerDBID) + 1) ) + "|" +self.getChineseNumberByNumber( completeStage ))
			rankIndex = self.shiFangChengPassStage2Dict[spaceClassName].index(playerDBID)
			if rankIndex == 1 or rankIndex == 2 or rankIndex == 3 or rankIndex%5 == 0:
				self.statusStageMessageToJoinPlayer(playerDBID,rankIndex,playerName,completeStage,spaceClassName)

	def statusStageMessageToJoinPlayer( self, playerDBID,rankIndex,playerName,completeStage,spaceClassName ):
		"""
		发送完成某阶段的提示
		"""
		msgID = 0
		if rankIndex == 1:
			msgID = csstatus.SHI_FANG_CHENG_COMPLETESTAGE_FIRST
		elif rankIndex == 2:
			msgID = csstatus.SHI_FANG_CHENG_COMPLETESTAGE_SECOND
		elif rankIndex == 3:
			msgID = csstatus.SHI_FANG_CHENG_COMPLETESTAGE_THREE
		elif rankIndex %5 ==0:
			msgID = csstatus.SHI_FANG_CHENG_COMPLETESTAGE_BEHIND_THREE
		for activityKey, data in self.SFCSignUpData.items():
			for joinPlayerDBID, playername in data.items():
				if joinPlayerDBID != playerDBID:
					KBEngine.lookUpEntityByDBID( "Role", joinPlayerDBID, Functions.Functor( self.onStatusStageMessageToJoinPlayer, msgID,playerName,completeStage,spaceClassName) )

	def onStatusStageMessageToJoinPlayer( self, msgID, playerName, completeStage,spaceClassName,target ):
		"""
		"""
		if target is False:
			return
		if target is True:
			return
		if msgID == csstatus.SHI_FANG_CHENG_COMPLETESTAGE_BEHIND_THREE:
			if completeStage == 1:
				target.client.statusMessage( msgID,self.getChineseNumberByNumber( len(self.shiFangChengPassStage1Dict[spaceClassName]) )+"|"+self.getChineseNumberByNumber( completeStage ) )
			elif completeStage == 2:
				target.client.statusMessage( msgID,self.getChineseNumberByNumber( len(self.shiFangChengPassStage2Dict[spaceClassName]) )+"|"+self.getChineseNumberByNumber( completeStage ) )
			return
		target.statusMessage( msgID, playerName+"|"+self.getChineseNumberByNumber( completeStage )  )

	def gotoYeZhanFengQi( self, playerMB, activityKey, playerDBID ):
		"""
		进入血斗凤栖镇
		"""
		if not KBEngine.globalData.get("YZFQ_StateStart",0):
			return
		# 为了配合策划测试  暂时注释掉
		spaceClassName = self.FQZClassNameDict[activityKey]
		if spaceClassName not in self.FQZMemberListDict or playerDBID not in self.FQZMemberListDict[spaceClassName]:
			playerMB.statusMessage( csstatus.YE_ZHAN_FENG_QI_CAN_NOT_JOIN,"" )
			return
		if playerDBID in self.FQZMemberKickOutList:
			return
		spaceObject = g_objFactory.getSpaceObject( spaceClassName )
		enterPos,enterDir = spaceObject.getEnterInfo()
		playerMB.cell.gotoSpaceUseArg( spaceClassName, enterPos, enterDir, {} )

	def yeZhanFengQiKickOutMember( self, playerDBID ):
		"""
		血斗凤栖镇 玩家淘汰
		"""
		self.FQZMemberKickOutList.append(playerDBID)
		
	def sendWoldMsg( self, messageType, messageArg ):
		"""
		发送世界公告消息
		"""
		KST.g_baseAppEntity.globalWold( messageType, messageArg )

	def onTimer( self, id, userArg ):
		"""
		"""
		if userArg == TIMER_OUT_ARG:
			KBEngine.globalData["YZFQ_StateStart"] = 0

	def showPassShiFangChengByLogin( self, spaceClassName, playerMB ):
		"""
		显示通关十方城界面
		"""
		if spaceClassName not in self.shiFangChengPassListDict:
			return
		if len(self.shiFangChengPassListDict[spaceClassName]) <= 0:
			return
		if len(self.shiFangChengPassListDict[spaceClassName]) == 1:
			if hasattr(playerMB,"client") and playerMB.client:
				playerMB.client.CLIENT_ShowFirstPassShiFangCheng( self.shiFangChengPassListDict[spaceClassName][0][0],self.shiFangChengPassListDict[spaceClassName][0][1] )
		else:
			if hasattr(playerMB,"client") and playerMB.client:
				playerMB.client.CLIENT_ShowPassShiFangChengNumber( len(self.shiFangChengPassListDict[spaceClassName]) )

