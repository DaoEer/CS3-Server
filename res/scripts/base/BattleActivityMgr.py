#-*- coding:utf-8 -*-



from functools import reduce

import KBEngine

import KST
import csstatus
import KBEDebug
import csdefine
import HotConst
from CoreObject import MgrPersistentObject
from ConfigObject.Crond.CrondDatas import CrondDatas
g_CrondDatas = CrondDatas.instance()


MATCH_FAILURE_TIME = 180	#匹配失败的时间
MATCH_TIME_OUT_ARG = 30		#匹配超过3分钟参数
TIMER_ARG_TELEPORT = 40		#传送等待倒计时参数

TELEPORT_DELAY = 3.0 #传送倒计时

# 活动副本名
SPACE_COPY_NAME = {
	csdefine.ACTIVITY_TYPE_CAMP_YCJMD		:	"fu_ben_L_YCJMD_zhenyingPVP",
	csdefine.ACTIVITY_TYPE_CAMP_LING_MAI	:	"fu_ben_L_LMZC",
}

MEMBER_TYPE_SINGLE = 1
MEMBER_TYPE_TEAM = 2

class Member:
	def __init__(self, type, activityType, level, num):
		self._type = type
		self.level = level
		self.num = num
		self.matchTimerID = 0
		self.activityType = activityType

	def getType(self):
		return self._type

	def getLevel(self):
		return self.level

	def getNum(self):
		return self.num

	def getActivityType(self):
		return self.activityType

	def setMatchTimerID(self, matchTimerID):
		self.matchTimerID = matchTimerID
	
class Single(Member):
	def __init__(self, activityType, playerBase, playerDBID, level):
		Member.__init__(self, MEMBER_TYPE_SINGLE, activityType, level, 1)
		self.playerBase = playerBase
		self.playerDBID = playerDBID
		
	def getPlayerID(self):
		return self.playerBase.id

	def hasPlayerID(self, playerID):
		return playerID == self.playerBase.id

	def getPlayerBaseList(self):
		return [self.playerBase]

	def getPlayerDBIDs(self):
		return [self.playerDBID]

class Team(Member):
	def __init__(self, activityType, teamMB, memberDatas, level):
		Member.__init__(self, MEMBER_TYPE_TEAM, activityType, level, len(memberDatas))
		self.teamMB = teamMB
		self.playerDatas = []
		for data in memberDatas:
			params = {}
			params["playerBase"] = data["playerBase"]
			params["playerDBID"] = data["playerDBID"]
			self.playerDatas.append(params)

	def getTeamMB(self):
		return self.teamMB

	def getTeamID(self):
		return self.teamMB.id

	def getPlayerBaseList(self):
		return [data['playerBase'] for data in self.playerDatas]

	def getPlayerDBIDs(self):
		return [data['playerDBID'] for data in self.playerDatas]

	def hasPlayerID(self, playerID):
		return playerID in [data['playerBase'].id for data in self.playerDatas]
	
	def getPlayerDBIDs(self):
		return [data['playerDBID'] for data in self.playerDatas]

class CampItem:
	def __init__(self, memberList, camp=0):
		self.camp = camp
		self.memberList = memberList

	def getCamp(self):
		return self.camp

	def getMemberList(self):
		return self.memberList


class MatchItem:
	"""
	大荒战场游戏匹配对象
	"""
	def __init__(self, activityType, level, campItems):
		#分两边势力
		self.campItems = campItems
		self.enterSpaceTimerID= 0 #进图定时器timerID
		self.level = level
		self.activityType = activityType
	
	def getCampItem(self, camp):
		for item in self.campItems:
			if item.getCamp() == camp:
				return item

	def getCampItems(self):
		return self.campItems

	def getLevel(self):
		return self.level

	def getActivityType(self):
		return self.activityType

	def setEnterSpaceTimerID(self, timerID):
		self.enterSpaceTimerID = timerID

	def getEnterSpaceTimerID(self):
		return self.enterSpaceTimerID

