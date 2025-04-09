# -*- coding: utf-8 -*-

import random
import csdefine
import KBEDebug
import KBEngine
import Math
import KST
import csconst
import Functions
import Const
import csstatus
import HotConst
from CoreObject import MgrPersistentObject
from ObjectScript.ObjectScriptFactory import g_objFactory
from ConfigObject.Crond.CrondDatas import CrondDatas
g_CrondDatas = CrondDatas.instance()


REQ_OBJ_TYPE_PERSON		= 1
REQ_OBJ_TYPE_TEAM		= 2

MATCH_FAILURE_TIME = 180	#匹配失败的时间
MATCH_TIME_OUT_ARG = 30		#匹配超过3分钟参数
TIMER_ARG_TELEPORT = 40		#传送等待倒计时参数

# 活动玩法最大人数	
# MATCH_NUMBER = {
# 	csdefine.ACTIVITY_TYPE_CAMP_YXLM		:	Const.SPACECOPY_CAMP_YXLM_MATCH_NUMBER,
# 	csdefine.ACTIVITY_TYPE_CAMP_SGMZ		:	Const.SPACECOPY_CAMP_SGMZ_MATCH_NUMBER,
# 	csdefine.ACTIVITY_TYPE_CAMP_YCJMD		:	Const.SPACECOPY_CAMP_YCJMD_MATCH_NUMBER,
# 	csdefine.ACTIVITY_TYPE_CAMP_LING_MAI	:	Const.CAMP_LING_MAI_MATCH_NUM,
# 	csdefine.ACTIVITY_TYPE_CAMP_FIVE_YCJMD	:	Const.SPACECOPY_CAMP_FIVE_YCJMD_MATCH_NUMBER,
# }

# 活动副本名
SPACE_COPY_NAME = {
	csdefine.ACTIVITY_TYPE_CAMP_YXLM		:	"fu_ben_L_YXWZ",
	csdefine.ACTIVITY_TYPE_CAMP_SGMZ		:	"fu_ben_L_SGMZ",
	csdefine.ACTIVITY_TYPE_CAMP_YCJMD		:	"fu_ben_L_YCJMD_zhenyingPVP",
	csdefine.ACTIVITY_TYPE_CAMP_LING_MAI	:	"fu_ben_L_LMZC",
	csdefine.ACTIVITY_TYPE_CAMP_FIVE_YCJMD	:	"fu_ben_L_YCJMD_zhenyingPVP_wuren1",
}

class PlayerData( object ):
	"""
	一个玩家数据类
	"""
	def __init__( self, mailBox, playerDBID, camp, level, name ):
		self.playerMB = mailBox
		self.playerDBID = playerDBID
		self.camp = camp
		self.level = level
		self.name = name

	def getCamp( self ):
		"""
		获得玩家阵营
		"""
		return self.camp

	def getDictToClient( self ):
		tdict  = {}
		tdict[ "id" ] = str(self.playerMB.id)
		tdict[ "camp" ] = str(self.camp)
		tdict[ "level" ] = str(self.level)
		tdict[ "name" ] = self.name
		return tdict

class ReqBase( object ):
	_type = 0
	
	def getType( SELF ):
		return SELF._type

	def getCamp( self ):
		return self.camp

class ReqPersonInfos( ReqBase ):
	"""
	单个玩家匹配类
	"""
	_type = REQ_OBJ_TYPE_PERSON
	def __init__( self, playerMB, playerDBID, camp, level, name, timeID ):
		self.playerObj = PlayerData( playerMB,playerDBID,camp,level,name )
		self.level = level
		self.camp = camp
		self.name = name
		self.matchTimeID = timeID

	def nofityClientSignup( self ):
		self.playerObj.playerMB.campRandomFitJoin()
		if self.playerObj.playerMB.client:
			self.playerObj.playerMB.client.OnCampRandomFitStart()

	def getDictToClient( self ):
		"""
		打包数据发给客户端
		"""
		return [ self.playerObj.getDictToClient() ]

	def getAllPlayerDBID( self ):
		"""
		获得所有成员DBID
		"""
		return [ self.playerObj.playerDBID ]

	def isItemPlayer( self, playerID ):
		"""
		判断是否为该玩家
		"""
		return self.playerObj.playerMB.id == playerID

	def getID( self ):
		return self.playerObj.playerMB.id

	def getPlayerNum( self ):
		"""
		获得总人数
		"""
		return 1

	def getAllPlayerMB( self ):
		"""
		获得所有成员
		"""
		return [ self.playerObj.playerMB ]

	def quitSignUp( self, message = csstatus.CAMP_RANDOM_FIT_CANCEL ):
		"""
		退出报名
		"""
		self.playerObj.playerMB.campRandomFitQuit()
		self.playerObj.playerMB.statusMessage( message, "" )
		if self.playerObj.playerMB.client:
			self.playerObj.playerMB.client.OnCampRandomFitInterrupt()

	def onMatch( self ):
		"""
		匹配成功
		"""
		if self.playerObj.playerMB.client:
			self.playerObj.playerMB.client.OnCampRandomFitSuccess()

	def removePlayer( self, playerMB ):
		"""
		删除玩家
		"""
		pass

	def onOutFit(self):
		"""
		退出匹配
		"""
		pass

