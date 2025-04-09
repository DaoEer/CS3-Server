# -*- coding: utf-8 -*-

import random
import KBEDebug
import Math
import KBEngine
import csdefine
from CoreObject import MgrPersistentObject
import csstatus
import KST
import csconst
import Functions
import time

REQ_OBJ_TYPE_PERSON		= 1
REQ_OBJ_TYPE_TEAM		= 2

MATCH_FAILURE_TIME = 1800    #匹配失败的时间
MATCH_FAILURE_TIME_ARG = 30  #匹配失败参数


RE_CALC_MATCH_TIME = 60 #重新预计的匹配时间60秒
RE_CALC_MATCH_TIME_ARG = 100 #预计匹配时间的参数

CALC_MATCH_SUCCESS_TIME = 90 #预计匹配的时间

class PlayerData( object ):
	"""
	一个玩家数据类
	"""
	def __init__( self, mailBox, playerDBID, level, name ):
		self.playerMB = mailBox
		self.playerDBID = playerDBID
		self.level = level
		self.name = name

	def getDictToClient( self ):
		tdict  = {}
		tdict[ "id" ] = str(self.playerMB.id)
		tdict[ "level" ] = str(self.level)
		tdict[ "name" ] = self.name
		return tdict

class ReqBase( object ):
	_type = 0
	
	def getType( SELF ):
		return SELF._type

class ReqPersonInfos( ReqBase ):
	"""
	单个玩家匹配类
	"""
	_type = REQ_OBJ_TYPE_PERSON
	def __init__( self, playerMB, playerDBID, level, name, spaceScriptID, timeID ):
		self.playerObj = PlayerData( playerMB,playerDBID,level,name )
		self.level = level
		self.name = name
		self.spaceScriptID = spaceScriptID
		self.matchTimeID = timeID
		self.reqPerTime = time.time()
		self.calcMatchTime = 0
		self.calcMatchTimerID = 0

	def getReqTime( self ):
		return self.reqPerTime

	def notifyClientFastTeamSignUp( self, calcMatchTime, calcMatchTimerID ):
		"""
		通知客户端请求成功
		"""
		self.calcMatchTime = calcMatchTime
		self.calcMatchTimerID = calcMatchTimerID
		self.playerObj.playerMB.fastTeamOnjoin( self.spaceScriptID )
		self.playerObj.playerMB.notifyClientFastTeamSignUp(self.spaceScriptID,calcMatchTime)
		self.playerObj.playerMB.cell.fastTeamOnjoin()

	def quitSignUp( self,mgr ):
		"""
		取消
		"""
		self.playerObj.playerMB.notifyClientFastTeamCancelSignUp()
		self.popCalcMatchTimer(mgr)
		self.personFastTeamCancel()
		if hasattr(self.playerObj.playerMB,"cell") and self.playerObj.playerMB.cell:
			self.playerObj.playerMB.cell.fastTeamOnCancel()
	
	def popCalcMatchTimer( self,mgr ):
		"""
		"""
		if self.calcMatchTimerID:
			mgr.delTimer( self.calcMatchTimerID )
			self.calcMatchTimerID = 0

	def personFastTeamCancel( self ):
		"""
		"""
		self.playerObj.playerMB.fastTeamOnCancel()

	def getID( self ):
		return self.playerObj.playerMB.id

	def getAllPlayerMB( self ):
		return [self.playerObj.playerMB]

	def getPlayerNum( self ):
		"""
		获得总人数
		"""
		return 1

	def isItemPlayer( self, playerID ):
		"""
		判断是否为该玩家
		"""
		return self.playerObj.playerMB.id == playerID

	def matchFailure( self,mgr ):
		"""
		匹配失败
		"""
		self.quitSignUp(mgr)
		self.playerObj.playerMB.client.statusMessage( csstatus.FAST_TEAM_REQ_TEAM_FAILURE,"" )

	def setTeamSearchTime( self, calcMatchTime ):
		"""
		"""
		self.playerObj.playerMB.client.CLIENT_OnSetTeamSearchTime( int(calcMatchTime) )