class MatchMgr:
	"""
	"""
	def __init__(self):
		self.members = []
		self.matchItems = []

	def addMember(self, member):
		self.members.append(member)

	def removeMember(self, member):
		if member in self.members:
			self.members.remove(member)

	def addMatchItem(self, matchItem):
		self.matchItems.append(matchItem)

	def removeMatchItem(self, matchItem):
		if matchItem in self.matchItems:
			self.matchItems.remove(matchItem)

	def getMembersByLevel(self, activityType, level):
		members = []
		for m in self.members:
			if m.getActivityType() == activityType and m.getLevel() == level:
				members.append(m)
		return members

	def getMemberByPlayerID(self, playerID):
		for m in self.members:
			if m.hasPlayerID(playerID):
				return m
		return None

	def getMemberByTeamID(self, teamID):
		for m in self.members:
			if m.getType() == MEMBER_TYPE_TEAM and m.getTeamID() == teamID:
				return m
		return None

	def getMatchItem(self, activityType, level, maxNum, members):
		#获取匹配
		memberList1 = self.getCampMemberList(maxNum, members)
		if memberList1:
			for member in memberList1:
				members.remove(member)

			memberList2 = self.getCampMemberList(maxNum, members)
			if memberList2:
				campItem1 = CampItem(memberList1, csdefine.CAMP_TAOSIM)
				campItem2 = CampItem(memberList2, csdefine.CAMP_DEMON)

				matchItem = MatchItem(activityType, level, [campItem1, campItem2])
				
				
				return matchItem
		return None

	def getCampMemberList(self, maxNum, members):
		#获取阵营成员列表
		#按人数分堆
		if not len(members):
			return []

		matchData = {} 
		for m in members:
			key = m.getNum()
			if key not in matchData:
				matchData[key]=[]
			matchData[key].append(m)
		keys = []
		for k,v in matchData.items():
			keys.append((k,len(v)))
		result = self.getMatchResult(maxNum, keys)
		memberList = []
		for key, num in result:
			for i in range(num):
				memberList.append(matchData[key].pop(0))
		return memberList

	def getMatchData(self, members):
		"""
		获取匹配数据
		"""
		data = {} #按人数分堆
		for m in members:
			key = m.getNum()
			if key not in data:
				data[key]=[]
			data[key].append(m)

		return data

	def getMatchResult(self, maxNum, keys, index=0, result=None):
		#获取匹配的结果 如果返回的不是空列表，表示找到了一个阵营的玩家
		if result == None:
			result = []
		if index >= len(keys):
			return result

		key, num = keys[index]
		for i in range(num+1):
			result.append((key, i))
			result = self.getMatchResult(maxNum, keys, index+1, result)
			if reduce(lambda x,y: x+y[0]*y[1], result, 0) == maxNum:
				break
			result.remove((key, i))
		return result