class ReqTeamInfos( ReqBase ):
	"""
	队伍匹配类
	"""
	_type = REQ_OBJ_TYPE_TEAM
	def __init__( self, teamMB, memberDataList, camp, level, timeID ):
		self.teamMB = teamMB 
		self.camp = camp
		self.level = level
		self.matchTimeID = timeID
		self.memberList = []
		for memberData in memberDataList:
			self.memberList.append( PlayerData( memberData["playerMB"], memberData["playerDBID"], memberData["camp"],memberData["level"], memberData["name"] ) )

	def isItemPlayer( self, playerID ):
		"""
		判断玩家是否在匹配列表中
		"""
		return playerID in [member.playerMB.id for member in self.memberList ]

	def getAllPlayerDBID( self ):
		"""
		获得所有成员DBID
		"""
		memberDBIDList = []
		for member in self.memberList:
			memberDBIDList.append( member.playerDBID )
		return memberDBIDList

	def nofityClientSignup( self ):
		self.teamMB.setIsReqCampRandomFit(True)
		for member in self.memberList:
			member.playerMB.campRandomFitJoin()
			if member.playerMB.client:
				member.playerMB.client.OnCampRandomFitStart()

	def getDictToClient( self ):
		"""
		打包数据发给客户端
		"""
		memberData = []
		for member in self.memberList:
			memberData.append(member.getDictToClient())

		return memberData

	def getID( self ):
		return self.teamMB.id

	def getPlayerNum( self ):
		"""
		获得总人数
		"""
		return len(self.memberList)

	def getAllPlayerMB( self ):
		"""
		获得所有成员
		"""
		return [ member.playerMB for member in self.memberList ]

	def quitSignUp( self, message = csstatus.CAMP_RANDOM_FIT_CANCEL ):
		"""
		退出报名
		"""
		for member in self.memberList:
			member.playerMB.campRandomFitQuit()
			member.playerMB.statusMessage( message, "" )
			if member.playerMB.client:
				member.playerMB.client.OnCampRandomFitInterrupt()

	def onMatch( self ):
		"""
		匹配成功
		"""
		for member in self.memberList:
			if member.playerMB.client:
				member.playerMB.client.OnCampRandomFitSuccess()

	def removePlayer( self, playerMB ):
		"""
		删除玩家
		"""
		for member in self.memberList:
			if member.playerMB.id == playerMB.id:
				self.memberList.remove(member)
				return

	def onOutFit(self):
		"""
		退出匹配
		"""
		self.teamMB.setIsReqCampRandomFit(False)