class ReqTeamInfos( ReqBase ):
	"""
	队伍匹配类
	"""
	_type = REQ_OBJ_TYPE_TEAM
	def __init__( self, teamMB, memberDataList,  spaceScriptID, timeID ):
		self.teamMB = teamMB
		self.spaceScriptID = spaceScriptID
		self.matchTimeID = timeID
		self.reqTeamTime = time.time()
		self.memberList = []
		self.calcMatchTime = 0
		self.calcMatchTimerID = 0
		for memberData in memberDataList:
			self.memberList.append( PlayerData( memberData["playerMB"], memberData["playerDBID"], memberData["level"], memberData["name"] ) )

	def getID( self ):
		return self.teamMB.id

	def getAllPlayerMB( self ):
		return [ member.playerMB for member in self.memberList ]

	def getReqTime( self ):
		return self.reqTeamTime

	def isItemPlayer( self, playerID ):
		"""
		判断玩家是否在匹配列表中
		"""
		return playerID in [member.playerMB.id for member in self.memberList ]

	def getPlayerNum( self ):
		"""
		获得总人数
		"""
		return len( self.memberList )

	def notifyClientFastTeamSignUp( self, calcMatchTime, calcMatchTimerID ):
		"""
		通知客户端请求成功
		"""
		self.calcMatchTime = calcMatchTime
		self.calcMatchTimerID = calcMatchTimerID
		self.teamMB.fastTeamOnReq( self.spaceScriptID )
		for member in self.memberList:
			member.playerMB.fastTeamOnjoin( self.spaceScriptID )
			member.playerMB.notifyClientFastTeamSignUp(self.spaceScriptID,calcMatchTime)
			member.playerMB.cell.fastTeamOnjoin()

	def quitSignUp( self,mgr ):
		"""
		取消
		"""
		for member in self.memberList:
			member.playerMB.fastTeamOnCancel()
			member.playerMB.notifyClientFastTeamCancelSignUp()
			if hasattr(member.playerMB,"cell") and member.playerMB.cell:
				member.playerMB.cell.fastTeamOnCancel()
		self.popCalcMatchTimer(mgr)
		self.teamCancelFastTeam()

	def popCalcMatchTimer( self,mgr ):
		"""
		"""
		if self.calcMatchTimerID:
			mgr.delTimer( self.calcMatchTimerID )
			self.calcMatchTimerID = 0

	def teamCancelFastTeam( self ):
		"""
		"""
		self.teamMB.fastTeamOnCancel()

	def memberLeave( self, memberMailBox ):
		"""
		成员离开
		"""
		for mem in self.memberList:
			if mem.playerMB.id == memberMailBox.id:
				self.memberList.remove( mem )
				memberMailBox.notifyClientFastTeamCancelSignUp()
				break

	def memberLogin( self, memberMailBox, memberDBID ):
		"""
		成员登录
		"""
		for mem in self.memberList:
			if mem.playerDBID == memberDBID:
				mem.playerMB = memberMailBox
				break

	def memberJoin( self, playerMB, playerName, playerDBID, playerLevel ):
		"""
		增加成员
		"""
		self.memberList.append(PlayerData( playerMB, playerDBID, playerLevel, playerName))
		playerMB.notifyClientFastTeamSignUp(self.spaceScriptID,self.calcMatchTime)

	def matchFailure( self, mgr ):
		"""
		匹配失败
		"""
		self.quitSignUp(mgr)
		for mem in self.memberList:
			mem.playerMB.client.statusMessage( csstatus.FAST_TEAM_REQ_TEAM_FAILURE,"" )

	def setTeamSearchTime( self, calcMatchTime ):
		"""
		"""
		for mem in self.memberList:
			mem.playerMB.client.CLIENT_OnSetTeamSearchTime( int(calcMatchTime) )