class BattleActivityMgr(MgrPersistentObject.MgrPersistentObject):
	"""
	战场活动管理器
	"""
	def __init__(self):
		MgrPersistentObject.MgrPersistentObject.__init__(self)
		self.regist()
		self._activityState  = False	#是否开启活动
		self.matchMgr = MatchMgr()
		self.onCompleteInit()

	def regist(self):
		"""
		注册
		"""
		taskEvents = { "BattleActivityMgr_Notice":"onActiveNotice",
						"BattleActivityMgr_Start":"onActiveStart",
						"BattleActivityMgr_End":"onActiveEnd"
		 }
		for taskName, callbackName in taskEvents.items():
			for scriptID, cmd in g_CrondDatas.getCrondTaskCmds(taskName):
		 		KBEngine.globalData["CrondManager"].addScheme( scriptID, cmd, self, callbackName, -1,() )


	def onActiveNotice( self, cmd ):
		"""
		活动公告
		"""
		KST.g_baseAppEntity.globalWold( csstatus.ACTIVITY_CAMP_LING_MAI_NOTICE, "" )

	def onActiveStart( self, cmd ):
		"""
		活动开始
		"""
		self._activityState = True
		KST.g_baseAppEntity.globalWold( csstatus.ACTIVITY_CAMP_LING_MAI_START, "" )
		
	def onActiveEnd( self, cmd ):
		"""
		活动结束
		"""
		self._activityState = False
		KST.g_baseAppEntity.globalWold( csstatus.ACTIVITY_CAMP_LING_MAI_END, "" )


	def signUpSingle(self, activityType, playerBase, playerDBID, level):
		"""
		个人申请
		"""
		if not self._activityState:
			playerBase.statusMessage(csstatus.SPACECOPY_CAMP_YXLM_NOT_START,"")
			return
		member = Single(activityType, playerBase, playerDBID, level)
		self.signUp(member, activityType, level)
			
	def signUpTeam( self, activityType, playerBase, teamMB, memberDataList, level ):
		"""
		队伍申请
		"""
		if not len(memberDataList):
			return
		if not self._activityState:
			playerBase.statusMessage( csstatus.SPACECOPY_CAMP_YXLM_NOT_START,"")
			return
		member = Team(activityType, teamMB, memberDataList, level)
		teamMB.setIsReqBattle(True)
		self.signUp(member, activityType, level)


	def signUp(self, member, activityType, level):
		"""
		报名
		"""
		self.matchMgr.addMember(member)
		member.setMatchTimerID(self.addTimer(MATCH_FAILURE_TIME, 0, MATCH_TIME_OUT_ARG))
		playerBaseList = member.getPlayerBaseList()
		for playerBase in playerBaseList:
			playerBase.battleActivitySignUp()
			if playerBase.client:
				playerBase.client.OnBattleMatchStart()
		
		self.match(activityType, level)

	def match(self, activityType, level):
		"""
		匹配
		"""
		members = self.matchMgr.getMembersByLevel(activityType, level)
		maxNum = HotConst.MATCH_NUMBER[activityType]
		matchItem = self.matchMgr.getMatchItem(activityType, level, maxNum, members)
		if matchItem:
			self.onMatchSucceeded(matchItem)
			
	def onMatchSucceeded(self, matchItem):
		self.matchMgr.addMatchItem(matchItem)
		playerDBIDs = []
		playerBaseList = []
		playerCampInfo = {}
		activityType = matchItem.getActivityType()
		for campItem in matchItem.getCampItems():
			camp = campItem.getCamp()
			for member in campItem.getMemberList():
				#从排队列表中移除
				self.matchMgr.removeMember(member)
				dbids = member.getPlayerDBIDs()
				#记录阵营信息
				for dbid in dbids:
					playerCampInfo[dbid] = camp
			
				playerDBIDs.extend(dbids)

				baseList = member.getPlayerBaseList()
				playerBaseList.extend(baseList)
				for playerBase in baseList:
					if playerBase.client:
						playerBase.client.ShowEnterRandomFitTime(TELEPORT_DELAY)

		spaceParams = {}
		spaceParams["spaceKey"] = SPACE_COPY_NAME[activityType]
		spaceParams["belongType"] = csdefine.SPACE_BELONG_NORMAL
		spaceParams["playerDBIDs"] = playerDBIDs
		spaceParams["packSpaceLevel"] = matchItem.getLevel()//10 * 10 + 5
		spaceParams["playerCampInfo"] = playerCampInfo
		KBEngine.globalData["SpaceManager"].remoteCallDomain( SPACE_COPY_NAME[activityType], "requestNewSpace",(spaceParams,))
		matchItem.setEnterSpaceTimerID(self.addTimer(TELEPORT_DELAY, 0, TIMER_ARG_TELEPORT))
		

	def onCancelSignUp(self, member, message):
		self.matchMgr.removeMember(member)
		if member.getType()==MEMBER_TYPE_TEAM:
			member.getTeamMB().setIsReqBattle(False)
		playerBaseList = member.getPlayerBaseList()
		for playerBase in playerBaseList:
			playerBase.battleActivitySignOut()
			playerBase.statusMessage( message, "" )
			if playerBase.client:
				playerBase.client.OnCampRandomFitInterrupt()


	def cancelSignUp( self, playerMB ):
		"""
		取消随机匹配
		"""
		member = self.matchMgr.getMemberByPlayerID(playerMB.id)
		self.onCancelSignUp(member, csstatus.CAMP_RANDOM_FIT_CANCEL)

	
	def onTeamChange( self, teamMB ):
		"""
		队伍人数变动，取消申请
		"""
		member = self.matchMgr.getMemberByTeamID(teamMB.id)
		if not member:
			return
		self.onCancelSignUp(member, csstatus.CAMP_RANDOM_FIT_LEAVE)

	def onJoinTeam( self, playerMB ):
		"""
		加入队伍，取消申请
		"""
		member = self.matchMgr.getMemberByPlayerID(playerMB.id)
		self.onCancelSignUp(member, csstatus.CAMP_RANDOM_FIT_CANCEL)

	def onPlayerLoginOff(self, playerMB):
		"""
		玩家下线
		"""
		member = self.matchMgr.getMemberByPlayerID(playerMB.id)
		self.onCancelSignUp(member, csstatus.CAMP_RANDOM_FIT_MEB_OFFLINE)

		# 自动离开队伍
		playerMB.leaveTeamFB(playerMB.id)
		
	def onTimer(self, id, userArg):
		"""
		addTimer回调函数
		"""
		if userArg == MATCH_TIME_OUT_ARG:
			return
		elif userArg == TIMER_ARG_TELEPORT:
			for matchItem in self.matchMgr.matchItems:
				if matchItem.getEnterSpaceTimerID() == id:
					self.teleportToSpace(matchItem)
					return

	def teleportToSpace(self, matchItem):
		"""
		传送玩家
		"""
		activityType = matchItem.getActivityType()
		spaceObj = KST.g_objFactory.getSpaceObject( SPACE_COPY_NAME[activityType] )
		for item in matchItem.getCampItems():
			pos,direction = spaceObj.getEnterPos(item.getCamp())
			for member in item.getMemberList():
				if member.getType() == MEMBER_TYPE_TEAM:
					member.getTeamMB().setIsReqBattle(False)
				for playerBase in member.getPlayerBaseList():
					playerBase.battleActivitySignOut()
					playerBase.cell.campFitTeleport( SPACE_COPY_NAME[activityType], pos, direction )

		self.matchMgr.removeMatchItem(matchItem)