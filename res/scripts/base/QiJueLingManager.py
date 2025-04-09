# -*- coding: utf-8 -*-

import random
import KBEDebug
import Math
import KBEngine
import csdefine
from CoreObject import MgrPersistentObject
from ObjectScript.ObjectScriptFactory import g_objFactory

SPACE_CLASS_NAME = ""

MATCH_STAGE_0	= 0		#准备阶段
MATCH_STAGE_1	= 1		#入场阶段
MATCH_STAGE_2 	= 2		#初赛
MATCH_STAGE_3	= 3		#半决赛
MATCH_STAGE_4	= 4		#决赛
MATCH_STAGE_5	= 5		#已经结束

class MemberItem:
	"""
	一个参赛玩家的数据
	"""
	def __init__( self, number, playerDBID, playerMB, playerName ):
		self.number = number		   		#玩家编号 根据上场比赛名次来
		self.playerDBID = playerDBID   		#玩家DBID
		self.playerMB = playerMB			#玩家MailBox
		self.playerName = playerName		#玩家名称
		self.isInSpace = False				#是否在副本内
		self.isKickOut = False				#是否被淘汰
		self.kickOutStage = MATCH_STAGE_0	#哪个阶段被淘汰
		self.enemyDBID = 0					#当前对阵的玩家DBID