class MatchObj( object ):
	"""
	一个匹配战队
	"""
	def __init__( self, camp, reqObjList, activityType ):
		self.captainDBID = 0
		self.camp = camp
		self.reqObjList = reqObjList
		self.activityType = activityType
		self.teamList = []			#已加入队伍的mailBox列表
		self.initData()

	def initData(self):
		"""
		初始化数据
		"""
		for reqObj in self.reqObjList:
			if reqObj.getType() == REQ_OBJ_TYPE_TEAM:
				self.teamList.append(reqObj.getID())
		self.setCaptainDBID(self.getAllPlayerDBID()[0])

	def setCaptainDBID(self, DBID):
		"""
		设置战队队长DBID
		"""
		self.captainDBID = DBID

	def getCaptainDBID(self):
		"""	
		获得战队队长DBID
		"""
		return self.captainDBID

	def getDictToClient( self ):
		"""
		打包一个战队数据发给客户端
		"""
		memberListDict = []
		for reqObj in self.reqObjList:
			memberListDict.extend(reqObj.getDictToClient())
		return memberListDict

	def getAllPlayerDBID( self ):
		"""
		"""
		memberDBIDList = []
		for reqObj in self.reqObjList:
			memberDBIDList.extend( reqObj.getAllPlayerDBID() )
		return memberDBIDList

	def isSelfTeamReqObj( self, teamID ):
		"""
		是此战队中的某个队伍
		""" 
		for reqObj in self.reqObjList:
			if reqObj.getType() == REQ_OBJ_TYPE_TEAM and reqObj.getID() == teamID:
				return True
		return False

	def isItemPlayer( self, playerID ):
		"""
		"""
		for reqObj in self.reqObjList:
			if reqObj.isItemPlayer(playerID):
				return True
		return False

	def getAllPlayerMB( self ):
		"""
		获得所有玩家Mailbox
		"""
		_list = []
		for reqObj in self.reqObjList:
			_list.extend( reqObj.getAllPlayerMB() )
		return _list

	def getWaitAffirmList( self ):
		"""
		获得所有等待玩家确认的ID列表
		"""
		_list = []
		for mb in self.getAllPlayerMB():
			if mb.id not in self.affirmList:
				_list.append( mb.id )
		return _list

	def doOnMatch( self, mgr ):
		"""
		执行匹配完后的工作
		"""
		for reqObj in self.reqObjList:
			mgr.randomFit_popReq(self.activityType, reqObj)
			mgr.randomFit_popTimeoutReq(self.activityType, reqObj)
			reqObj.onMatch()

	def showEnterTime( self, time ):
		"""
		显示倒计时进入副本时间
		"""
		for playerMB in self.getAllPlayerMB():
			if playerMB.client:
				playerMB.client.ShowEnterRandomFitTime(time)

	def removePlayer( self, playerMB ):
		"""
		删除玩家
		"""
		tempObj = None
		for reqObj in self.reqObjList:
			if reqObj.isItemPlayer(playerMB.id):
				tempObj = reqObj
		if tempObj.getType() == REQ_OBJ_TYPE_TEAM and tempObj.getPlayerNum() > 1:
			tempObj.removePlayer( playerMB )
		else:
			self.reqObjList.remove(tempObj)

	def onOutFit(self):
		"""
		退出匹配
		"""
		for reqObj in self.reqObjList:
			reqObj.onOutFit()