class MatchObj( object ):
	"""
	一个匹配战队
	"""
	def __init__( self, mgr,spaceScriptID,reqObjList ):
		self.teamMB = None
		self.spaceScriptID = spaceScriptID
		self.reqObjList = reqObjList
		reqTimeList = [ reqObj.getReqTime() for reqObj in self.reqObjList ]
		self.matchSuccessTime = int(time.time() - min(reqTimeList))
		self.waiteJoinTeamList = []		#等待加入队伍的mailbox列表

		for mailBox in self.getAllPlayerMB():
			if hasattr( mailBox, "client" ) and mailBox.client:
				mailBox.client.FastTeamOnMatchSuccess()

	def isItemPlayer( self, playerID ):
		"""
		是否为该玩家
		"""
		for reqobj in self.reqObjList:
			if reqobj.isItemPlayer( playerID ):
				return True
		return False

	def getAllPlayerMB( self ):
		"""
		获得所有玩家MailBox
		"""
		mailBoxlist = []
		for reqobj in self.reqObjList:
			mailBoxlist.extend( reqobj.getAllPlayerMB() )
		return mailBoxlist

	def doOnMatch( self, mgr ):
		"""
		匹配成功后操作
		"""
		for reqobj in self.reqObjList:
			mgr.fastTeam_popReq( self.spaceScriptID,reqobj )
			if reqobj.getType() == REQ_OBJ_TYPE_TEAM:
				reqobj.teamCancelFastTeam()
			else:
				reqobj.personFastTeamCancel()

		self.createTeam()

	def createTeam( self ):
		"""
		创建一支队伍
		"""
		allPlayerMBList = self.getAllPlayerMB()
		if not len(allPlayerMBList):
			return

		for playerMB in allPlayerMBList:
			if playerMB.id != allPlayerMBList[0].id:
				self.waiteJoinTeamList.append(playerMB)
		#在这里取队长 先暂定第一个
		allPlayerMBList[0].fastTeamCreateTeam( self.spaceScriptID )

	def onCreateTeam( self, captainMB, teamMB ):
		"""
		队伍创建成功
		"""
		allPlayerMBList = self.getAllPlayerMB()
		for mailBox in allPlayerMBList:
			mailBox.fastTeamOnCancel()
			if hasattr(mailBox,"cell") and mailBox.cell:
				mailBox.cell.fastTeamOnCancel()

		self.teamMB = teamMB
		for mb in self.waiteJoinTeamList:
			mb.fastTeamOnJoinTeam(captainMB.id, teamMB)
			
	def onUseCurrTeam(self, captainMB, teamMB):
		"""
		不需要创建队伍，使用当前的队伍
		"""
		allPlayerMBList = self.getAllPlayerMB()
		for mailBox in allPlayerMBList:
			mailBox.fastTeamOnCancel()
			if hasattr(mailBox,"cell") and mailBox.cell:
				mailBox.cell.fastTeamOnCancel()


