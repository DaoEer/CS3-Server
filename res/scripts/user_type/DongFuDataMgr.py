# -*- coding: utf-8 -*-

import KBEDebug
import KBEngine
import csstatus
import csdefine
import Math
import math
import time
import Const
import csconst
import ItemFactory
import Functions
import cschannel_msgs
import LogDefine
from MsgLogger import g_logger

class ClientDongFuData():
	"""客户端洞府数据"""
	def __init__( self ):
		self.challengeState = csdefine.CHANLLENGE_TYPE_NONE
		
	@classmethod
	def getDictFromObj( self, obj ):
		dict = {
			"dongFuType"	: obj.dongFuType,
			"challengeState": obj.getChallengeState(),
			"playerName" 	: obj.playerName,
			"level"			: obj.buildLevels[csdefine.LHMJ_BUIILD_LING_QUAN],
			"group" 		: obj.group,
			"batteleID" 	: obj.batteleID,
			}
		return dict
		
	def getChallengeState( self ):
		"""获取挑战状态"""
		isPlunderActive = KBEngine.globalData.get("LHMJ_PlunderActiveReady")
		isChallengeActive = KBEngine.globalData.get("LHMJ_ChallengeActiveReady")
		
		if isPlunderActive or isChallengeActive:
			if isPlunderActive:							# 掠夺战
				for buildType in csconst.DF_PLUNDER_BUILDS:
					if buildType in self.destroyBuild:
						return csdefine.CHANLLENGE_TYPE_REPAIR
			elif isChallengeActive:							# 争夺战
				if csdefine.LHMJ_BUIILD_LING_QUAN in self.destroyBuild:
					return csdefine.CHANLLENGE_TYPE_REPAIR
			if self.challengePlayerDBID:
				if self.hasChallenge():
					return csdefine.CHANLLENGE_TYPE_ACCEPT
				return csdefine.CHANLLENGE_TYPE_CANNOT
			if self.challengeOtherDBID:
				return csdefine.CHANLLENGE_TYPE_CANNOT
			if self.playerDBID:
				return csdefine.CHANLLENGE_TYPE_COMMON
			
		return csdefine.CHANLLENGE_TYPE_NONE
		
	@classmethod
	def createObjFromDict( self, dict ):
		obj = self.__class__()
		return obj
		
	@classmethod
	def isSameType( self, obj ):
		return isinstance( obj, ClientDongFuData )

