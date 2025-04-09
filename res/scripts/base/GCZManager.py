# -*- coding: utf-8 -*-

from CoreObject import MgrPersistentObject
from ConfigObject.Crond.CrondDatas import CrondDatas
g_CrondDatas = CrondDatas.instance()
import KBEngine
import KBEDebug
import time
import csstatus
import csdefine
from Functions import Functor

REQ_OBJ_TYPE_PERSON		= 1
REQ_OBJ_TYPE_TEAM		= 2

FIRST_MATCH_TIME = 4 * 60	# 第一阶段匹配前4分钟
SECOND_MATCH_TIME = 4 * 60 +30 # 第二阶段匹配前4分钟

GCZ_SPACE_CLASS_NAME = "fu_ben_L_GCZ"

class PlayerData( object ):
	"""
	一个玩家数据
	"""
	def __init__( self, mailBox, playerDBID, playerLevel ):
		self.playerMB = mailBox
		self.playerDBID = playerDBID
		self.playerLevel = playerLevel

	def getPlayerDBID( self ):
		return self.playerDBID

	def getPlayerLevel( self ):
		return self.playerLevel

class ReqBase( object ):
	_type = 0
	
	def getType( SELF ):
		return SELF._type

class ReqPersonInfos( ReqBase ):
	"""
	单个玩家匹配类
	"""
	_type = REQ_OBJ_TYPE_PERSON
	def __init__( self, playerMB, playerDBID, playerLevel ):
		self.playerObj = PlayerData( playerMB, playerDBID,playerLevel )

	def getAllPlayerMB( self ):
		return [self.playerObj.playerMB]

	def getAllPlayerDBID( self ):
		return [self.playerObj.playerDBID]

	def getID( self ):
		return self.playerObj.playerMB.id

	def isItemPlayer( self, playerID ):
		"""
		判断是否为该玩家
		"""
		return self.playerObj.playerMB.id == playerID

	def getCaptainLevel( self, captainID ):
		return self.playerObj.getPlayerLevel()

	def getPlayerNum( self ):
		"""
		获得总人数
		"""
		return 1

	def notifyToStartMatchGCZ( self ):
		"""
		通知开始匹配 显示匹配界面
		"""
		for playerMB in self.getAllPlayerMB():
			playerMB.notifyToStartMatchGCZ( len( self.getAllPlayerMB() ) )

	def notifyCancelMatchGCZ( self ):
		"""
		取消匹配
		"""
		for playerMB in self.getAllPlayerMB():
			playerMB.notifyCancelMatchGCZ()

	def matchGCZTeamChange( self ):
		"""
		队伍成员变化 取消匹配
		"""
		self.notifyCancelMatchGCZ()
		for playerMB in self.getAllPlayerMB():
			if hasattr( playerMB,"client" ) and playerMB.client:
				playerMB.client.statusMessage( csstatus.GCZ_MATCH_FORBID_TEAM_MEMBER_CHANGE,"" )