class FastTeamMgr( MgrPersistentObject.MgrPersistentObject ):
	"""
	快速组队管理类
	"""
	def __init__( self ) :
		MgrPersistentObject.MgrPersistentObject.__init__( self )
		self.reqDict = {}	#所有组队副本申请快速组队的字典 {spaceScriptID:[玩家申请列表]}
		self.matchObjDict = {} #所有组队副本已匹配的字典		
		self.teamMemberMaxNumDict = {} #副本可以组队的最大人数
		self.onCompleteInit()
		
	def setTeamMemberMaxNum(self, spaceScriptID, maxNum):
		"""
		define method
		设置副本可以组队的最大人数
		"""
		self.teamMemberMaxNumDict[spaceScriptID] = maxNum
		
	def fastTeam_reqPerson( self, spaceScriptID,playerMB, playerDBID, level, name ):
		"""
		个人点击快速组队
		"""
		if not spaceScriptID:
			return
		if spaceScriptID in self.reqDict:
			reqList = self.reqDict[spaceScriptID]
			if playerMB.id in [ obj.getID() for obj in reqList]:
				return
		timeID = self.addTimer( MATCH_FAILURE_TIME, 0, MATCH_FAILURE_TIME_ARG )

		reqobj = ReqPersonInfos( playerMB, playerDBID, level, name, spaceScriptID, timeID )
		self.fastTeam_pushReq( reqobj )
		self.fastTeam_tryMatch(spaceScriptID)

	def fastTeam_reqTeam( self, spaceScriptID,playerMB, teamMB, memberDataList):
		"""
		队伍队长点击快速组队
		"""
		if not spaceScriptID:
			return
		if not len(memberDataList):
			return
		if len(memberDataList) == self.teamMemberMaxNumDict[spaceScriptID]: 
			playerMB.statusMessage( csstatus.FAST_TEAM_IS_FULL,"" )
			return
		if len( memberDataList ) > self.teamMemberMaxNumDict[spaceScriptID]:
			playerMB.statusMessage( csstatus.FAST_TEAM_FORBID_MEMBER,"" )
			return
			
		if spaceScriptID in self.reqDict:
			reqList = self.reqDict[spaceScriptID]
			if teamMB.id in [obj.getID() for obj in reqList]:
				#已申请
				return
		timeID = self.addTimer( MATCH_FAILURE_TIME, 0, MATCH_FAILURE_TIME_ARG )
		reqobj = ReqTeamInfos( teamMB,memberDataList,spaceScriptID, timeID )
		teamMB.setFastTeamMaxMemberNum(self.teamMemberMaxNumDict[spaceScriptID])
		self.fastTeam_pushReq( reqobj )
		self.fastTeam_tryMatch( spaceScriptID )

	def fastTeam_perSonCancelSignUp( self, spaceScriptID, playerID ):
		"""
		取消快速组队
		"""
		if spaceScriptID not in self.reqDict:
			return
		for reqobj in self.reqDict[spaceScriptID]:
			if reqobj and reqobj.getType() == REQ_OBJ_TYPE_PERSON and reqobj.getID() == playerID:
				reqobj.quitSignUp(self)  
				self.fastTeam_popReq( spaceScriptID,reqobj )
				break

	def fastTeam_teamCancelSignUp( self, spaceScriptID, teamID ):
		"""
		取消快速组队
		"""
		if spaceScriptID not in self.reqDict:
			return
		for reqobj in self.reqDict[spaceScriptID]:
			if reqobj and reqobj.getType() == REQ_OBJ_TYPE_TEAM and reqobj.getID() == teamID:
				reqobj.quitSignUp(self)  
				self.fastTeam_popReq( spaceScriptID,reqobj )
				break

	def fastTeam_pushReq( self, reqobj ):
		"""
		压入请求列表
		"""
		if reqobj.spaceScriptID not in self.reqDict:
			self.reqDict[reqobj.spaceScriptID] = []
		self.reqDict[reqobj.spaceScriptID].append(reqobj)

		calcMatchTime = CALC_MATCH_SUCCESS_TIME
		if reqobj.spaceScriptID in self.matchObjDict:
			if len( self.matchObjDict[reqobj.spaceScriptID] ):
				matchList = self.matchObjDict[reqobj.spaceScriptID]
				matchobj = matchList[len(matchList) - 1]
				calcMatchTime = matchobj.matchSuccessTime

		timeID = self.addTimer(0.1,RE_CALC_MATCH_TIME,RE_CALC_MATCH_TIME_ARG)
		reqobj.notifyClientFastTeamSignUp(calcMatchTime,timeID)

	def fastTeam_popReq( self, spaceScriptID,reqobj ):
		"""
		弹出请求列表
		"""
		if spaceScriptID not in self.reqDict:
			return
		reqobj.popCalcMatchTimer(self)
		for item in self.reqDict[spaceScriptID]:
			if item.getID() == reqobj.getID():
				self.reqDict[spaceScriptID].remove( item )
				break

	def fastTeam_tryMatch( self, spaceScriptID ):
		"""
		尝试匹配某个副本的队伍
		"""
		reqObjList = self.reqDict[spaceScriptID]
		maxNum = self.teamMemberMaxNumDict[spaceScriptID]
		matchIndexs = self.getMatchReqObjIndexs(reqObjList, maxNum)
		if matchIndexs:
			matchObj = MatchObj( self,spaceScriptID,[reqObjList[index] for index in matchIndexs] )
			self.fastTeam_pushMatch( spaceScriptID, matchObj )
			matchObj.doOnMatch(self)

	def getMatchReqObjIndexs( self, reqList, maxNum ):
		"""
		获取一组报名小队中能组成多人战队的小队的index
		"""
		Num = maxNum
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


	def fastTeam_pushMatch( self, spaceScriptID ,matchObj ):
		"""
		压入已匹配列表
		"""
		if spaceScriptID not in self.matchObjDict:
			self.matchObjDict[spaceScriptID] = []
		self.matchObjDict[spaceScriptID].append( matchObj )

	def fastTeam_onCreateTeam( self, spaceScriptID,captainMB, teamMB ):
		"""
		创建队伍回调
		"""
		if spaceScriptID not in self.matchObjDict:
			return
		for matchObj in self.matchObjDict[spaceScriptID]:
			if matchObj and matchObj.isItemPlayer( captainMB.id ):
				teamMB.setFastTeamMaxMemberNum(self.teamMemberMaxNumDict[spaceScriptID])
				matchObj.onCreateTeam( captainMB, teamMB )
				self.matchObjDict[spaceScriptID].remove(matchObj)
				break
				
	def fastTeam_onUseCurrTeam(self, spaceScriptID,captainMB, teamMB):
		"""
		不需要创建队伍，使用当前的队伍
		"""
		if spaceScriptID not in self.matchObjDict:
			return
		for matchObj in self.matchObjDict[spaceScriptID]:
			if matchObj and matchObj.isItemPlayer( captainMB.id ):
				matchObj.onUseCurrTeam( captainMB, teamMB )
				self.matchObjDict[spaceScriptID].remove(matchObj)
				break

	def fastTeam_OnMemberLeave( self, teamMB, spaceScriptID, memberMailBox ):
		"""
		队伍人数变动，取消申请
		"""
		if spaceScriptID not in self.reqDict:
			return
		teamReqList = [ reqObj for reqObj in self.reqDict[spaceScriptID] if reqObj.getType() == REQ_OBJ_TYPE_TEAM and reqObj.getID() == teamMB.id ]
		if len(teamReqList):
			reqobj = teamReqList[0]
			reqobj.memberLeave( memberMailBox )

	def fastTeam_OnMemberLogin( self, teamMB, spaceScriptID, memberMailBox, memberDBID ):
		"""
		玩家下线
		"""
		if spaceScriptID not in self.reqDict:
			return
		teamReqList = [ reqObj for reqObj in self.reqDict[spaceScriptID] if reqObj.getType() == REQ_OBJ_TYPE_TEAM and reqObj.getID() == teamMB.id ]
		if len(teamReqList):
			reqobj = teamReqList[0]
			reqobj.memberLogin( memberMailBox, memberDBID )

	def fastTeam_OnTeamDisband( self, teamMB, spaceScriptID ):
		"""
		队伍解散
		"""
		if spaceScriptID not in self.reqDict:
			return
		teamReqList = [ reqObj for reqObj in self.reqDict[spaceScriptID] if reqObj.getType() == REQ_OBJ_TYPE_TEAM and reqObj.getID() == teamMB.id ]
		if len(teamReqList):
			reqobj = teamReqList[0]
			reqobj.quitSignUp( self )  
			self.fastTeam_popReq( spaceScriptID,reqobj )

	def fastTeam_OnMemberJoin( self, teamMB, spaceScriptID, playerMB, playerName, playerDBID, playerLevel ):
		"""
		队伍增加人员
		"""
		if spaceScriptID not in self.reqDict:
			return
		teamReqList = [ reqobj for reqobj in self.reqDict[spaceScriptID] if reqobj.getType() == REQ_OBJ_TYPE_TEAM and reqobj.getID() == teamMB.id ]
		if len(teamReqList):
			reqobj = teamReqList[0]
			if reqobj.isItemPlayer(playerMB.id):
				return
			reqobj.memberJoin( playerMB, playerName, playerDBID, playerLevel )
			self.fastTeam_tryMatch( spaceScriptID )

	def fastTeam_matchFastTeamOnJoinTeam( self, spaceScriptID, playerMB, teamMB, memberDataList ):
		"""
		匹配时加入队伍
		"""
		if not spaceScriptID:
			return
		if not len( memberDataList ):
			return
		timeID = 0
		if spaceScriptID in self.reqDict:	
			for reqobj in self.reqDict[spaceScriptID]:
				if reqobj and reqobj.getType() == REQ_OBJ_TYPE_PERSON and reqobj.getID() == playerMB.id:
					timeID = reqobj.matchTimeID
					reqobj.personFastTeamCancel()
					self.fastTeam_popReq( spaceScriptID,reqobj )

		reqobj = ReqTeamInfos( teamMB,memberDataList,spaceScriptID,timeID )
		self.fastTeam_pushReq( reqobj )
		self.fastTeam_tryMatch( spaceScriptID )

	def onTimer( self, id, userArg ):
		"""
		"""
		if userArg == MATCH_FAILURE_TIME_ARG:
			for spaceScriptID,reqObjList in self.reqDict.items():
				for reqObj in reqObjList:
					if reqObj.matchTimeID == id:
						self.fastTeam_popReq( spaceScriptID, reqObj )
						reqObj.matchFailure(self)
						break
				break
		elif userArg == RE_CALC_MATCH_TIME_ARG:
			for spaceScriptID,reqObjList in self.reqDict.items():
				for reqObj in reqObjList:
					calcMatchTime = CALC_MATCH_SUCCESS_TIME
					if reqObj.calcMatchTimerID == id and reqObj.spaceScriptID in self.matchObjDict:
						if len( self.matchObjDict[reqObj.spaceScriptID] ):
							matchList = self.matchObjDict[reqObj.spaceScriptID]
							matchobj = matchList[len(matchList) - 1]
							calcMatchTime = matchobj.matchSuccessTime
					reqObj.setTeamSearchTime( calcMatchTime )
					break
				break
						