class DongFuData( ClientDongFuData ):
	"""
	洞府数据
	"""
	def __init__( self  ):
		ClientDongFuData.__init__( self  )
		self.dongFuBase = None
		self.playerMB = None
		self.dongFuType = csdefine.SPACE_TYPE_PRIVATE
		self.lineNumber = 1
		self.position = (0,0,0)
		self.playerDBID = 0
		self.occupyProtectTime = 0.0
		self.dongFuState = csdefine.LHMJ_BUILD_STATE_NONE
		self.playerName = ""
		self.group = 0
		self.batteleID = 0
		self.destroyBuild = {}				# 需要被修复的建筑 {csdefine.LHMJ_BUIILD_LING_QUAN : "itemID:amount|itemID:amount"}
		self.fixBuild = {}					# 正在修复中的建筑  {csdefine.LHMJ_BUIILD_LING_QUAN:int(endTime)}
		self.buildLevels = {}
		self.buildLevels[csdefine.LHMJ_BUIILD_LING_QUAN] = 1
		self.buildLevels[csdefine.LHMJ_BUIILD_GONG_FANG] = 1
		self.buildLevels[csdefine.LHMJ_BUIILD_QIAN_KU_DING] = 1
		self.buildLevels[csdefine.LHMJ_BUIILD_SHOU_LAN] = 1
		self.buildLevels[csdefine.LHMJ_BUIILD_LING_TIAN] = 1
		self.guardType = []					# 洞府守卫类型
		self.guardReviveTime = 0			# 守卫复活时间
		
		self.challengeOtherDBID = 0			# 挑战其他玩家洞府的玩家DBID
		self.isPlunderActivity = 1			# 是否掠夺战
		self.activityStage = 0				# 活动阶段
		self.activityTime = 0				# 活动时间
		self.challengePlayerBase = None		# 挑战的玩家
		self.challengePlayerName = ""		# 挑战玩家名字
		self.challengePlayerDBID = 0		# 挑战玩家的DBID
		self.challengeDefaultTime = 0		# 到点执行默认应战
		self.canRefuseTime = csconst.LHMJ_CHALLENGE_REFUSE				# 一周可以拒绝的次数
		self.replyResult = {}				# 回应的结果 {DBID : csdefine.CHANLLENGE_REPLY_NONE}
	
	def onInitPlayerMB( self, playerBase ):
		"""初始化洞府玩家"""
		self.playerMB = playerBase
		data = {}
		for buildType, itemStr in self.destroyBuild.items():
			temp = {}
			for itemStrSplit in itemStr.split("|"):
				buildStr = itemStrSplit.split(":")
				if len(buildStr) >= 2:
					temp[int(buildStr[0])] = int(buildStr[1])
			data[buildType] = temp
		playerBase.cell.initDongFuDatas( self.dongFuType, self.lineNumber, self.group, self.position, self.buildLevels, data, self.fixBuild, self.guardReviveTime )

		if self.isSysReply():
			if self.isPlunderActivity:
				self.playerMB.client.statusMessage( csstatus.LHMJ_SYS_AGAIN_PLUNDER, self.challengePlayerName)
			else:
				self.playerMB.client.statusMessage( csstatus.LHMJ_SYS_AGAIN_CHALLENGE, self.challengePlayerName)
		
		if self.isNotReply():
			self.playerMB.client.ShowChallenge( self.challengePlayerName, self.canRefuseTime)
		elif self.isChallengeing():
			self.onActiveHasStart( playerBase, self.challengePlayerName, csdefine.BELONG_SIDE_PROTECT )
		self.playerMB.client.InitDongFuData( self, self.lineNumber, self.position )
	
	def onPlayerOffLine( self ):
		"""玩家下线"""
		self.playerMB = None
		
	def onChallengePlayerOnLine( self, playerBase, playerDBID ):
		"""挑战玩家上线"""
		if self.challengePlayerDBID != playerDBID:						# 有可能是上一次活动的挑战信息
			playerBase.cell.onRequestLHMJChallengeReplyNo()
			return
		if playerDBID in self.replyResult:
			replay = self.replyResult[playerDBID]
			if self.isChallengePlayer( playerDBID ):
				self.challengePlayerBase = playerBase
				playerBase.client.ShowChallengeMsg( self, self.lineNumber, self.position )
				playerBase.cell.onRequestLHMJChallengeReplyYes( self.lineNumber )
				playerBase.client.onRequestLHMJChallengeReply( replay, self.playerName, self.isPlunderActivity )
				# 如果已经开启活动了
				if self.isChallengeing():
					self.onActiveHasStart( playerBase, self.playerName, csdefine.BELONG_SIDE_ATTACK )
						
			elif replay == csdefine.CHANLLENGE_REPLY_NO:
				playerBase.cell.onRequestLHMJChallengeReplyNo()
				playerBase.client.onRequestLHMJChallengeReply( replay, self.playerName, self.isPlunderActivity )
		
	def onChallengePlayerOffLine( self ):
		"""挑战玩家下线"""
		self.challengePlayerBase = None
	
	def isNotReply( self ):
		"""被挑战了，但没答复"""
		return self.challengePlayerDBID and self.replyResult[self.challengePlayerDBID] == csdefine.CHANLLENGE_REPLY_NONE
	
	def isSysReply( self ):
		"""系统 默认应战"""
		return self.challengePlayerDBID and self.replyResult[self.challengePlayerDBID] == csdefine.CHANLLENGE_REPLY_SYS_YES
	
	def isChallengeing( self ):
		"""洞府是否正在被挑战"""
		if self.hasChallenge():
			if KBEngine.globalData.get("LHMJ_PlunderActive") or KBEngine.globalData.get("LHMJ_ChallengeActive"):
				return True
		return False
		
	def setChallengeOtherDBID( self, playerDBID ):
		"""
		设置本洞府的玩家要挑战的其他玩家
		用于解决，A挑战了其它洞府，其他人来挑战A
		"""
		self.challengeOtherDBID = playerDBID
		if self.hasChallenge():
			KBEDebug.ERROR_MSG("Must be err!!Please check!")
		if self.challengePlayerDBID:
			self.replyChallenge( csdefine.CHANLLENGE_REPLY_NO, True )
		
	def canChallengeOther( self ):
		"""
		是否能挑战别人
		如果被挑战了，或者挑战了，就不能再挑战或被挑战
		"""
		if self.challengeOtherDBID:
			return False
		return not self.hasChallenge()
		
	def hasChallenge( self ):
		"""是否有挑战"""
		return self.challengePlayerDBID and self.replyResult[self.challengePlayerDBID] in [ csdefine.CHANLLENGE_REPLY_YES, csdefine.CHANLLENGE_REPLY_SYS_YES]
	
	def isChallengePlayer( self, playerDBID ):
		"""是否是挑战的玩家"""
		if self.challengePlayerDBID == playerDBID:
			return self.hasChallenge()
		return False
	
	def onBuildDestroy( self, buildType, itemStr):
		"""洞府建筑被破坏"""
		self.destroyBuild[buildType] = itemStr
		if self.playerMB:
			data = {}
			for itemStrSplit in itemStr.split("|"):
				buildStr = itemStrSplit.split(":")
				if len(buildStr) >= 2:
					data[int(buildStr[0])] = int(buildStr[1])
			self.playerMB.cell.onDFBuildDestroy(buildType, data)
	
	def getMinRepairData( self ):
		""""""
		minTime = -1
		buildType = None
		for build, time in self.fixBuild.items():
			if buildType is None:
				minTime = time
				buildType = build
			elif time < minTime:
				minTime = time
				buildType = build
		return buildType, minTime
	
	def beginRepairBuild( self, buildType, endTime ):
		"""开始修复建筑"""
		self.fixBuild[buildType] = endTime
	
	def onBuildRepair( self, buildType ):
		"""洞府建筑修复完成"""
		self.destroyBuild.pop( buildType )
		self.fixBuild.pop( buildType )
		if self.playerMB:
			self.playerMB.cell.onRepairDFBuildFinish( buildType )
		pickArgs = {"spaceKey": str(self.playerDBID), "belongType" : csdefine.SPACE_BELONG_PERSON, "belongDBID" : self.playerDBID}
		KBEngine.globalData["SpaceManager"].remoteCallDomain( csconst.DONGFU_MAP_SPACESCRIPTID[self.dongFuType], "onBuildRepair", ( pickArgs, buildType ) )
	
	def changeMaster( self, baseMB, playerName, playerDBID ):
		"""洞府 易主"""
		self.playerMB = baseMB
		self.playerName = playerName
		self.playerDBID = playerDBID
		if baseMB:							# 交换洞府时，这个baseMB可能为None
			self.onInitPlayerMB( baseMB )
	
	def getBuildLevel( self, buildType ):
		"""获取建筑等级"""
		return self.buildLevels[buildType]
		
	def setBuildLevel( self, buildType, level ):
		"""设置建筑等级"""
		self.buildLevels[buildType] = level
		if buildType == csdefine.LHMJ_BUIILD_LING_QUAN:
			if self.dongFuBase:
				self.dongFuBase.updateDongFuLevel( level )
			if level in csconst.ADD_GUARD_LEVEL:
				self.guardType.append( csdefine.DONG_FU_GUARD_TYPE_DEFAULT )
		
	def changeGuardType( self, oldType, newType ):
		"""替换守卫类型"""
		self.guardType.remove( oldType )
		self.guardType.append( newType )
	
	def openBattele( self, itemID ):
		"""开启阵图"""
		self.batteleID = itemID
		
	def closeBattele( self ):
		"""关闭阵图"""
		self.batteleID = 0
		
	def noticeBattele( self ):
		""""""
		if self.batteleID and self.challengePlayerBase:
			KBEngine.globalData["SpaceManager"].remoteCallDomain( csconst.LUN_HUI_MI_JIN_SCRIPTID, "noticeMECPEnter", 
				( self.lineNumber, self.group, self.challengePlayerBase.id ) )
		
	def dealChallenge( self, playerBase, playerName, playerDBID, level ):
		"""处理挑战"""
		if self.challengePlayerDBID or self.challengeOtherDBID:			# 有人挑战了
			playerBase.statusMessage( csstatus.CHALLENGE_PEOPLE_TOO_MUSH, "" )
			return False
		if level <= Const.LHMJ_CHALLENGE_LEVEL:
			if self.getBuildLevel( csdefine.LHMJ_BUIILD_LING_QUAN ) < level:
				playerBase.statusMessage( csstatus.CHALLENGE_NO_AS_LEVEL, "" )
				return False
		else:
			if self.getBuildLevel( csdefine.LHMJ_BUIILD_LING_QUAN ) < level - 1:
				playerBase.statusMessage( csstatus.CHALLENGE_NO_AS_LEVEL, "" )
				return False
		if playerDBID in self.replyResult:		# 被回应了
			playerBase.statusMessage( csstatus.CHALLENGE_HAS_REFUSE_INVITE, "" )
			return False
		if KBEngine.globalData.get("LHMJ_ChallengeActiveReady"):
			if csdefine.LHMJ_BUIILD_LING_QUAN in self.destroyBuild:			# 灵泉坏了，无法抢夺
				KBEDebug.ERROR_MSG("Cannot lhmj challenge as lingquan not repair!!")
				return False
		if KBEngine.globalData.get("LHMJ_PlunderActiveReady"):
			for buildType in csconst.DF_PLUNDER_BUILDS:
				if buildType in self.destroyBuild:
					KBEDebug.ERROR_MSG("Cannot lhmj challenge as all builds not repair!!")		# 建筑坏了一个，无法掠夺
					return False
		
		self.isPlunderActivity = KBEngine.globalData.get("LHMJ_PlunderActiveReady", 0)
		self.challengePlayerBase = playerBase
		self.challengePlayerName = playerName
		self.challengePlayerDBID = playerDBID
		self.challengeDefaultTime = int(time.time()) + Const.LHMJ_DEFAULT_REPLY
		self.replyResult[playerDBID] = csdefine.CHANLLENGE_REPLY_NONE
		if self.playerMB:
			self.playerMB.client.ShowChallenge( playerName, self.canRefuseTime)
		return True
		
	def replyChallenge( self, replay, isSystemSet = False ):
		"""回应挑战"""
		if self.challengePlayerDBID in self.replyResult:
			if self.replyResult[self.challengePlayerDBID] != csdefine.CHANLLENGE_REPLY_NONE:
				return
		if len( self.replyResult ) > csconst.LHMJ_CHALLENGE_REFUSE and not isSystemSet:		# 超过拒绝次数，必然是应战
			replay = 1
		if replay:
			result = replay
			if self.playerMB:									# 因为有默认应战
				if self.isPlunderActivity:
					self.playerMB.statusMessage( csstatus.CHALLENGE_IS_ACCEPT_MY, self.challengePlayerName)
				else:
					self.playerMB.statusMessage( csstatus.PLUNDER_IS_ACCEPT_MY, self.challengePlayerName)
			if self.challengePlayerBase:
				self.challengePlayerBase.cell.onRequestLHMJChallengeReplyYes( self.lineNumber )
				self.challengePlayerBase.client.ShowChallengeMsg( self, self.lineNumber, self.position )		# 因为传输定义的是ClientDongFuData 类型，所以 这两个参数需要单独传
				self.challengePlayerBase.client.onRequestLHMJChallengeReply( replay, self.playerName, self.isPlunderActivity )
			KBEngine.globalData["SpaceLunHuiMiJinMgr"].onReplyChallenge( self.playerDBID, self.challengePlayerDBID )
		else:
			result = csdefine.CHANLLENGE_REPLY_NO
			if self.playerMB:
				if self.isPlunderActivity:
					self.playerMB.statusMessage( csstatus.CHALLENGE_IS_REFUSE_MY, self.challengePlayerName)
				else:
					self.playerMB.statusMessage( csstatus.PLUNDER_IS_REFUSE_MY, self.challengePlayerName)
			if self.challengePlayerBase:
				self.challengePlayerBase.cell.onRequestLHMJChallengeReplyNo()
				self.challengePlayerBase.client.onRequestLHMJChallengeReply( replay, self.playerName, self.isPlunderActivity )
		if not isSystemSet:
			self.replyResult[self.challengePlayerDBID] = result
		if result == csdefine.CHANLLENGE_REPLY_NO:
			self.canRefuseTime -= 1
			self.challengePlayerBase = None
			self.challengePlayerName = ""
			self.challengePlayerDBID = 0
			self.challengeDefaultTime = 0
			
	def clearChallengeData( self ):
		"""清除挑战数据"""
		self.challengePlayerBase = None
		self.challengePlayerDBID = 0
		self.challengeDefaultTime = 0
		self.challengePlayerName = ""
		self.replyResult = {}
		
	def onActiveStart( self ):
		"""掠夺战、争夺战 活动开启"""
		self.activityStage = 0
		self.activityTime = Functions.getTime( Const.LHMJ_FIRST_STAGE_TIME )
		if self.hasChallenge():			# 如果有挑战者,并且应战了
			pickArgs = {"spaceKey": str(self.playerDBID), "belongType" : csdefine.SPACE_BELONG_PERSON, "belongDBID" : self.playerDBID}
			KBEngine.globalData["SpaceManager"].remoteCallDomain( csconst.DONGFU_MAP_SPACESCRIPTID[self.dongFuType], "onChallengeActiveStart", ( pickArgs, ) )
			
			if self.playerMB:
				self.playerMB.cell.updateDFActiveStage( self.activityStage, not self.isPlunderActivity, csdefine.BELONG_SIDE_PROTECT, self.activityTime )
				self.playerMB.client.onDFActiveStart( self.isPlunderActivity, self.challengePlayerName )
				if self.challengePlayerBase:
					self.playerMB.client.updateLHMJChanllengeRelation( self.challengePlayerBase.id )
			
			if self.challengePlayerBase:
				if self.dongFuBase:
					self.dongFuBase.updateChallengeDBID( self.challengePlayerDBID, self.challengePlayerBase.id )
				self.noticeBattele()
				self.challengePlayerBase.cell.updateDFActiveStage( self.activityStage, not self.isPlunderActivity, csdefine.BELONG_SIDE_ATTACK, self.activityTime )
				self.challengePlayerBase.client.onDFActiveStart( self.isPlunderActivity, self.playerName )
				if self.playerMB:
					self.challengePlayerBase.client.updateLHMJChanllengeRelation( self.playerMB.id )
		else:
			self.clearChallengeData()
		
	def onActiveHasStart( self, player, playerName, belongSide ):
		"""活动已经开启,姗姗来迟"""
		if belongSide == csdefine.BELONG_SIDE_ATTACK:
			self.dongFuBase.updateChallengeDBID( self.challengePlayerDBID, self.challengePlayerBase.id )
			self.noticeBattele()
		if self.playerMB and self.challengePlayerBase:
			self.challengePlayerBase.client.updateLHMJChanllengeRelation( self.playerMB.id )
			self.playerMB.client.updateLHMJChanllengeRelation( self.challengePlayerBase.id )
		player.cell.updateDFActiveStage( self.activityStage, not self.isPlunderActivity, belongSide, self.activityTime )
		player.client.onDFActiveStart( self.isPlunderActivity, playerName )
		
	def addDFActiveStage( self ):
		"""增加活动阶段"""
		self.activityStage += 1
		if self.activityStage <= 1:
			self.activityTime = Functions.getTime( Const.LHMJ_SECONED_STAGE_TIME )
		if self.playerMB:
			self.playerMB.cell.updateDFActiveStage( self.activityStage, not self.isPlunderActivity, csdefine.BELONG_SIDE_PROTECT, self.activityTime )
		if self.challengePlayerBase:
			self.challengePlayerBase.cell.updateDFActiveStage( self.activityStage, not self.isPlunderActivity, csdefine.BELONG_SIDE_ATTACK, self.activityTime )
		
	def doDefaultChallenge( self ):
		"""没答复，默认应战"""
		if self.isNotReply() and not self.challengeOtherDBID:
			self.replyChallenge( csdefine.CHANLLENGE_REPLY_SYS_YES )
			self.challengeDefaultTime = 0
		
	def onActiveEnd( self, isChallengeActive ):
		"""掠夺战、争夺战 活动结束"""
		if self.challengePlayerDBID:
			pickArgs = {"spaceKey":str(self.playerDBID), "belongType" : csdefine.SPACE_BELONG_PERSON}
			KBEngine.globalData["SpaceManager"].remoteCallDomain( csconst.DONGFU_MAP_SPACESCRIPTID[self.dongFuType], "onChallengeActiveEnd", ( isChallengeActive, pickArgs, ) )
			self._calGuardRevTime()
			if self.challengePlayerBase:
				self.challengePlayerBase.cell.updateDFActiveStage( 2, not self.isPlunderActivity, csdefine.BELONG_SIDE_ATTACK, self.activityTime )
				self.challengePlayerBase.cell.onDFActiveEnd()
				self.challengePlayerBase.client.onDFActiveEnd()
			
			if self.playerMB:
				self.playerMB.cell.updateDFActiveStage( 2, not self.isPlunderActivity, csdefine.BELONG_SIDE_PROTECT, self.activityTime )
				self.playerMB.client.onDFActiveEnd()
				if self.guardReviveTime:
					self.playerMB.cell.onGuardReviveTime( self.guardReviveTime )
			self.clearChallengeData()
			if self.dongFuBase:
				self.dongFuBase.onActivityEnd()
				
		self.challengeOtherDBID = 0
		if isChallengeActive:
			self.canRefuseTime = csconst.LHMJ_CHALLENGE_REFUSE
	
	def onFinishActive( self ):
		"""完成挑战活动"""
		self._calGuardRevTime()
		if self.playerMB:
			self.playerMB.cell.updateDFActiveStage( 2, not self.isPlunderActivity, csdefine.BELONG_SIDE_PROTECT, self.activityTime )
			if self.guardReviveTime:
				self.playerMB.cell.onGuardReviveTime( self.guardReviveTime )
		if self.challengePlayerBase:
			self.challengePlayerBase.cell.updateDFActiveStage( 2, not self.isPlunderActivity, csdefine.BELONG_SIDE_ATTACK, self.activityTime )
		self.clearChallengeData()
		self.dongFuBase.onActivityEnd()
			
	
	def onMonsterCoverBeAttack( self, playerName ):
		"""保护罩被攻击"""
		if self.playerMB:
			self.playerMB.client.statusMessage( csstatus.DONG_FU_COVER_BEING_ATTACK, playerName )
	
	def onMonsterCoverBeKill( self, result ):
		"""
		保护罩被打坏了
		result为1，攻方没发msg;result为2，守方没发msg；result为3，双方都没发msg
		"""
		if result in [1,3] and self.challengePlayerBase:
			self.challengePlayerBase.client.statusMessage( csstatus.DONG_FU_COVER_DESTROY_ATTACK, "" )
		if result in [2,3] and self.playerMB:
			msgStr = self.challengePlayerName + "|" + self.challengePlayerName
			self.playerMB.client.statusMessage( csstatus.DONG_FU_COVER_DESTROY_PROTECT, msgStr )
	
	def noticeAPlayerEnter( self, playerName ):
		"""攻方玩家进入洞府"""
		if self.playerMB:
			self.playerMB.client.statusMessage( csstatus.DONG_FU_ENTER_BY_ATTACK, playerName )
	
	def onGuardDead( self ):
		"""守卫死亡"""
		self.guardReviveTime = Const.LHMJ_GUARD_REVIVE_TIME
	
	def _calGuardRevTime( self ):
		""""""
		if csdefine.LHMJ_BUIILD_LING_QUAN in self.destroyBuild:			# 如果灵泉坏了，则还不能计时
			return
		if self.guardReviveTime == Const.LHMJ_GUARD_REVIVE_TIME:		# 防止重复计算
			self.guardReviveTime += int( time.time() )
	
	def canCalRevTime( self ):
		""""""
		if self.guardReviveTime:
			if not csdefine.LHMJ_BUIILD_LING_QUAN in self.destroyBuild:
				return True
		return False
	
	def onGuardRevive( self ):
		""""""
		self.guardReviveTime = 0
		if self.playerMB:
			self.playerMB.cell.onGuardReviveTime( 0 )
			
	def doActiveReward( self, belongSide, result, rewards, gifts, destroyBuids, startTime, activeTime, deadNum, accountDBID, playerLevel ):
		"""活动结算，攻守方 可能不在洞府"""
		if belongSide == csdefine.BELONG_SIDE_ATTACK:
			playerBase = self.challengePlayerBase
			playerName = self.challengePlayerName
		else:
			playerBase = self.playerMB
			playerName = self.playerName
		if playerBase:
			playerBase.cell.doActiveReward( not self.isPlunderActivity, result, rewards, destroyBuids, startTime, activeTime, deadNum )
		else:
			if not playerName:
				KBEDebug.ERROR_MSG("Cannot find playerName(%d) in dfObj(dbid:%d)"%(belongSide, self.playerDBID))
				return
			actResult = LogDefine.ACTIVE_STATE_TYPE_SUCCESS
			action = LogDefine.ACTIVE_SPACE_TYPE_DFLDZ
			if self.isPlunderActivity:
				title = cschannel_msgs.DF_ACTIVE_PLUNDER_TITLE
				if result in [1,3, 4]:
					content = cschannel_msgs.DF_ACTIVE_PLUNDER_SUCCESS_CONTENT
				else:
					content = cschannel_msgs.DF_ACTIVE_PLUNDER_FAIL_CONTENT
					actResult = LogDefine.ACTIVE_STATE_TYPE_FAIL
			else:
				title = cschannel_msgs.DF_ACTIVE_CHALLENGE_TITLE
				action = LogDefine.ACTIVE_SPACE_TYPE_DFZDZ
				if result in [1,3, 4]:
					content = cschannel_msgs.DF_ACTIVE_CHALLENGE_SUCCESS_CONTENT
				else:
					content = cschannel_msgs.DF_ACTIVE_CHALLENGE_FAIL_CONTENT
					actResult = LogDefine.ACTIVE_STATE_TYPE_FAIL
			itemDatas = []
			for itemID in gifts:
				itemInst = ItemFactory.ItemFactoryInst.createDynamicItem(itemID, 1, {})
				if not itemInst:
					KBEDebug.ERROR_MSG("LunHuiMiJin\BuildDepleteCfg.json has not item=%i"%(itemID))
					continue
				itemDatas.append( itemInst )
				if not result:
					actResult = LogDefine.ACTIVE_STATE_TYPE_FAIL
				g_logger.roleActiveRecord(action, accountDBID, self.playerDBID, playerLevel, LogDefine.ACTIVE_REWARD_TYPE_ITEM, itemInst.id, startTime, activeTime, actResult)
			KBEngine.globalData["MailManager"].send( None, playerName,csdefine.MAIL_SENDER_TYPE_SYS,
			cschannel_msgs.MAIL_SEND_SYSTEM, title, content, 0, 0, itemDatas, 0, 0 )
	
	def getDictFromObj( self, obj ):
		dict = {
			"lineNumber"	: obj.lineNumber,
			"group"			: obj.group,
			"position" 		: obj.position,
			"playerDBID"	: obj.playerDBID,
			"playerName"	: obj.playerName,
			"occupyProtectTime"	: obj.occupyProtectTime,
			"dongFuState"	: obj.dongFuState,
			"batteleID"		: obj.batteleID,
			"destroyBuild"	: obj.destroyBuild,
			"fixBuild"		: obj.fixBuild,
			"buildLevels"	: obj.buildLevels,
			"guardType" 	: obj.guardType,
			"guardReviveTime" : obj.guardReviveTime,
		}
		return dict
	
	def createObjFromDict( self, dict ):
		obj = self.__class__()
		obj.lineNumber = dict[ "lineNumber" ]
		obj.group = dict[ "group" ]
		obj.position = dict[ "position" ]
		obj.playerDBID = dict["playerDBID"]
		obj.playerName = dict["playerName"]
		obj.occupyProtectTime = dict["occupyProtectTime"]
		obj.dongFuState = dict["dongFuState"]
		obj.group = dict[ "group" ]
		obj.playerName = dict["playerName"]
		obj.batteleID = dict["batteleID"]
		obj.guardType = dict["guardType"]
		obj.guardReviveTime = dict["guardReviveTime"]
		if dict["destroyBuild"]:
			obj.destroyBuild = dict["destroyBuild"]
		if dict["fixBuild"]:
			obj.fixBuild = dict["fixBuild"]
		if dict["buildLevels"]:
			obj.buildLevels = dict["buildLevels"]
		return obj
		
	def isSameType( self, obj ):
		return isinstance( obj, DongFuData )