class ReqTeamInfos( ReqBase ):
	"""
	队伍匹配类
	"""
	_type = REQ_OBJ_TYPE_TEAM
	def __init__( self, teamMB, captainID,memberDataList):
		self.teamMB = teamMB
		self.captainID = captainID
		self.memberList = []
		for memberData in memberDataList:
			self.memberList.append( PlayerData(memberData["playerMB"], memberData["playerDBID"],memberData["playerLevel"] ))

	def getID( self ):
		return self.teamMB.id

	def getCaptainMB( self ):
		captainMB = None
		for member in self.memberList:
			if member.playerMB.id == self.captainID:
				captainMB = member.playerMB
		return captainMB

	def getTeamMB( self ):
		return self.teamMB

	def getCaptainLevel( self, captainID ):
		for member in self.memberList:
			if member.playerMB.id == captainID:
				return member.getPlayerLevel()

		return 0

	def getPlayerNum( self ):
		"""
		获得总人数
		"""
		return len( self.memberList )

	def getAllPlayerMB( self ):
		return [ member.playerMB for member in self.memberList ]

	def getAllPlayerDBID( self ):
		return [ member.playerDBID for member in self.memberList ]

	def isItemPlayer( self, playerID ):
		"""
		判断玩家是否在匹配列表中
		"""
		return playerID in [member.playerMB.id for member in self.memberList ]

	def notifyToStartMatchGCZ( self ):
		"""
		通知开始匹配 显示匹配界面
		"""
		for playerMB in self.getAllPlayerMB():
			playerMB.notifyToStartMatchGCZ( len( self.getAllPlayerMB() ) )

	def notifyCancelMatchGCZ( self ):
		"""
		取消匹配
		"""
		for playerMB in self.getAllPlayerMB():
			playerMB.notifyCancelMatchGCZ()

	def notfiyToOtherTeamMemberCanCelMath( self ):
		"""
		队长取消匹配
		"""
		self.notifyCancelMatchGCZ()
		for playerMB in self.getAllPlayerMB():
			if hasattr( playerMB,"client" ) and playerMB.client:
				playerMB.client.statusMessage( csstatus.GCZ_TEAMCAPTAIN_CANCEL_MATCH,"" )

	def matchGCZTeamChange( self ):
		"""
		队伍成员变化 取消匹配
		"""
		self.notifyCancelMatchGCZ()
		for playerMB in self.getAllPlayerMB():
			if hasattr( playerMB,"client" ) and playerMB.client:
				playerMB.client.statusMessage( csstatus.GCZ_MATCH_FORBID_TEAM_MEMBER_CHANGE,"" )

	def memberLoginOff( self, playerName ):
		"""
		"""
		self.notifyCancelMatchGCZ()
		for playerMB in self.getAllPlayerMB():
			if hasattr( playerMB,"client" ) and playerMB.client:
				playerMB.client.statusMessage( csstatus.GCZ_MATCH_CANCEL_BY_OFFLINE_MEMBER,playerName )