class MatchItem( object ):
	"""
	一对匹配了的战队
	"""
	def __init__( self, mgr, timerID, objectA, objectB, activityType ):
		self.objectA = objectA
		self.objectB = objectB
		self.matchTimeID = timerID
		self.objectA.doOnMatch(mgr)
		self.objectB.doOnMatch(mgr)
		self.enterSpaceTimerID = None
		self.activityType = activityType
		self.SGMZRoute = random.sample( range( 0, 4 ), 2 )

	def setEnterTimer( self, timerID, time ):
		"""
		设置进入副本倒计时
		"""
		self.enterSpaceTimerID = timerID
		self.objectA.showEnterTime(time)
		self.objectB.showEnterTime(time)

	def isItemPlayer( self, playerID ):
		"""
		"""
		return self.objectA.isItemPlayer(playerID) or self.objectB.isItemPlayer(playerID)

	def onMatchObjCreateTeam( self, mgr ):
		"""
		某个战队匹配成功
		"""
		spaceParams = {}
		routeParams = {}
		routeParams[csdefine.CAMP_TAOSIM] = self.SGMZRoute[0]
		routeParams[csdefine.CAMP_DEMON] = self.SGMZRoute[1]
		spaceParams["spaceKey"] = SPACE_COPY_NAME[self.activityType]
		spaceParams["belongType"] = csdefine.SPACE_BELONG_NORMAL
		spaceParams["playerDBIDs"] = self.objectA.getAllPlayerDBID() + self.objectB.getAllPlayerDBID()
		spaceParams["routeParams"] = routeParams
		spaceParams["packSpaceLevel"] = int(self.objectA.reqObjList[0].level /10) * 10 + 5
		KBEngine.globalData["SpaceManager"].remoteCallDomain( SPACE_COPY_NAME[self.activityType], "requestNewSpace",(spaceParams,))
		mgr.randomFit_removeMatch(self)
		mgr.randomFit_pushSuccessMath( self )

	def teleportToCopy( self, mgr ):
		"""
		传送玩家
		"""
		if self.activityType == csdefine.ACTIVITY_TYPE_CAMP_SGMZ:
			self.teleportToSGMZCopy(mgr)
			return

		#仙
		pos,direction = self.getEnterInfos( csdefine.CAMP_TAOSIM )
		for playerMB in self.objectA.getAllPlayerMB():
			playerMB.campRandomFitQuit()
			playerMB.cell.campFitTeleport( SPACE_COPY_NAME[self.activityType], pos, direction )

		#魔
		pos,direction = self.getEnterInfos( csdefine.CAMP_DEMON )
		for playerMB in self.objectB.getAllPlayerMB():
			playerMB.campRandomFitQuit()
			playerMB.cell.campFitTeleport( SPACE_COPY_NAME[self.activityType], pos, direction )

		self.objectA.onOutFit()
		self.objectB.onOutFit()

		mgr.randomFit_removeSuccessMatch( self )

	def teleportToSGMZCopy( self, mgr ):
		"""
		传送玩家到上古密阵
		"""
		spaceObj = KST.g_objFactory.getSpaceObject( SPACE_COPY_NAME[self.activityType] )
		#仙
		pos,direction = spaceObj.getEnterPos( csdefine.CAMP_TAOSIM, self.SGMZRoute[0] )
		for playerMB in self.objectA.getAllPlayerMB():
			playerMB.cell.gotoSpace( SPACE_COPY_NAME[self.activityType], pos, direction )
			playerMB.campRandomFitQuit()
		#魔
		pos,direction = spaceObj.getEnterPos( csdefine.CAMP_DEMON, self.SGMZRoute[1] )
		for playerMB in self.objectB.getAllPlayerMB():
			playerMB.cell.gotoSpace( SPACE_COPY_NAME[self.activityType], pos, direction )
			playerMB.campRandomFitQuit()

		self.objectA.onOutFit()
		self.objectB.onOutFit()

		mgr.randomFit_removeSuccessMatch( self )

	def getEnterInfos( self, camp ):
		"""
		获取玩家要进入的坐标
		"""
		spaceObj = KST.g_objFactory.getSpaceObject( SPACE_COPY_NAME[self.activityType] )
		return spaceObj.getEnterPos(camp)

	def removePlayer( self, playerMB ):
		"""
		删除玩家
		"""
		if self.objectA.isItemPlayer( playerMB.id ):
			self.objectA.removePlayer( playerMB )
		if self.objectB.isItemPlayer( playerMB.id ):
			self.objectB.removePlayer( playerMB)