class DongFuDataMgr( dict ):
	"""
	洞府数据管理器
	"""
	def __init__( self ):
		self.lineNumberMapData = {}					# 便于排序
	
	def initData( self, dict ):
		for m  in dict[ "datas" ]:
			if m.lineNumber not in self:
				self[m.lineNumber] = {}
			self[ m.lineNumber ][m.group] = m

	def addDongFuData( self, lineNumber, group, dongFuMail, position, dongFuType ):
		"""
		增加洞府初始化数据
		"""
		if lineNumber not in self:
			self[lineNumber] = {}
		if group not in self[lineNumber]:
			self[lineNumber][group] = DongFuData()
		self[lineNumber][group].lineNumber = lineNumber
		self[lineNumber][group].group = group
		self[lineNumber][group].position = position
		self[lineNumber][group].dongFuBase = dongFuMail
		self[lineNumber][group].dongFuType = dongFuType
		if not self[lineNumber][group].guardType:
			if dongFuType == csdefine.SPACE_TYPE_PRIVATE:
				self[lineNumber][group].guardType = [ csdefine.DONG_FU_GUARD_TYPE_DEFAULT ]
			else:
				self[lineNumber][group].guardType = [ csdefine.DONG_FU_GUARD_TYPE_DEFAULT, csdefine.DONG_FU_GUARD_TYPE_DEFAULT ]

	def updateDongFuOccupyData( self, lineNumber, group, playerMB, playerDBID, playerName, occupyProtectTime ):
		"""
		更新占领信息
		"""
		if lineNumber in self:
			if group in self[lineNumber]:
				self[lineNumber][group].playerMB = playerMB
				self[lineNumber][group].playerDBID = playerDBID
				self[lineNumber][group].playerName = playerName
				self[lineNumber][group].occupyProtectTime = occupyProtectTime

	def getMinProtectDongFu( self ):
		"""获取最短保护状态的洞府"""
		minTime = 0.0
		minData = None
		for lineNumber, datas in self.items():
			for group, dfObj in datas.items():
				if dfObj.dongFuState == csdefine.LHMJ_BUILD_STATE_OCUPPY:
					if minTime == 0.0:
						minTime = dfObj.occupyProtectTime
						minData = dfObj
					else:
						if minTime < dfObj.occupyProtectTime:
							minTime = dfObj.occupyProtectTime
							minData = dfObj
		return minData

	def getFreeDFNum( self, lineNumber ):
		"""没有被占领的洞府"""
		freeNum = 0
		for dfObj in self[lineNumber].values():
			if dfObj.playerDBID == 0:
				freeNum += 1
		return freeNum

	def getDFDataByLineNumber( self, playerDBID, lineNumber, offset ):
		"""获取的某线洞府数据"""
		# 因为 我的洞府 和 被我挑战的洞府置顶了，所以在排序的时候 放到最后！不传给客户端
		if not lineNumber in self:
			KBEDebug.ERROR_MSG("Cannot find lineNumber(%d)"%lineNumber)
			return
		data = sorted(self[lineNumber].values(), key = lambda x :(x.playerDBID != playerDBID, not x.isChallengePlayer(playerDBID) 
			, x.buildLevels[csdefine.LHMJ_BUIILD_LING_QUAN], x.playerName, x.dongFuType), reverse = 1)
		self.lineNumberMapData[lineNumber] = data
		totalNum = len( data )
		totalPage = math.ceil(totalNum / Const.LHMJ_DONG_FU_SHOW_ENTRY)
		freeDFNum = 0
		for index, dfObj in enumerate( data ):
			if dfObj.playerDBID == 0:
				freeDFNum = totalNum - index - 1 - offset			# 因为我的洞府 和 挑战的洞府排到最后了
				break
		tail = Const.LHMJ_DONG_FU_SHOW_ENTRY - offset
		return totalPage, freeDFNum, data[0:tail]
		
	def getDFDataByPage( self, playerDBID, lineNumber, page = 1, offset = 0):
		"""获取某一页的洞府数据"""
		if not lineNumber in self.lineNumberMapData or self.lineNumberMapData[lineNumber][-1] != playerDBID:			# 如果 我有洞府，且不相等的话！说明 别人也排序了，需要重新拍
			data = sorted(self[lineNumber].values(), key = lambda x :(x.playerDBID != playerDBID, not x.isChallengePlayer(playerDBID) 
				, x.buildLevels[csdefine.LHMJ_BUIILD_LING_QUAN], x.playerName, x.dongFuType), reverse = 1)
			self.lineNumberMapData[lineNumber] = data
		else:
			data = self.lineNumberMapData[lineNumber]
		
		head = max((page - 1) * Const.LHMJ_DONG_FU_SHOW_ENTRY - offset, 0)
		tail = page * Const.LHMJ_DONG_FU_SHOW_ENTRY - offset
		return data[head : tail]
		
	def getMinRepairTimeDF( self ):
		"""获取最短修复建筑时间的洞府"""
		minTime = -1
		minDfObj = None
		for lineNumber, lineDatas in self.items():
			for dfObj in lineDatas.values():
				if dfObj.fixBuild:
					if minDfObj is None:
						minDfObj = dfObj
						minTime = min( dfObj.fixBuild.values() )
					else:
						mTime = min( dfObj.fixBuild.values() )
						if mTime < minTime:
							minDfObj = dfObj
							minTime = mTime
		return minTime, minDfObj
		
	def getMinDefaultReplyTime( self ):
		"""获取最短 默认时间答复"""
		temp = []
		for lineDatas in self.values():
			temp.extend( lineDatas.values() )
		temp.sort(key = lambda x: ( not x.isNotReply(), x.challengeDefaultTime))
		return temp[0]
		
	def getMinGReviveTime( self ):
		"""获取 守卫复活的最短时间"""
		temp = []
		for lineDatas in self.values():
			temp.extend( lineDatas.values() )
		temp.sort(key = lambda x: (not x.canCalRevTime(), x.guardReviveTime))
		return temp[0] if temp else None
		
	def onActiveStart( self ):
		"""活动开始"""
		for lineNumber, groupDatas in self.items():
			for group, dfObj in groupDatas.items():
				dfObj.onActiveStart()
		
	def onActiveEnd( self, isChallengeActive ):
		"""活动结束"""
		for lineNumber, groupDatas in self.items():
			for group, dfObj in groupDatas.items():
				dfObj.onActiveEnd(isChallengeActive)
		
	def getDictFromObj( self, obj ):
		tempDict = {}
		tempDict[ "datas" ] = []
		for mObj in list(obj.values()):
			for obj in list(mObj.values()):
				tempDict[ "datas" ].append( obj )
			
		return tempDict
	
	def createObjFromDict( self, dict ):
		obj = DongFuDataMgr()
		obj.initData( dict )
		return obj
		
	def isSameType( self, obj ):
		return isinstance( obj, DongFuDataMgr )

g_DongFuDataMgr = DongFuDataMgr()
g_DongFuData = DongFuData()
g_CDongFuData = ClientDongFuData()