class MatchObj( object ):
	"""
	一个匹配战队
	"""
	def __init__( self, reqObjList ):
		self.teamMB = None
		self.reqObjList = reqObjList
		self.waiteJoinTeamList = []		#等待加入队伍的mailbox列表
		self.joinTeamList = [] 	# 已加入队伍的mailBox列表
		self.teamCaptainLevel = 0 #队长等级

	def getAllPlayerMB( self ):
		"""
		获得所有玩家MailBox
		"""
		mailBoxlist = []
		for reqobj in self.reqObjList:
			mailBoxlist.extend( reqobj.getAllPlayerMB() )
		return mailBoxlist

	def getAllPlayerDBID( self ):
		"""
		获得所有玩家的playerDBID
		"""
		dbidList = []
		for reqobj in self.reqObjList:
			dbidList.extend( reqobj.getAllPlayerDBID() )
		return dbidList

	def isItemPlayer( self, playerID ):
		"""
		是否为该玩家
		"""
		for reqobj in self.reqObjList:
			if reqobj.isItemPlayer( playerID ):
				return True
		return False

	def getReqObjByPlayerID( self, playerID ):
		"""
		"""
		for reqobj in self.reqObjList:
			if reqobj.isItemPlayer( playerID ):
				return reqobj
		return None

	def doOnMatch( self, mgr ):
		"""
		匹配成功后操作
		"""
		for reqobj in self.reqObjList:
			mgr.gcz_popReq( reqobj )

		self.createTeam()

	def createTeam( self ):
		"""
		创建一支队伍
		"""
		allPlayerMBList = self.getAllPlayerMB()
		if not len(allPlayerMBList):
			return

		reqObj = self.getReqObjByPlayerID( self.getCaptainMB().id )
		if not reqObj:
			return
		if reqObj.getType() == REQ_OBJ_TYPE_TEAM:
			self.teamMB = reqObj.getTeamMB()
			self.teamCaptainLevel = reqObj.getCaptainLevel(reqObj.captainID)
			for playerMB in allPlayerMBList:
				if reqObj.isItemPlayer( playerMB.id ):
					continue
				self.waiteJoinTeamList.append( playerMB )
			
			if len(self.waiteJoinTeamList) == 0:
				self.preCreateSpace()
				return
			for mb in self.waiteJoinTeamList:
				mb.GCZOnJoinTeam( reqObj.captainID, self.teamMB )
		else:
			for playerMB in allPlayerMBList:
				if playerMB.id != self.getCaptainMB().id:
					self.waiteJoinTeamList.append(playerMB)
			self.getCaptainMB().GCZCreateTeam()

	def getCaptainLevelByCaptainID( self, captainID ):
		"""
		获得队长等级
		"""
		for reqobj in self.reqObjList:
			if reqobj.isItemPlayer( captainID ):
				return reqobj.getCaptainLevel(captainID)
		return 0

	def onCreateTeam( self, captainMB, teamMB ):
		"""
		创建队伍回调
		"""
		if self.teamMB != None:
			return
		self.teamMB = teamMB
		
		self.teamCaptainLevel = self.getCaptainLevelByCaptainID( captainMB.id )
		if len(self.waiteJoinTeamList) == 0:
			self.preCreateSpace()
			return
		for mb in self.waiteJoinTeamList:
			mb.GCZOnJoinTeam( captainMB.id, teamMB )

	def onGCZMemberJoin( self, playerMB ):
		"""
		加入队伍的回调
		"""
		self.joinTeamList.append( playerMB )
		if len( self.joinTeamList ) == len( self.waiteJoinTeamList ):
			self.preCreateSpace()

	def preCreateSpace( self ):
		"""
		全部加入队伍后  创建攻城战Space
		"""
		# 预创建副本空间
		spaceParams = {}
		spaceParams["spaceKey"] = str( self.teamMB.id )
		spaceParams["belongType"] = csdefine.SPACE_BELONG_TEAM
		spaceParams["enterPlayerDBID"] = self.getAllPlayerDBID()
		spaceParams["teamID"] = self.teamMB.id
		spaceParams["packSpaceLevel"] = self.teamCaptainLevel
		KBEngine.globalData["SpaceManager"].remoteCallDomain( GCZ_SPACE_CLASS_NAME,"requestNewSpace",(spaceParams,))
		for playerMB in self.getAllPlayerMB():
			playerMB.cell.matchGCZSuccess(GCZ_SPACE_CLASS_NAME)

	def getCaptainMB( self ):
		"""
		获得队长
		"""
		hasAllPersonReq = True	# 是不是所有人都是个人请求
		for reqobj in self.reqObjList:
			if reqobj.getType() == REQ_OBJ_TYPE_TEAM:
				hasAllPersonReq = False
				break
		if hasAllPersonReq:
			return self.reqObjList[0].getAllPlayerMB()[0]
		else:
			captainMB = None
			reqTeamList = [ i for i in self.reqObjList if i.getType() == REQ_OBJ_TYPE_TEAM ]
			reqPersonList = [ i for i in self.reqObjList if i.getType() == REQ_OBJ_TYPE_PERSON ]
			if len(reqTeamList) == 1:
				captainMB = reqTeamList[0].getCaptainMB()
			if len(reqTeamList) == 2:
				if len(reqTeamList[0].getAllPlayerMB()) > len( reqTeamList[1].getAllPlayerMB() ):
					captainMB = reqTeamList[0].getCaptainMB()
				elif len(reqTeamList[0].getAllPlayerMB()) < len( reqTeamList[1].getAllPlayerMB() ):
					captainMB = reqTeamList[1].getCaptainMB()
				else:
					captainMB = reqPersonList[0].getAllPlayerMB()[0]
			else:
				captainMB = self.reqObjList[0].getAllPlayerMB()[0]
			return captainMB
			