class CampActivityRandomFitMgr(MgrPersistentObject.MgrPersistentObject ):
	"""
	阵营战场随机匹配
	"""
	def __init__(self):
		MgrPersistentObject.MgrPersistentObject.__init__( self )
		self.register()
		self._reqDict = {}				#所有请求参与的玩家列表
		self._timeoutReqDict = {}		#请求超时参与的玩家列表
		self._matchItemDict = {}		#所有已匹配的列表
		self._successMathDict = {}		#已匹配成功的列表

		self._activityState  = False	#是否开启活动
		self.onCompleteInit()

	def register( self ):
		"""
		注册
		"""
		taskEvents = { "CampActivityRandomFitMgr_Notice":"onActiveNotice",
						"CampActivityRandomFitMgr_Start":"onActiveStart",
						"CampActivityRandomFitMgr_End":"onActiveEnd"
		 }
		for taskName, callbackName in taskEvents.items():
			for scriptID, cmd in g_CrondDatas.getCrondTaskCmds(taskName):
		 		KBEngine.globalData["CrondManager"].addScheme( scriptID, cmd, self, callbackName, -1,() )

	def onActiveNotice( self, cmd ):
		"""
		活动公告
		"""
		KST.g_baseAppEntity.globalWold( csstatus.CAMP_RANDOM_FIT_NOTIFY, "" )

	def onActiveStart( self, cmd ):
		"""
		活动开始
		"""
		self._activityState = True
		KST.g_baseAppEntity.globalWold( csstatus.CAMP_RANDOM_FIT_START, "" )

	def onActiveEnd( self, cmd ):
		"""
		活动结束
		"""
		self._activityState = False
		KST.g_baseAppEntity.globalWold( csstatus.CAMP_RANDOM_FIT_END, "" )
		for spaceName in SPACE_COPY_NAME.values():
			KBEngine.globalData["SpaceManager"].remoteCallDomain( spaceName ,"activityEnd",[] )

	def randomFit_reqPerson( self, activityType, playerMB, playerDBID, camp, level, name ):
		"""
		个人申请
		"""
		if not self._activityState:
			playerMB.statusMessage(csstatus.SPACECOPY_CAMP_YXLM_NOT_START,"")
			return
		timeID = self.addTimer( MATCH_FAILURE_TIME, 0, MATCH_TIME_OUT_ARG )
		reqObj = ReqPersonInfos( playerMB, playerDBID, camp, level, name, timeID )
		self.randomFit_pushReq( activityType, reqObj )
		self.randomFit_tryMatch(activityType, level)

	def randomFit_reqTeam( self, activityType, playerMB, teamMB, memberDataList, camp, level ):
		"""
		队伍申请
		"""
		if not len(memberDataList):
			return
		if not self._activityState:
			playerMB.statusMessage( csstatus.SPACECOPY_CAMP_YXLM_NOT_START,"")
			return
		timeID = self.addTimer( MATCH_FAILURE_TIME, 0, MATCH_TIME_OUT_ARG )
		reqObj = ReqTeamInfos( teamMB, memberDataList, camp, level, timeID )
		self.randomFit_pushReq( activityType, reqObj )
		self.randomFit_tryMatch(activityType, level)

	def randomFit_cancelSignUp( self, playerMB ):
		"""
		取消随机匹配
		"""
		for activityType, reqObjList in self._reqDict.items():
			for reqObj in reqObjList:
				if reqObj and reqObj.isItemPlayer(playerMB.id):
					reqObj.quitSignUp()
					self.randomFit_popReq(activityType, reqObj)
					self.randomFit_popTimeoutReq(activityType, reqObj)
					return

	def randomFit_onTeamChange( self, teamMB ):
		"""
		队伍人数变动，取消申请
		"""
		removeReqObj = None
		activityType = 0
		for key, reqObjList in self._reqDict.items():
			for reqObj in reqObjList:
				if reqObj.getType() == REQ_OBJ_TYPE_TEAM and reqObj.getID() == teamMB.id:
					activityType = key
					removeReqObj = reqObj
					break
			if removeReqObj:
				break
		if removeReqObj:
			removeReqObj.quitSignUp( csstatus.CAMP_RANDOM_FIT_LEAVE )
			self.randomFit_popReq(activityType, removeReqObj)
			self.randomFit_popTimeoutReq(activityType, removeReqObj)

	def randomFit_onJoinTeam( self, playerMB ):
		"""
		加入队伍，取消申请
		"""
		removeReqObj = None
		activityType = 0
		for key, reqObjList in self._reqDict.items():
			for reqObj in reqObjList:
				if reqObj and reqObj.isItemPlayer( playerMB.id ):
					activityType = key
					removeReqObj = reqObj
					break
			if removeReqObj:
				break
		if removeReqObj:
			removeReqObj.quitSignUp()
			self.randomFit_popReq(activityType, removeReqObj)
			self.randomFit_popTimeoutReq(activityType, removeReqObj)

	def randomFit_onPlayerLoginOff( self, playerMB, playerName ):
		"""
		玩家下线
		"""
		removeReqObj = None
		activityType = 0
		for key, reqObjList in self._reqDict.items():
			for reqObj in reqObjList:
				if reqObj and reqObj.isItemPlayer( playerMB.id ):
					activityType = key
					removeReqObj = reqObj
					break
			if removeReqObj:
				break
		if removeReqObj:		
			removeReqObj.quitSignUp( csstatus.CAMP_RANDOM_FIT_MEB_OFFLINE )
			self.randomFit_popReq(activityType, removeReqObj)
			self.randomFit_popTimeoutReq(activityType, removeReqObj)

		# 自动离开队伍
		playerMB.leaveTeamFB( playerMB.id )

		# 如果已经匹配完成时
		for matchItemList in self._matchItemDict.values():
			for matchItem in matchItemList:
				if matchItem and matchItem.isItemPlayer(playerMB.id):
					matchItem.removePlayer( playerMB )
					return

	def randomFit_pushReq( self, activityType, reqObj ):
		"""
		压入请求列表
		"""
		if activityType not in self._reqDict:
			self._reqDict[activityType] = []
		self._reqDict[activityType].append(reqObj)
		reqObj.nofityClientSignup()

	def randomFit_popReq( self, activityType, reqObj ):
		"""
		弹出请求列表
		"""
		for item in self._reqDict[activityType]:
			if item.getID() == reqObj.getID():
				self._reqDict[activityType].remove( item )
				break

	def randomFit_tryMatch( self, activityType, level ):
		"""
		尝试匹配
		"""
		t_reqObjList = [ obj for obj in self._reqDict[activityType] if obj.getCamp() == csdefine.CAMP_TAOSIM and int(obj.level/10) == int(level/10)]
		d_reqObjList = [ obj for obj in self._reqDict[activityType] if obj.getCamp() == csdefine.CAMP_DEMON  and int(obj.level/10) == int(level/10)]
		tMatchIndexs = self.getMatchReqObjIndexs( activityType, t_reqObjList )
		dMatchIndexs = self.getMatchReqObjIndexs( activityType, d_reqObjList )
		if tMatchIndexs and dMatchIndexs:
			t_MatchObj = MatchObj( csdefine.CAMP_TAOSIM,[ t_reqObjList[index] for index in tMatchIndexs ], activityType )
			d_MatchObj = MatchObj( csdefine.CAMP_DEMON, [d_reqObjList[index] for index in dMatchIndexs ], activityType )
			self.randomFit_pushMatch( activityType, t_MatchObj,d_MatchObj )	

	def getMatchReqObjIndexs( self, activityType, campReqList ):
		"""
		获取一组报名小队中能组成战队index
		"""
		Num = HotConst.MATCH_NUMBER[activityType]
		for indexI,reqObjI in enumerate(campReqList):
			NumI = reqObjI.getPlayerNum()
			if NumI == Num:
				return [indexI]
			elif NumI <	Num:
				sumNum = NumI
				resultList = [indexI]
				for indexJ, reqObjJ in enumerate(campReqList):
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

	def randomFit_pushMatch( self, activityType, matchObjA, matchObjB ):
		"""
		压入已匹配列表
		"""
		if activityType not in self._matchItemDict:
			self._matchItemDict[activityType] = []
		matchItem = MatchItem(self, 0, matchObjA, matchObjB, activityType)
		self._matchItemDict[activityType].append( matchItem )
		matchItem.onMatchObjCreateTeam( self )

	def randomFit_removeMatch( self, matchItem ):
		"""
		移除已匹配列表
		"""
		if matchItem.activityType not in self._matchItemDict or matchItem not in self._matchItemDict[matchItem.activityType]:
			KBEDebug.ERROR_MSG("CampActivityRandomFitMgr _matchItemDict has not this matchItem")
			return

		self._matchItemDict[matchItem.activityType].remove(matchItem)

	def randomFit_pushSuccessMath( self, matchItem ):
		"""
		压入确认匹配成功列表
		"""
		timerID = self.addTimer(3.0, 0, TIMER_ARG_TELEPORT )
		matchItem.setEnterTimer(timerID,3.0)
		if matchItem.activityType not in self._successMathDict:
			self._successMathDict[matchItem.activityType] = []
		self._successMathDict[matchItem.activityType].append(matchItem)

	def randomFit_removeSuccessMatch( self, matchItem ):
		"""
	 	移除确认匹配成功列表
		"""
		if matchItem.activityType not in self._successMathDict:
			return
		if matchItem not in self._successMathDict[matchItem.activityType]:
			return
		self._successMathDict[matchItem.activityType].remove(matchItem)

	def randomFit_pushTimeoutReq( self, activityType, reqObj ):
		"""
		压入超时请求列表
		"""
		if activityType not in self._timeoutReqDict:
			self._timeoutReqDict[activityType] = []
		self._timeoutReqDict[activityType].append(reqObj)
		self.randomFit_tryTimeoutMatch(activityType, reqObj.level)

	def randomFit_popTimeoutReq( self, activityType, reqObj ):
		"""
		弹出超时请求列表
		"""
		if activityType not in self._timeoutReqDict:
			return
		for item in self._timeoutReqDict[activityType]:
			if item.getID() == reqObj.getID():
				self._timeoutReqDict[activityType].remove( item )
				break

	def randomFit_tryTimeoutMatch( self, activityType, level ):
		"""
		尝试超时匹配
		"""
		t_reqObjList = [ obj for obj in self._timeoutReqDict[activityType] if obj.getCamp() == csdefine.CAMP_TAOSIM and int(obj.level/10) == int(level/10)]
		d_reqObjList = [ obj for obj in self._timeoutReqDict[activityType] if obj.getCamp() == csdefine.CAMP_DEMON and int(obj.level/10) == int(level/10)]
		tMatchIndexs, tAmount = self.getMatchTimeoutReqObjIndexs( activityType, t_reqObjList )
		dMatchIndexs, dAmount = self.getMatchTimeoutReqObjIndexs( activityType, d_reqObjList )
		if tMatchIndexs and dMatchIndexs and tAmount == dAmount:
			t_MatchObj = MatchObj( csdefine.CAMP_TAOSIM,[ t_reqObjList[index] for index in tMatchIndexs ], activityType )
			d_MatchObj = MatchObj( csdefine.CAMP_DEMON, [d_reqObjList[index] for index in dMatchIndexs ], activityType )
			self.randomFit_pushMatch( activityType, t_MatchObj,d_MatchObj )	

	def getMatchTimeoutReqObjIndexs( self, activityType, campReqList ):
		"""
		获取一组超时小队中能组成战队index
		"""	
		Num = 15 if HotConst.MATCH_NUMBER[activityType] > 5 else 5
		amount = 0
		# 5v5 必须双方匹配人数到达5人，才匹配成功
		if Num == 5:
			for indexI,reqObjI in enumerate(campReqList):
				NumI = reqObjI.getPlayerNum()
				if NumI == Num:
					amount = NumI
					return [indexI], amount
				elif NumI <	Num:
					sumNum = NumI
					resultList = [indexI]
					for indexJ, reqObjJ in enumerate(campReqList):
						NumJ = reqObjJ.getPlayerNum()
						if indexI == indexJ or indexJ in resultList:
							continue
						
						elif sumNum + NumJ < Num:
							sumNum += NumJ
							resultList.append( indexJ )
						
						elif sumNum + NumJ == Num:
							resultList.append( indexJ )
							amount = sumNum + NumJ
							return [indexI], amount
		else:  #下浮匹配人数，最低不少于15人，当双方人数相等
			for indexI,reqObjI in enumerate(campReqList):
				NumI = reqObjI.getPlayerNum()
				if NumI >= Num and NumI <= HotConst.MATCH_NUMBER[activityType]:
					amount = NumI
					return [indexI], amount
				elif NumI <	Num:
					sumNum = NumI
					resultList = [indexI]
					for indexJ, reqObjJ in enumerate(campReqList):
						NumJ = reqObjJ.getPlayerNum()
						if indexI == indexJ or indexJ in resultList:
							continue
						
						elif sumNum + NumJ < Num:
							sumNum += NumJ
							resultList.append( indexJ )
						
						elif (sumNum + NumJ) >= Num and (sumNum + NumJ) <= HotConst.MATCH_NUMBER[activityType]:
							resultList.append( indexJ )
							amount = sumNum + NumJ
							return resultList, amount
		return [], amount

	def onTimer( self, id, userArg ):
		"""
		addTimer回调函数
		"""
		if userArg == MATCH_TIME_OUT_ARG:
			for activityType, reqObjList in self._reqDict.items():
				for reqObj in reqObjList:
					if reqObj.matchTimeID == id:
						self.randomFit_pushTimeoutReq(activityType, reqObj)
						break
		elif userArg == TIMER_ARG_TELEPORT:
			for matchItemList in self._successMathDict.values():
				for matchItem in matchItemList:
					if matchItem.enterSpaceTimerID == id:
						matchItem.teleportToCopy( self )
						break