class MatchItem:
	"""
	一个等级段的比赛
	"""
	def __init__( self, mgr, matchKey ):
		self.mgr = mgr
		self.joinDatas = {}
		self.matchKey = matchKey		#一个等级段比赛 如30-39级 key值为3
		self.stageType = MATCH_STAGE_0	#当前所处阶段
		self.isPrepare = False   		#是否在准备阶段

		self.spaceMB = None				#副本MailBox
		self.spaceObject = g_objFactory.getSpaceObject( SPACE_CLASS_NAME % self.matchKey ) 
		self.readyTimerID = 0
		self.stage1TimerID = 0
		self.stage2TimerID = 0
		self.stage3TimerID = 0
		self.endPrepareTimer = 0
		
		self.joinMemberList = {}

	def addJoinData( self, playerMB, playerDBID, playerName, score ):
		"""
		添加参与玩家数据
		"""
		if len( self.joinDatas ) == 0:
			self.readyTimerID = self.mgr.addTimer( 30.0, 0.0, 0 ) #准备开始

		self.joinDatas[ playerDBID ] = { "playerDBID": playerDBID, "playerMB": playerMB, "playerName": playerName, "score": score }

	def onTimer( self, tid, userArg ):
		"""
		"""
		if tid == self.readyTimerID:
			self.readyTimerID = 0
			self.startMatch()
		elif tid == self.stage1TimerID:
			self.stage1TimerID = 0
			self.startFirstStage()
		elif tid == self.stage2TimerID:
			self.stage2TimerID = 0
			self.startSecondStage()
		elif tid == self.stage3TimerID:
			self.stage3TimerID = 0
			self.startThirdStage()
		elif tid == self.endPrepareTimer:
			self.endPrepareTimer = 0
			self.onPrepareEnd()

	def startMatch( self ):
		"""
		比赛开始
		"""
		playerInfos = sorted( self.joinDatas.values(), key = lambda a:a["score"], reverse = True )[0:8] #8表示加入该比赛的最大人数
		for index, info in enumerate( playerInfos ):
			number = index + 1
			memberItem = MemberItem( number, info["playerDBID"], info["playerMB"], info["playerName"] )
			self.joinMemberList[number] = memberItem

		self.startEnterStage()

	def endMatch( self ):
		"""
		比赛结束
		"""
		if self.stageType == MATCH_STAGE_5:
			return
		self.stageType = MATCH_STAGE_5

	def startEnterStage( self ):
		"""
		入场
		"""
		self.stageType = MATCH_STAGE_1
		#传入副本对应的山峰
		posList = self.spaceObject.getPositionList()
		for memberItem in self.joinMemberList.values():
			if not memberItem.playerMB: continue

			platNumber = self.getPlayerPlatNumber( memberItem.number )
			if not platNumber:
				continue
			memberItem.playerMB.cell.gotoSpaceUseArg(SPACE_CLASS_NAME % self.matchKey,posList[platNumber - 1],Math.Vector3(0,0,0),{"spaceKey":str(self.matchKey)})

		self.stage1TimerID = self.mgr.addTimer(15.0,0.0,0) #给15秒钟传送

	def startFirstStage( self ):
		"""
		初赛开始
		"""
		KBEDebug.DEBUG_MSG( "QiJueLing start first stage." )
		for num1, num2 in [[1,5],[3,7],[4,8],[2,6]]:
			if num1 in self.joinMemberList and num2 in self.joinMemberList:
				self.joinMemberList[num1].enemyDBID = self.joinMemberList[num2].playerDBID
				self.joinMemberList[num2].enemyDBID = self.joinMemberList[num1].playerDBID
		self.isPrePare = True
		self.stageType = MATCH_STAGE_2
		if self.spaceMB:
			self.spaceMB.cell.startFirstStage()

		self.endPrepareTimer = self.mgr.addTimer( 30.0, 0, 0 )	#30秒准备时间

	def startSecondStage( self ):
		"""
		半决赛开始
		"""
		KBEDebug.DEBUG_MSG( "QiJueLing start Second stage." )
		for groupNums in [ [ 1, 3, 5, 7 ], [ 2, 4, 6, 8 ] ]:
			tempList = []
			for num in groupNums:
				if num in self.joinMemberList and not self.joinMemberList[num].isKickOut:
					tempList.append(num)
			
			if len( tempList ) == 2: #找出哪两个没有被淘汰的
				num1 = tempList[0]
				num2 = tempList[1]
				self.joinMemberList[ num1 ].enemyDBID = self.joinMemberList[ num2 ].playerDBID
				self.joinMemberList[ num2 ].enemyDBID = self.joinMemberList[ num1 ].playerDBID
		
		self.stageType = MATCH_STAGE_3
		self.isPrepare = True
		self.endPrepareTimer = self.mgr.addTimer( 30.0, 0.0, 0 )

	def startThirdStage( self ):
		"""
		决赛
		"""
		KBEDebug.DEBUG_MSG( "QiJueLing start third stage." )
		tempList = []
		for num in range( 1, 9 ):
			if num in self.joinMemberList and not self.joinMemberList[ num ].isKickOut:
				tempList.append( num )
		
		if len( tempList ) == 2:
			num1 = tempList[0]
			num2 = tempList[1]
			self.joinMemberList[ num1 ].enemyDBID = self.joinMemberList[ num2 ].playerDBID
			self.joinMemberList[ num2 ].enemyDBID = self.joinMemberList[ num1 ].playerDBID
		
		self.stageType = MATCH_STAGE_4
		self.isPrepare = True
		self.endPrepareTimer = self.mgr.addTimer( 30.0, 0.0, 0 )

	def onPrepareEnd( self ):
		"""
		准备结束
		"""
		self.isPrePare = False
		#淘汰不在副本内的玩家
		for memberItem in self.joinMemberList.values():
			if not memberItem.isInSpace and not memberItem.isKickOut:
				memberItem.isKickOut = True

		#让某些玩家直接胜出
		for memberItem in self.joinMemberList.values():
			if memberItem.isKickOut: continue
			if not memberItem.enemyDBID:
				if self.stageType != MATCH_STAGE_4:
					#发送晋级的信息
					pass
			else:
				enemyItem = self.getMemberItemByDBID( memberItem.enemyDBID )
				if enemyItem.isKickOut:
					if self.stageType != MATCH_STAGE_4:
						#晋级信息
						pass

		# 更新比赛进度
		if self.checkStageCompleted():
			#结束当前阶段
			self.endCurrentStage()
		else:
			#开始战斗
			self.spaceMB.cell.enterFightProcess(self.stageType)

	def endCurrentStage( self ):
		"""
		当前阶段结束
		"""
		if self.stageType == MATCH_STAGE_2:
			self.stage2TimerID = self.addTimer( 15.0,0.0,0 )	#15秒的飞行时间
		elif self.stageType == MATCH_STAGE_3:
			self.stage3TimerID = self.addTimer( 15.0, 0.0, 0 )  #15秒的飞行时间
		else:
			self.endMatch()

	def checkStageCompleted( self ):
		"""
		判断当前阶段是否完成：每个小组都决出胜负就算完成
		"""
		groups = []
		if self.stageType == MATCH_STAGE_2:
			groups = [[1,5],[3,7],[4,8],[2,6]]
		elif self.stageType == MATCH_STAGE_3:
			groups = [[1,3,5,7],[2,4,6,8]]
		elif self.stageType == MATCH_STAGE_4:
			groups = list(range( 1, 9 ))

		for numList in groups:
			amount = 0
			for num in numList:
				if num in self.joinMemberList and not self.joinMemberList[num].isKickOut:
					amount += 1
			if amount >= 2:	#amount是表示有几个没有被淘汰
				return False
		return True

	def onPlayerDie( self, playerDBID ):
		"""
		玩家死亡
		"""
		if self.stageType == MATCH_STAGE_5:		# 比赛已结束则不处理
			return
		
		memberItem = self.getMemberItemByDBID( playerDBID )
		if not memberItem:
			KBEDebug.ERROR_MSG("QiJueLing stageType %i has no this player(playerDBID = %i)"%(self.stageType,playerDBID))
			return
		if memberItem.isKickOut:
			KBEDebug.ERROR_MSG("QiJueLing stageType %i this player(playerDBID = %i) is out"%(self.stageType,playerDBID))
			return

		self.kickOutPlayer( playerDBID )
		#通知副本该轮比赛结束
		self.spaceMB.cell.onPlatFightOver( self.getPlayerPlatNumber(memberItem.number) )
		# 更新比赛进度
		if self.checkStageCompleted():
			self.endCurrentStage()

	def onSpaceCreate( self, spaceMB ):
		"""
		副本创建
		"""
		self.spaceMB = spaceMB

	def onPlayerTeleportReady( self, playerDBID ):
		"""
		define method
		玩家已经进入副本
		"""
		memberItem = self.getMemberItemByDBID( playerDBID )
		if not memberItem:
			KBEDebug.ERROR_MSG("QiJueLing onPlayerTeleportReady stageType %i has no this player(playerDBID = %i)"%(self.stageType,playerDBID))
			return
		memberItem.isInSpace = True
		if memberItem.isKickOut:
			#发送晋级失败
			pass

	def onPlayerLeaveSpace( self, playerDBID ):
		"""
		玩家离开副本
		"""
		memberItem = self.getMemItemFromDBID( playerDBID )
		if not memberItem:
			return
		memberItem.isInSpace = False
		
		if self.isPrepare or self.stageType in [ MATCH_STAGE_1, MATCH_STAGE_5 ]:	# 准备阶段和入场阶段离开不处理
			KBEDebug.ERROR_MSG("QiJueLing onPlayerLeaveSpace stageType %i isPrepare"%(self.stageType))
			return
		if memberItem.isKickOut:
			KBEDebug.ERROR_MSG("QiJueLing onPlayerLeaveSpace stageType %i player%i isKickOut "%(self.stageType,playerDBID))
			return
		#通知副本该轮比赛结束
		self.kickOutPlayer( playerDBID )
		# 更新比赛进度
		if self.checkStageCompleted():
			self.endCurrentStage()

	def kickOutPlayer( self, playerDBID ):
		"""
		淘汰某玩家
		"""
		memberItem = self.getMemberItemByDBID( playerDBID )
		memberItem.isKickOut = True
		memberItem.kickOutStage = self.stageType

		if not memberItem.enemyDBID:
			KBEDebug.ERROR_MSG("QiJueLing stageType %i this player(playerDBID = %i) has no enemy"%( self.stageType, playerDBID ))
			return
		enemyMemberItem = self.getMemberItemByDBID( memberItem.enemyDBID )
		if enemyMemberItem.isKickOut or not enemyMemberItem.mailbox or not enemyMemberItem.isInSpace: #对手淘汰或 掉线 或不在副本内不处理
			KBEDebug.DEBUG_MSG( "QiJueLing enemy player state wrong! dbid:%s, enemyDBID:%s, enemy state:( %s, %s, %s )." % \
					( memberItem.playerDBID, memberItem.enemyDBID, enemyMemberItem.mailbox is not None, enemyMemberItem.isKickOut, enemyMemberItem.isInSpace ) )
			return
		#加免战
		if self.stageType != MATCH_STAGE_4:
			#发送晋级的信息
			pass

	def getMemberItemByDBID( self, playerDBID ):
		"""
		根据DBID获取参赛者数据
		"""
		for memberItem in self.joinMemberList.values():
			if memberItem.playerDBID == playerDBID:
				return memberItem
		return None

	def getPlayerPlatNumber( self, number ):
		"""
		获得玩家对应山峰的编号
		"""
		if self.stageType in [MATCH_STAGE_1, MATCH_STAGE_2]:
			if number in [1,5]: return 1
			elif number in [3,7]: return 2
			elif number in [4,8]: return 3
			elif number in [2,6]: return 4
		elif self.stageType == MATCH_STAGE_3:
			if number in [1,3,5,7]: return 5
			elif number in [2,4,6,8]: return 6
		elif self.stageType == MATCH_STAGE_4:
			return 7
		return 0


