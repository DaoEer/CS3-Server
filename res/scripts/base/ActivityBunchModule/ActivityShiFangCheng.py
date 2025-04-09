# -*- coding: utf-8 -*-


from ActivityBunchModule.ActivityBase import ActivityBase

import csstatus
from ActivityBunchModule import ABDefine
import csdefine
import Functions
import csconst
import KBEDebug
import KBEngine
import KST
import cschannel_msgs
import random
from Functions import Functor

class ActivityShiFangCheng( ActivityBase ):
	"""
	十方城
	"""
	def __init__( self, actBunch, bunchName, section ):
		ActivityBase.__init__( self, actBunch, bunchName, section )
		self._joinInfos = {}
		self._passList = []
		self._passStage1 = []
		self._passStage2 = []
		
	def onSignUp( self ):
		"""
		开始报名
		"""
		ActivityBase.onSignUp( self )
		KST.g_baseAppEntity.globalWold( csstatus.SHI_FANG_CHENG_ACTIVITY_SIGN_UP,"" )
		self._joinInfos = {}
	
	def onSignUpEnd( self ):
		"""
		报名结束
		"""
		ActivityBase.onSignUpEnd(self)
	
	def onStart( self ):
		"""
		开始活动
		"""
		ActivityBase.onStart(self)
		self.statusMsgJoin()
		KST.g_baseAppEntity.globalWold( csstatus.SHI_FANG_CHENG_ACTIVITY_START,"" )
		spaceClassName = list(self._joinScript.getAllSpace())[0]
		spaceObj = KST.g_objFactory.getSpaceObject( spaceClassName )
		index = 0
		if spaceObj: 
			index = random.randint( 0,len(spaceObj.getStageListStr()) -1 )
		for spaceClassName in self._joinScript.getAllSpace(): #通知所有活动副本，活动开始
			KBEngine.globalData["SpaceManager"].remoteCallDomain(  spaceClassName, "activityStart", (index,) )

	def statusMsgJoin( self ):
		"""
		"""
		for activityKey, data in self._joinInfos.items():
			for playerDBID, playerName in data.items():
				KBEngine.lookUpEntityByDBID( "Role", playerDBID, Functor( self.statusMsgJoinCallBack, self._bunchName, self._activityName, activityKey ) )

	def statusMsgJoinCallBack( self, bunchName, actName, activityKey,target ):
		"""
		发送消息
		"""
		if target is False:
			return
		if target is True:
			return
		target.cell.actBunch_joinNotarize( bunchName,actName,activityKey )
	
	def onEnd( self ):
		"""
		活动结束
		"""
		ActivityBase.onEnd( self )
		self._joinInfos = {}
		self._passList = []
		self._passStage1 = []
		self._passStage2 = []

		for spaceClassName in self._joinScript.getAllSpace(): #通知所有活动副本，活动开始
			KBEngine.globalData["SpaceManager"].remoteCallDomain(  spaceClassName, "activityEnd", () )

	def addjoinner( self, actMgr, joinEntityMB, params ):
		"""
		添加本轮活动的参考者
		"""
		activityKey = params.get("activityKey",None)
		playerDBID = params.get("playerDBID",0)
		playerName = params.get("playerName","")
		if not self._joinInfos.get(activityKey,None):
			self._joinInfos[activityKey] = {}
		self._joinInfos[ activityKey ][ playerDBID ] = playerName
		self._joinScript.requestPrepareSpace( joinEntityMB, params )

	def abandon( self, actMgr, abandonEntityMB, activityKey, playerDBID ):
		"""
		放弃活动
		"""
		if activityKey in self._joinInfos:
			if playerDBID in self._joinInfos[activityKey]:
				self._joinInfos[activityKey].pop(playerDBID)

	def join( self, actMgr, joinEntityMB, params ):
		"""
		参加十方城活动
		"""
		if self.getCurrentState() != ABDefine.ACTIVITY_STATE_START:
			return

		activityKey = params.get("activityKey",None)
		playerDBID = params.get("playerDBID",0)
		if not self._joinInfos.get(activityKey,None):
			KBEDebug.ERROR_MSG("ActivityShiFangCheng has no this activityKey%s"%activityKey)
			return
		if not self._joinInfos[activityKey].get(playerDBID,None):
			joinEntityMB.statusMessage( csstatus.SHI_FANG_CHENG_NOT_SIGN_UP,"" )
			return

		self._joinScript.join( actMgr, joinEntityMB, params )

	def joinNext( self, mgr, joinEntityMB, params ):
		#参与下轮
		ActivityBase.joinNext( self, mgr, joinEntityMB, params )
		passTime = str(params[ "passTime" ])
		playerName = params[ "playerName" ]
		self._passList.append( ( playerName, passTime ) )
		minutes = int(params[ "passTime" ]/60)
		second = int(params[ "passTime" ]%60)
		time = "%i%s%i%s"%(minutes, cschannel_msgs.MINUTE, second, cschannel_msgs.SECOND)
		joinEntityMB.client.statusMessage(csstatus.SHI_FANG_CHENG_SPACE_SUCCESS, str(time) + "|" +  self.getChineseNumberByNumber( len( self._passList ) ))
		msgID = 0
		if len( self._passList ) == 1:
			msgID = csstatus.SHI_FANG_CHENG_SPACE_SUCCESS_FIRST
		elif len( self._passList ) == 2:
			msgID = csstatus.SHI_FANG_CHENG_SPACE_SUCCESS_SECOND
		elif len( self._passList ) == 3:
			msgID = csstatus.SHI_FANG_CHENG_SPACE_SUCCESS_THREE
		elif len( self._passList ) %5 == 0:
			msgID = csstatus.SHI_FANG_CHENG_SPACE_SUCCESS_BEHIND_THREE
		if msgID != 0:
			self.statusPassMessageToJoinPlayer( msgID, playerName )
		self.showList( joinEntityMB )

	def showList( self, passEntityMB ):
		"""
		显示排行榜
		"""
		passDataList = []
		for playerName, passTime in self._passList:
			tempDict = {}
			tempDict["playerName"] = playerName
			tempDict["passTime"] = passTime
			passDataList.append(tempDict)

		passEntityMB.client.CLIENT_ShowShiFangChengPassList(len(self._joinInfos), Functions.toJsonString(passDataList))

	def onCompleteActivityStage( self, joinEntityMB, playerDBID,playerName,completeStage, useTime ):
		"""
		完成某个活动的某阶段
		"""
		minutes = int(useTime/60)
		second = int(useTime%60)
		time = "%i%s%i%s"%(minutes, cschannel_msgs.MINUTE, second, cschannel_msgs.SECOND)
		if completeStage == 1:
			self._passStage1.append( playerDBID )
			joinEntityMB.client.statusMessage( csstatus.SHI_FANG_CHENG_COMPLETESTAGE, self.getChineseNumberByNumber( completeStage ) + "|" + str(time)+ "|" + self.getChineseNumberByNumber( (self._passStage1.index(playerDBID) + 1)) + "|" +self.getChineseNumberByNumber( completeStage ))
			rankIndex = self._passStage1.index(playerDBID)
			if len(self._passStage2) <= 0:
				if rankIndex == 1 or rankIndex == 2 or rankIndex == 3 or rankIndex%5 == 0:
					self.statusStageMessageToJoinPlayer(playerDBID,rankIndex,playerName,completeStage)
		elif completeStage == 2:
			self._passStage2.append( playerDBID )
			joinEntityMB.client.statusMessage( csstatus.SHI_FANG_CHENG_COMPLETESTAGE,self.getChineseNumberByNumber( completeStage ) + "|" + str(time)+ "|" + self.getChineseNumberByNumber( (self._passStage2.index(playerDBID) + 1) ) + "|" +self.getChineseNumberByNumber( completeStage ))
			rankIndex = self._passStage2.index(playerDBID)
			if rankIndex == 1 or rankIndex == 2 or rankIndex == 3 or rankIndex%5 == 0:
				self.statusStageMessageToJoinPlayer(playerDBID,rankIndex,playerName,completeStage)

	def statusStageMessageToJoinPlayer( self, playerDBID,rankIndex,playerName,completeStage ):
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
		for activityKey, data in self._joinInfos.items():
			for joinPlayerDBID, playerName in data.items():
				if joinPlayerDBID != playerDBID:
					KBEngine.lookUpEntityByDBID( "Role", joinPlayerDBID, Functions.Functor( self.onStatusStageMessageToJoinPlayer, msgID,playerName,completeStage) )

	def onStatusStageMessageToJoinPlayer( self, msgID, playerName, completeStage,target ):
		"""
		"""
		if target is False:
			return
		if target is True:
			return
		if msgID == csstatus.SHI_FANG_CHENG_COMPLETESTAGE_BEHIND_THREE:
			if completeStage == 1:
				target.client.statusMessage( msgID,self.getChineseNumberByNumber( len(self._passStage1) )+"|"+self.getChineseNumberByNumber( completeStage ) )
			elif completeStage == 2:
				target.client.statusMessage( msgID,self.getChineseNumberByNumber( len(self._passStage2) )+"|"+self.getChineseNumberByNumber( completeStage ) )
			return
		target.statusMessage( msgID, playerName+"|"+self.getChineseNumberByNumber( completeStage )  )

	def statusPassMessageToJoinPlayer( self, msgID, playerName  ):
		"""
		发送通关消息
		"""
		for activityKey, data in self._joinInfos.items():
			for joinPlayerDBID, joinPlayerName in data.items():
				if playerName != joinPlayerName:
					KBEngine.lookUpEntityByDBID( "Role", joinPlayerDBID, Functions.Functor( self.onStatusPassMessageToJoinPlayer, msgID,playerName) )

	def onStatusPassMessageToJoinPlayer( self,msgID, playerName ,target ):
		"""
		"""
		if target is False:
			return
		if target is True:
			return

		target.statusMessage( msgID, playerName )

	def getChineseNumberByNumber( self, number ):
		"""
		"""
		if number <= 9:
			return cschannel_msgs.ChineseNumber[number]
		else:
			return cschannel_msgs.ChineseNumber[0] + cschannel_msgs.ChineseNumber[number%10]