class GCZManager( MgrPersistentObject.MgrPersistentObject ):
	"""
	CST-12515 攻城战管理器
	"""
	def __init__( self ) :
		MgrPersistentObject.MgrPersistentObject.__init__( self )
		self.register()
		self.openMatchNumber = 0	# 开放的匹配场次
		self.joinGCZMatch = {}
		self.gczMatchSuccess = {} 	# 匹配成功数据
		self.onCompleteInit()
	
	def register( self ):
		"""
		所有帮会初始化完成
		"""
		taskEvents = { 
						"GCZSignUpStart":"onGCZSignUpStart",
						"GCZSignUpEnd":"onGCZSignUpEnd",
						"GCZStart":"onGCZStart",
						"GCZNotifyJoinMemberMatchStart":"onGCZNotifyJoinMemberMatchStart",
						"GCZNotifyJoinMemberMatchEnd":"onGCZNotifyJoinMemberMatchEnd",
						"GCZNotifyEnter":"onGCZNotifyEnter",
						"GCZNotifyEnterClose":"onGCZNotifyEnterClose",
						"GCZEnd":"onGCZEnd",
		}
		for taskName, callbackName in taskEvents.items():
			for scriptID, cmd in g_CrondDatas.getCrondTaskCmds(taskName):
				KBEngine.globalData["CrondManager"].addScheme( scriptID, cmd, self, callbackName, -1,() )

	def onGCZSignUpStart( self, cmd ):
		"""
		攻城战 报名开始
		"""
		KBEngine.globalData["GCZStatus"] = [csdefine.GCZ_ACTIVITY_STATUS_SIGNUP]

	def onGCZSignUpEnd( self, cmd ):
		"""
		攻城战 报名结束
		"""
		if csdefine.GCZ_ACTIVITY_STATUS_SIGNUP in KBEngine.globalData.get("GCZStatus",[]):
			status = list(KBEngine.globalData["GCZStatus"])
			status.remove( csdefine.GCZ_ACTIVITY_STATUS_SIGNUP )
			KBEngine.globalData["GCZStatus"] = status

	def onGCZStart( self, cmd ):
		"""
		攻城战 活动开始
		"""
		status = list(KBEngine.globalData.get("GCZStatus",[]))
		status.append( csdefine.GCZ_ACTIVITY_STATUS_START )
		KBEngine.globalData["GCZStatus"] = status

	def onGCZEnd( self, cmd ):
		"""
		攻城战 活动结束
		"""
		KBEngine.globalData["GCZStatus"] = []
		self.joinGCZMemDatas = {}
		self.openMatchNumber = 0
		self.joinGCZMatch = {}
		self.gczMatchSuccess = {}

	def openJoinGCZWin( self, numGCZs, gczStartTimes, gczMaxJoinNums, playerMB, npcID ):
		"""
		打开参加攻城战面板
		"""
		gczRemainJoinNums = []
		for num in numGCZs:
			index = numGCZs.index(num)
			if num not in self.joinGCZMemDatas:
				gczRemainJoinNums.append( gczMaxJoinNums[index] )
			else:
				if index + 1 in self.joinGCZMemDatas:
					remainNum = gczMaxJoinNums[index] - len(self.joinGCZMemDatas[index + 1])
				else:
					remainNum = gczMaxJoinNums[index]
				gczRemainJoinNums.append(remainNum)

		if hasattr( playerMB, "client" ) and playerMB.client:
			playerMB.client.OpenJoinGCZWin( numGCZs, gczStartTimes, gczRemainJoinNums, npcID )

	def signUpGCZ( self, number,playerMB, playerDBID,maxJoinNum, startTime ):
		"""
		报名攻城战
		number : 代表场次
		"""
		if csdefine.GCZ_ACTIVITY_STATUS_SIGNUP not in KBEngine.globalData.get("GCZStatus",[]):
			return

		if number not in self.joinGCZMemDatas:
			self.joinGCZMemDatas[number] = []

		args = "{0}|{1}".format( startTime.split(":")[0],startTime.split(":")[1] )
		if len(self.joinGCZMemDatas[number]) >= maxJoinNum:
			if hasattr( playerMB, "client" ) and playerMB.client:
				playerMB.client.statusMessage( csstatus.GCZ_SIGN_UP_FORBID_NUMBER_PERSON, args )
			return

		allJoinPlayerDBIDs = []
		for playerDBIDs in self.joinGCZMemDatas.values():
			allJoinPlayerDBIDs.extend( playerDBIDs )

		if playerDBID in allJoinPlayerDBIDs:
			if hasattr( playerMB, "client" ) and playerMB.client:
				playerMB.client.statusMessage( csstatus.GCZ_ALREADY_SIGN_UP, "" )
			return

		self.joinGCZMemDatas[number].append( playerDBID )

		if hasattr( playerMB, "client" ) and playerMB.client:
			playerMB.client.statusMessage( csstatus.GCZ_SIGN_UP_SUCCESS, args )


	def onGCZNotifyJoinMemberMatchStart( self, cmd ):
		"""
		通知参加攻城战的玩家可以进行匹配了
		"""
		status = list(KBEngine.globalData.get("GCZStatus",[]))
		status.append( csdefine.GCZ_ACTIVITY_STATUS_MATCH )
		KBEngine.globalData["GCZStatus"] = status
		self.openMatchNumber += 1
		self.notfiyJoinMembers()
		self.addTimerCallBack( FIRST_MATCH_TIME, "breakTeamReqToPersonReq",() ) # 四分钟后未匹配成功的队伍变成单人匹配
		self.addTimerCallBack( SECOND_MATCH_TIME,"remainToBuildTeam",() ) # 最后剩下的组成一个队伍

	def onGCZNotifyJoinMemberMatchEnd( self, cmd ):
		"""
		关闭匹配
		"""
		if csdefine.GCZ_ACTIVITY_STATUS_MATCH in KBEngine.globalData.get("GCZStatus",[]):
			status = list(KBEngine.globalData["GCZStatus"])
			status.remove( csdefine.GCZ_ACTIVITY_STATUS_MATCH )
			KBEngine.globalData["GCZStatus"] = status

	def onGCZNotifyEnter( self, cmd ):
		"""
		开始进入选项
		"""
		status = list(KBEngine.globalData.get("GCZStatus",[]))
		status.append( csdefine.GCZ_ACTIVITY_STATUS_ENTER )
		KBEngine.globalData["GCZStatus"] = status

	def onGCZNotifyEnterClose( self, cmd ):
		"""
		关闭开始进入选项
		"""
		if csdefine.GCZ_ACTIVITY_STATUS_ENTER in KBEngine.globalData.get("GCZStatus",[]):
			status = list(KBEngine.globalData["GCZStatus"])
			status.remove( csdefine.GCZ_ACTIVITY_STATUS_ENTER )
			KBEngine.globalData["GCZStatus"] = status

	def notfiyJoinMembers( self ):
		"""
		提示参与该场的玩家进行匹配
		"""
		if self.openMatchNumber not in self.joinGCZMemDatas:
			KBEDebug.ERROR_MSG("GCZ Match num%i has not member"%self.openMatchNumber)
			return
		for playerDBID in self.joinGCZMemDatas[self.openMatchNumber]:
			KBEngine.lookUpEntityByDBID( "Role", playerDBID, Functor( self.notfiyJoinMemberCallBack, self.joinGCZMemDatas[self.openMatchNumber] ) )

	def notfiyJoinMemberCallBack( self, playerDBIDs,target ):
		"""
		"""
		if target is False:
			return
		if target is True:
			return

		target.notfiyToJoinGCZ( playerDBIDs )

	def reStartToMathGCZ( self, playerMB, playerDBID ):
		"""
		重新开始匹配
		"""
		if self.openMatchNumber not in self.joinGCZMemDatas:
			return
		if self.openMatchNumber in self.gczMatchSuccess:
			for matchObj in self.gczMatchSuccess[ self.openMatchNumber ]:
				if matchObj and matchObj.isItemPlayer(playerMB.id):
					playerMB.statusMessage( csstatus.GCZ_MATCH_FORBID_MATCH_SUCCESS,"" )
					return

		if playerDBID in self.joinGCZMemDatas[self.openMatchNumber]:
			playerMB.notfiyToJoinGCZ( self.joinGCZMemDatas[self.openMatchNumber] )
		else:
			playerMB.statusMessage( csstatus.GCZ_MATCH_FORBID_SIGNUP )

	def joinGCZMatchPerson( self, playerMB, playerDBID,playerLevel ):
		"""
		个人参加攻城战匹配
		"""
		obj = ReqPersonInfos( playerMB,playerDBID,playerLevel )
		self.joinGCZ_PushReq( obj )
		obj.notifyToStartMatchGCZ()
		self.gcz_TryMatch()

	def joinGCZMahchTeam( self, playerMB, teamMB, memberDataList, captainID ):
		"""
		队伍参加攻城战匹配
		"""
		if not len( memberDataList ):
			return

		if self.openMatchNumber in self.joinGCZMatch:
			reqList = self.joinGCZMatch[self.openMatchNumber]
			if teamMB.id in [ obj.getID() for obj in reqList ]:
				return
		reqobj = ReqTeamInfos( teamMB, captainID,memberDataList)
		self.joinGCZ_PushReq( reqobj )
		reqobj.notifyToStartMatchGCZ()
		self.gcz_TryMatch()

	def gcz_cancelMatch( self, playerMB ):
		"""
		取消匹配
		"""
		for reqobj in self.joinGCZMatch[ self.openMatchNumber ]:
			if reqobj.isItemPlayer( playerMB.id ):
				if reqobj.getType() == REQ_OBJ_TYPE_TEAM:
					reqobj.notfiyToOtherTeamMemberCanCelMath()
				else:
					reqobj.notifyCancelMatchGCZ()
				self.joinGCZMatch[self.openMatchNumber].remove( reqobj )
				break

	def joinGCZ_PushReq( self, obj ):
		"""
		压入请求列表
		"""
		if self.openMatchNumber not in self.joinGCZMatch:
			self.joinGCZMatch[self.openMatchNumber] = []

		self.joinGCZMatch[self.openMatchNumber].append( obj )

	def gcz_TryMatch( self ):
		"""
		攻城战尝试匹配
		"""
		reqList = self.joinGCZMatch[self.openMatchNumber]
		matchIndexs = self.getMatchReqObjIndexs( reqList )
		if matchIndexs:
			matchObj = MatchObj( [reqList[index] for index in matchIndexs] )
			self.gcz_pushMatch( matchObj )
			matchObj.doOnMatch(self)

	def gcz_pushMatch( self, matchObj ):
		"""
		匹配成功列表
		"""
		if self.openMatchNumber not in self.gczMatchSuccess:
			self.gczMatchSuccess[ self.openMatchNumber ] = []

		self.gczMatchSuccess[self.openMatchNumber].append( matchObj )

	def getMatchReqObjIndexs( self, reqList ):
		"""
		获取一组报名小队中能组成5人战队的小队的index
		"""
		Num = 5
		for indexI,reqObjI in enumerate(reqList):
			NumI = reqObjI.getPlayerNum()
			if NumI == Num:
				return [indexI]
			elif NumI < Num:
				sumNum = NumI
				resultList = [indexI]
				for indexJ, reqObjJ in enumerate(reqList):
					NumJ = reqObjJ.getPlayerNum()
					if indexI == indexJ or indexJ in resultList:
						continue
					
					elif sumNum + NumJ < Num:
						sumNum += NumJ
						resultList.append( indexJ )
					
					elif sumNum + NumJ == Num:
						resultList.append( indexJ )
						return resultList

		return []
	
	def gcz_popReq( self, reqobj ):
		"""
		弹出请求列表
		"""
		if self.openMatchNumber not in self.joinGCZMatch:
			return
		for item in self.joinGCZMatch[self.openMatchNumber]:
			if item.getID() == reqobj.getID():
				self.joinGCZMatch[self.openMatchNumber].remove( item )
				reqobj.notifyCancelMatchGCZ()
				break

	def gcz_onCreateTeam( self, captainMB, teamMB ):
		"""
		创建队伍回调
		"""
		if self.openMatchNumber not in self.gczMatchSuccess:
			return
		for matchObj in self.gczMatchSuccess[ self.openMatchNumber ]:
			if matchObj and matchObj.isItemPlayer(captainMB.id):
				matchObj.onCreateTeam( captainMB, teamMB )
				break

	def onGCZMemberJoin( self, playerMB ):
		"""
		攻城战成员加入
		"""
		for matchObj in self.gczMatchSuccess[ self.openMatchNumber ]:
			if matchObj and matchObj.isItemPlayer( playerMB.id ):
				matchObj.onGCZMemberJoin( playerMB )
				break

	def breakTeamReqToPersonReq( self ):
		"""
		将剩下队伍改为单人匹配 打乱为单人匹配
		"""
		if self.openMatchNumber not in self.joinGCZMatch:
			return

		tempReqTeam = []
		for reqobj in self.joinGCZMatch[ self.openMatchNumber ]:
			if reqobj.getType() == REQ_OBJ_TYPE_TEAM:
				tempReqTeam.append(reqobj)

		for tempReqObj in tempReqTeam:
			self.joinGCZMatch[ self.openMatchNumber ].remove( tempReqObj )

		for tempReqObj in tempReqTeam:
			for member in tempReqObj.memberList:
				obj = ReqPersonInfos( member.playerMB,member.playerDBID,member.playerLevel )
				self.joinGCZ_PushReq( obj )
			self.gcz_TryMatch()
			
	def gcz_MatchTeamChange( self, playerMB ):
		"""
		匹配过程中 队伍成员发生变化 取消匹配
		"""
		for reqobj in self.joinGCZMatch[ self.openMatchNumber ]:
			if reqobj.isItemPlayer( playerMB.id ):
				reqobj.matchGCZTeamChange()
				self.joinGCZMatch[self.openMatchNumber].remove( reqobj )
				break

	def gcz_memberLoginOff( self, playerMB, playerName ):
		"""
		成员掉线 取消匹配
		"""
		for reqobj in self.joinGCZMatch[ self.openMatchNumber ]:
			if reqobj.isItemPlayer( playerMB.id ):
				if reqobj.getType() == REQ_OBJ_TYPE_TEAM:
					reqobj.memberLoginOff(playerName)
				else:
					reqobj.notifyCancelMatchGCZ()
				self.joinGCZMatch[self.openMatchNumber].remove( reqobj )
				break

	def enterGCZ( self, playerMB, playerDBID, teamID ):
		"""
		进入攻城战
		"""
		if playerDBID not in self.joinGCZMemDatas[self.openMatchNumber]:
			playerMB.statusMessage( csstatus.GCZ_ENTER_FORBID_SIGNUP,"" )
			return
		if self.openMatchNumber not in self.gczMatchSuccess:
			playerMB.statusMessage( csstatus.GCZ_ENTER_FORBID_NOT_MATCH,"" )
			return
		if teamID not in [ matchObj.teamMB.id for matchObj in self.gczMatchSuccess[ self.openMatchNumber ] ]:
			playerMB.statusMessage( csstatus.GCZ_ENTER_FORBID_NOT_MATCH,"" )
			return

		playerMB.cell.onEnterGCZSpace( GCZ_SPACE_CLASS_NAME )

	def remainToBuildTeam( self ):
		"""
		最后剩下的成员组成队伍
		"""
		if self.openMatchNumber not in self.joinGCZMatch:
			return
		if not len( self.joinGCZMatch[self.openMatchNumber] ):
			return
		matchObj = MatchObj( list(self.joinGCZMatch[ self.openMatchNumber ]) )
		self.gcz_pushMatch( matchObj )
		matchObj.doOnMatch(self)