class QiJueLingManager( MgrPersistentObject.MgrPersistentObject ):
	"""
	七绝岭管理器
	"""
	def  __init__( self ):
		"""
		"""
		MgrPersistentObject.MgrPersistentObject.__init__( self )
		self.warData = {}

	def onTimer( self, tid, userArg ):
		"""
		timer 回调
		"""
		for mItem in self.warData.values():
			mItem.onTimer( id, userArg )

	def addJoinData( self, matchKey, playerMB, playerDBID, playerName, score ):
		"""
		将上场夜战凤栖镇的比赛结果添加
		matchKey 等级段的key
		如 30-39级 key值为3
		"""
		if matchKey not in self.warData:
			self.warData[matchKey] = MatchItem( self, matchKey )
		self.warData[matchKey].addJoinData( playerMB, playerDBID, playerName, score )

	def getPlayerMatchItem( self, playerDBID ):
		"""
		根据玩家DBID获得玩家参与比赛MatchItem
		"""
		for matchItem in self.warData.values():
			if matchItem.getMemberItemByDBID(playerDBID):
				return matchItem
		return None

	def onPlayerDie( self, playerDBID ):
		"""
		玩家死亡
		"""
		matchItem = self.getPlayerMatchItem( playerDBID )
		if matchItem:
			matchItem.onPlayerDie( playerDBID )

	def onSpaceCreate( self, spaceKey, spaceMB ):
		"""
		define method
		副本创建
		"""
		if int(spaceKey) in self.warData:
			self.warData[int(spaceKey)].onSpaceCreate( spaceMB )

	def onPlayerTeleportReady( self, spaceKey, playerDBID ):
		"""
		define method
		玩家已经进入副本
		"""
		if int(spaceKey) in self.warData:
			self.warData[int(spaceKey)].onPlayerTeleportReady( playerDBID )

	def onPlayerLeaveSpace( self, spaceKey, playerDBID ):
		"""
		define method
		玩家退出副本
		"""
		if int(spaceKey) in self.warData:
			self.warData[int(spaceKey)].onPlayerLeaveSpace( playerDBID )