# -*- coding: utf-8 -*-

import random
import KBEDebug
import Math
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
import Const

REQ_OBJ_TYPE_PERSON		= 1
REQ_OBJ_TYPE_TEAM		= 2

TIMER_ARG_AFFIRM_WRITE 	= 30
TIMER_ARG_TELEPORT		= 10

SPACE_COPY_CLASS_NAME = "fu_ben_L_YXWZ"

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
	def __init__( self, playerMB, playerDBID, camp, level, name ):
		self.playerObj = PlayerData( playerMB,playerDBID,camp,level,name )
		self.level = level
		self.camp = camp
		self.name = name

	def nofityClientSignup( self ):
		self.playerObj.playerMB.campYXLMOnJoin()
		self.playerObj.playerMB.client.CLIENT_CampYXLMSignUpSuccess()

	def getDictToClient( self ):
		"""
		打包数据发给客户端
		"""
		return [ self.playerObj.getDictToClient() ]

	def getAllPlayerDBID( self ):
		"""
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
		return [ self.playerObj.playerMB ]

	def quitSignUp( self ):
		"""
		退出报名
		"""
		self.playerObj.playerMB.campYXLMOnQuit()
		self.playerObj.playerMB.statusMessage(csstatus.SPACECOPY_CAMP_YXLM_CANCEL_SIGNUP,"")

	def onMatch( self ):
		"""
		匹配成功
		"""
		self.playerObj.playerMB.client.CLIENT_CampYXLMOnMatchSuccess()

	def upAffirmInfos( self, waitList ):
		"""
		发送等待确认的列表
		"""
		self.playerObj.playerMB.client.CLIENT_CampYXLMUpdateWaitAffirmList( waitList )

class ReqTeamInfos( ReqBase ):
	"""
	队伍匹配类
	"""
	_type = REQ_OBJ_TYPE_TEAM
	def __init__( self, teamMB, memberDataList, camp, level ):
		self.teamMB = teamMB
		self.camp = camp
		self.level = level
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
		"""
		memberDBIDList = []
		for member in self.memberList:
			memberDBIDList.append( member.playerDBID )
		return memberDBIDList

	def nofityClientSignup( self ):
		self.teamMB.setIsReqCopyCampYXLM(True)
		for member in self.memberList:
			member.playerMB.campYXLMOnJoin()
			member.playerMB.client.CLIENT_CampYXLMSignUpSuccess()

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
		return [ member.playerMB for member in self.memberList ]

	def quitSignUp( self ):
		"""
		退出报名
		"""
		for member in self.memberList:
			member.playerMB.campYXLMOnQuit()
			member.playerMB.statusMessage( csstatus.SPACECOPY_CAMP_YXLM_CANCEL_SIGNUP,"" )

	def onMatch( self ):
		"""
		匹配成功
		"""
		for member in self.memberList:
			member.playerMB.client.CLIENT_CampYXLMOnMatchSuccess()

	def upAffirmInfos( self, waitList ):
		"""
		发送等待确认的列表
		"""
		for member in self.memberList:
			member.playerMB.client.CLIENT_CampYXLMUpdateWaitAffirmList( waitList )
		if len( waitList ) == 0:
			self.teamMB.setIsReqCopyCampYXLM(False)

class MatchObj( object ):
	"""
	一个匹配战队
	"""
	def __init__( self, camp, reqObjList ):
		self.camp = camp
		self.teamMB = None
		self.reqObjList = reqObjList
		self.affirmList = []			#已确认的玩家ID列表
		self.waiteJoinTeamList = []		#等待加入队伍的mailbox列表
		self.joinTeamList = []			#已加入队伍的mailBox列表

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

	def isAllAffirm( self ):
		"""
		是否所有玩家都已确认
		"""
		return len(self.getWaitAffirmList()) == 0

	def upAffirmInfos( self, waitList ):
		"""
		发送等待确认的列表
		"""
		for reqObj in self.reqObjList:
			reqObj.upAffirmInfos( waitList )

	def doOnMatch( self, mgr ):
		"""
		执行匹配完后的工作
		"""
		for reqObj in self.reqObjList:
			mgr.yingXiong_popReq(reqObj)
			reqObj.onMatch()

	def onPlayerAffirm( self, playerMB ):
		"""
		某玩家确认
		"""
		self.affirmList.append(playerMB.id)

	def onPlayerCancelAffirm( self, mgr, playerMB, playerName ):
		"""
		某玩家取消确认
		"""
		for playerMailbox in self.getAllPlayerMB():
			playerMailbox.campYXLMOnQuit()
			if hasattr(playerMailbox, "client") and playerMailbox.client:
				playerMailbox.client.CLIENT_CampYXLMHideAffirmWindow() #隐藏确认框

		for reqObj in self.reqObjList:
			if not reqObj.isItemPlayer( playerMB.id ):
				mgr.yingXiong_pushReq( reqObj )
				for playerMailbox in reqObj.getAllPlayerMB():
					playerMailbox.statusMessage( csstatus.SPACECOPY_CAMP_YXLM_CANCEL_AFFIRM, playerName )

			else:
				if reqObj.getType() == REQ_OBJ_TYPE_TEAM:
					reqObj.teamMB.setIsReqCopyCampYXLM(False)
					for playerMailbox in reqObj.getAllPlayerMB():
						if playerMailbox.id != playerMB.id:
							playerMailbox.statusMessage( csstatus.SPACECOPY_CAMP_YXLM_TEAMMEMBER_CANCEL_AFFIRM,playerName )

	def onEnemyTeamCancelAffirm( self, mgr ):
		"""
		敌方战队玩家取消确认
		"""
		for playerMB in self.getAllPlayerMB():
			playerMB.campYXLMOnQuit()
			playerMB.client.CLIENT_CampYXLMHideAffirmWindow()

		for reqObj in self.reqObjList:
			mgr.yingXiong_pushReq(reqObj)

	def affirmFailure( self, mgr ):
		"""
		时间到达，没有全部确认
		"""
		waitList = self.getWaitAffirmList()
		for reqObj in self.reqObjList:
			allAffirm = True
			for playerMB in reqObj.getAllPlayerMB():
				playerMB.campYXLMOnQuit()
				playerMB.client.CLIENT_CampYXLMHideAffirmWindow()
				if playerMB.id in waitList:
					allAffirm = False
					#接收限时惩罚

			if allAffirm:
				mgr.yingXiong_pushReq( reqObj )
			else:
				if reqObj.getType() == REQ_OBJ_TYPE_TEAM:
					reqObj.teamMB.setIsReqCopyCampYXLM(False)
					for playerMB in reqObj.getAllPlayerMB():
						if playerMB.id not in writeAffirmList:
							playerMB.statusMessage( csstatus.SPACECOPY_CAMP_YXLM_MEM_CONFIRM_FAILURE,"")

	def createTeam( self, matchItem, mgr ):
		"""
		创建队伍
		"""
		# if len( self.reqObjList ) == 1 and self.reqObjList[0]._type == REQ_OBJ_TYPE_TEAM:
		# 	self.teamMB = self.reqObjList[0].teamMB
		# 	self.teamMB.setIsReqCopyCampYXLM(True)
		# 	matchItem.onMatchObjCreateTeam(mgr)
		# else:
		captainMB = None
		for playerMB in self.getAllPlayerMB():
			if playerMB.id == self.affirmList[0]: #指定第一个确认的玩家为队长
				captainMB = playerMB
			else:
				self.waiteJoinTeamList.append(playerMB)
		if captainMB:
			captainMB.campYXLMCreateTeam()

	def onCreateTeam( self, matchItem, mgr, captainMB, teamMB ):
		"""
		队伍创建成功
		"""
		self.teamMB = teamMB
		for mb in self.waiteJoinTeamList:
			mb.campYXLMJoinTeam( captainMB.id, self.teamMB )
		
	def onMemberJoinTeam( self, matchItem,playerMB, mgr):
		"""
		队伍加入成功
		"""
		self.joinTeamList.append( playerMB )

	def isAllMemeberJoinTeam( self ):
		"""
		"""
		return len(self.joinTeamList) == len(self.waiteJoinTeamList)

	def onTeamChange( self, mgr, teamID ):
		"""
		此战队中的某个队伍改变了
		"""
		for playerMB in self.getAllPlayerMB():
			playerMB.campYXLMOnQuit()
			playerMB.client.CLIENT_CampYXLMHideAffirmWindow()

		for reqObj in self.reqObjList:
			if reqObj.getType() == REQ_OBJ_TYPE_TEAM and reqObj.getID() == teamID:
				pass
			else:
				mgr.yingXiong_pushReq( reqObj )
				for playerMB in reqObj.getAllPlayerMB():
					playerMB.statusMessage( csstatus.SPACECOPY_CAMP_YXLM_TEAM_CHANGE,"" )


	def onEnemyTeamChange( self, mgr ):
		"""
		敌对战队的某个队伍改变了
		"""
		for playerMB in self.getAllPlayerMB():
			playerMB.campYXLMOnQuit()
			playerMB.client.CLIENT_CampYXLMHideAffirmWindow()
			playerMB.statusMessage( csstatus.SPACECOPY_CAMP_YXLM_ENEMY_TEAM_CHANGE,"" )
		
		for reqObj in self.reqObjList:
			mgr.yingXiong_pushReq( reqObj )

	def onMatchTeamChange( self ):
		"""
		"""
		for playerMB in self.getAllPlayerMB():
			playerMB.campYXLMOnQuit()
			playerMB.client.CLIENT_CampYXLMHideAffirmWindow()
			playerMB.statusMessage( csstatus.SPACECOPY_CAMP_YXLM_MATCH_ITEM_CHANGE,"" )

		self.teamMB.setIsReqCopyCampYXLM(False)

	def onMatchEnemyTeamChange( self ):
		"""
		"""
		for playerMB in self.getAllPlayerMB():
			playerMB.campYXLMOnQuit()
			playerMB.client.CLIENT_CampYXLMHideAffirmWindow()
			playerMB.statusMessage( csstatus.SPACECOPY_CAMP_YXLM_ENEMY_MATCH_ITEM_CHANGE,"" )

		self.teamMB.setIsReqCopyCampYXLM(False)

	def showEnterYXLMTime( self, time ):
		"""
		"""
		for playerMB in self.getAllPlayerMB():
			playerMB.client.CLIENT_ShowEnterYXLMTime(time)

class MatchItem( object ):
	"""
	一对匹配了的战队
	"""
	def __init__( self, mgr, timerID, objectA, objectB ):
		self.objectA = objectA
		self.objectB = objectB
		self.matchTimeID = timerID
		self.objectA.doOnMatch(mgr)
		self.objectB.doOnMatch(mgr)
		self.enterSpaceTimerID = None

	def setEnterTimer( self, timerID, time ):
		"""
		设置进入副本倒计时
		"""
		self.enterSpaceTimerID = timerID
		self.objectA.showEnterYXLMTime(time)
		self.objectB.showEnterYXLMTime(time)

	def isItemPlayer( self, playerID ):
		"""
		"""
		return self.objectA.isItemPlayer(playerID) or self.objectB.isItemPlayer(playerID)

	def isAllAffirm( self ):
		"""
		是否全部点确认
		"""
		return self.objectA.isAllAffirm() and self.objectB.isAllAffirm()

	def onPlayerAffirm( self, mgr, playerMB, playerName ):
		"""
		玩家点确认
		"""
		if not self.objectA.isItemPlayer(playerMB.id) and not self.objectB.isItemPlayer(playerMB.id):
			return
		
		affirmData = {}
		affirmData["xianTeamData"] = self.objectA.getDictToClient()
		affirmData["moTeamData"] = self.objectB.getDictToClient()
		#发送两队的数据给玩家 "Root":[{},{}....]
		playerMB.client.CLIENT_CampYXLMShowAffirmData( Functions.toJsonString([affirmData]) )

		if self.objectA.isItemPlayer(playerMB.id):
			self.objectA.onPlayerAffirm(playerMB)

		if self.objectB.isItemPlayer(playerMB.id):
			self.objectB.onPlayerAffirm(playerMB)

		#发送等待玩家确认的ID列表给客户端
		waitAffirmList = self.objectA.getWaitAffirmList() + self.objectB.getWaitAffirmList()
		self.objectA.upAffirmInfos( waitAffirmList )
		self.objectB.upAffirmInfos( waitAffirmList )

		if self.isAllAffirm():
			self.onAllAffirm(mgr)

	def onPlayerCancelAffirm( self, mgr, playerMB, playerName ):
		"""
		玩家取消确认
		"""
		if not self.objectA.isItemPlayer(playerMB.id) and not self.objectB.isItemPlayer(playerMB.id):
			return

		if self.objectA.isItemPlayer( playerMB.id ):
			self.objectA.onPlayerCancelAffirm(mgr, playerMB, playerName)
			self.objectB.onEnemyTeamCancelAffirm(mgr)

		if self.objectB.isItemPlayer( playerMB.id ):
			self.objectB.onPlayerCancelAffirm(mgr, playerMB, playerName)
			self.objectA.onEnemyTeamCancelAffirm(mgr)

		mgr.yingXiong_removeMatch(self)

	def affirmFailure( self, mgr ):
		"""
		时间到达，没有全部确认
		"""
		self.objectA.affirmFailure( mgr )
		self.objectB.affirmFailure( mgr )
		mgr.yingXiong_removeMatch( self )

	def onAllAffirm( self, mgr ):
		"""
		全部点了确定
		"""
		self.objectA.createTeam( self, mgr )
		self.objectB.createTeam( self, mgr )

	def onCreateTeam( self, mgr, captainMB, teamMB ):
		"""
		成功创建队伍
		"""
		if self.objectA.isItemPlayer( captainMB.id ):
			self.objectA.onCreateTeam( self, mgr, captainMB, teamMB )
		if self.objectB.isItemPlayer( captainMB.id ):
			self.objectB.onCreateTeam( self, mgr, captainMB, teamMB )

		if self.objectA.isAllMemeberJoinTeam() and self.objectB.isAllMemeberJoinTeam():
			self.onMatchObjCreateTeam(mgr)

	def onMemberJoinTeam( self, mgr, playerMB ):
		"""
		加入队伍的回调
		"""
		if self.objectA.isItemPlayer( playerMB.id ):
			self.objectA.onMemberJoinTeam( self,playerMB,mgr )
		if self.objectB.isItemPlayer( playerMB.id ):
			self.objectB.onMemberJoinTeam( self,playerMB,mgr)

		if self.objectA.isAllMemeberJoinTeam() and self.objectB.isAllMemeberJoinTeam():
			self.onMatchObjCreateTeam(mgr)

	def onMatchObjCreateTeam( self, mgr ):
		"""
		某个战队队伍创建成功
		"""
		if not self.objectA.teamMB or not self.objectB.teamMB:
			return
		spaceParams = {}
		spaceParams["spaceKey"] = SPACE_COPY_CLASS_NAME
		spaceParams["belongType"] = csdefine.SPACE_BELONG_NORMAL
		spaceParams["xianTeamID"] = self.objectA.teamMB.id
		spaceParams["moTeamID"] = self.objectB.teamMB.id
		spaceParams[self.objectA.teamMB.id] = self.objectA.getAllPlayerDBID()
		spaceParams[self.objectB.teamMB.id] = self.objectB.getAllPlayerDBID()
		spaceParams["teamInfos"] = ( self.objectA.teamMB.id, self.objectB.teamMB.id )
		KBEngine.globalData["SpaceManager"].remoteCallDomain( SPACE_COPY_CLASS_NAME, "requestNewSpace",(spaceParams,))
		mgr.yingXiong_removeMatch(self)
		mgr.yingXiong_pushSuccessMath( self )

	def onTeamChange( self, mgr, teamID ):
		"""
		当队伍发生改变
		"""
		if self.objectA.isSelfTeamReqObj( teamID ):
			self.objectA.onTeamChange( mgr, teamID )
			self.objectB.onEnemyTeamChange( mgr )
			mgr.yingXiong_removeMatch( self )

		if self.objectB.isSelfTeamReqObj( teamID ):
			self.objectB.onTeamChange( mgr, teamID )
			self.objectA.onEnemyTeamChange( mgr )
			mgr.yingXiong_removeMatch( self )

	def onMatchTeamChange( self, mgr, teamID ):
		"""
		某个完成确认的战队发生改变
		"""
		if self.objectA.teamMB and self.objectA.teamMB.id == teamID:
			self.objectA.onMatchTeamChange()
			self.objectB.onMatchEnemyTeamChange()
			mgr.yingXiong_removeSuccessMatch( self )

		if self.objectB.teamMB and self.objectB.teamMB.id == teamID:
			self.objectB.onMatchTeamChange()
			self.objectA.onMatchEnemyTeamChange()
			mgr.yingXiong_removeSuccessMatch( self )

	def teleportToCopy( self, mgr ):
		"""
		传送玩家
		"""
		#仙
		pos,direction = self.getEnterInfos( csdefine.CAMP_TAOSIM )
		for playerMB in self.objectA.getAllPlayerMB():
			playerMB.campYXLMOnQuit()
			playerMB.cell.gotoSpace( SPACE_COPY_CLASS_NAME, pos, direction )

		#魔
		pos,direction = self.getEnterInfos( csdefine.CAMP_DEMON )
		for playerMB in self.objectB.getAllPlayerMB():
			playerMB.campYXLMOnQuit()
			playerMB.cell.gotoSpace( SPACE_COPY_CLASS_NAME, pos, direction )

		self.objectA.teamMB.setIsReqCopyCampYXLM(False)
		self.objectB.teamMB.setIsReqCopyCampYXLM(False)

		mgr.yingXiong_removeSuccessMatch( self )

	def getEnterInfos( self, camp ):
		"""
		获取玩家要进入的坐标
		"""
		spaceObj = KST.g_objFactory.getSpaceObject( SPACE_COPY_CLASS_NAME )
		return spaceObj.getEnterPos(camp)


class CampYXLMCopyMgr( MgrPersistentObject.MgrPersistentObject ):
	"""
	英雄联盟 管理类
	"""
	def __init__( self ) :
		MgrPersistentObject.MgrPersistentObject.__init__( self )
		self.register()
		self.yingXiong_reqList = [] 		#所有请求参与的玩家列表
		self.yingXiong_matchItemList = [] 		#所有已匹配的列表
		self.yingXiong_successMathList = []	#已匹配成功的列表
		
		self.yingXiong_state  = False  	#是否开启活动
		self.onCompleteInit()

	def register( self ):
		"""
		注册
		"""
		taskEvents = { "CampYXLMCopyMgr_Notice":"onActiveNotice",
						"CampYXLMCopyMgr_Start":"onActiveStart",
						"CampYXLMCopyMgr_End":"onActiveEnd"
		 }
		for taskName, callbackName in taskEvents.items():
			for scriptID, cmd in g_CrondDatas.getCrondTaskCmds(taskName):
		 		KBEngine.globalData["CrondManager"].addScheme( scriptID, cmd, self, callbackName, -1,() )

	def onActiveNotice( self, cmd, *callbackArgs ):
		"""
		活动公告
		"""
		KST.g_baseAppEntity.globalWold( csstatus.SPACECOPY_CAMP_YXLM_NOTIFY, "" )

	def onActiveStart( self, cmd, *callbackArgs ):
		"""
		活动开始
		"""
		self.yingXiong_state = True
		KST.g_baseAppEntity.globalWold( csstatus.SPACECOPY_CAMP_YXLM_START, "" )

	def onActiveEnd( self, cmd, *callbackArgs ):
		"""
		活动结束
		"""
		self.yingXiong_state = False
		KST.g_baseAppEntity.globalWold( csstatus.SPACECOPY_CAMP_YXLM_END, "" )
		KBEngine.globalData["SpaceManager"].remoteCallDomain( SPACE_COPY_CLASS_NAME,"activityEnd",[] )

	def yingXiong_reqPerson( self, playerMB, playerDBID, camp, level, name ):
		"""
		个人申请
		"""
		if not self.yingXiong_state:
			playerMB.statusMessage(csstatus.SPACECOPY_CAMP_YXLM_NOT_START,"")
			return
		if playerMB.id in [ obj.getID() for obj in self.yingXiong_reqList if obj.getType() == REQ_OBJ_TYPE_PERSON ]:
			playerMB.statusMessage( csstatus.SPACECOPY_CAMP_YXLM_SIGN_UP_ALREADY,"" )
			return
		reqObj = ReqPersonInfos( playerMB, playerDBID, camp, level, name ) 
		self.yingXiong_pushReq( reqObj )
		self.yingXiong_tryMatch()

	def yingXiong_reqTeam( self, playerMB, teamMB, memberDataList, camp, level ):
		"""
		队伍申请
		"""
		if not len(memberDataList):
			return
		if not self.yingXiong_state:
			playerMB.statusMessage( csstatus.SPACECOPY_CAMP_YXLM_NOT_START,"")
			return
		if teamMB.id in [obj.getID() for obj in self.yingXiong_reqList if obj.getType() == REQ_OBJ_TYPE_TEAM ]:
			playerMB.statusMessage( csstatus.SPACECOPY_CAMP_YXLM_SIGN_UP_ALREADY,"" )
			return
		#memberData { "playerMB":玩家BaseMailbox,"playerDBID":玩家DBID,"camp":玩家阵营,"level":玩家等级,"name":玩家的名字 }
		reqObj = ReqTeamInfos( teamMB, memberDataList, camp, level )
		self.yingXiong_pushReq(reqObj)
		self.yingXiong_tryMatch()

	def yingXiong_cancelSignUp( self, playerMB ):
		"""
		取消报名
		"""
		for reqObj in self.yingXiong_reqList:
			if reqObj and reqObj.isItemPlayer(playerMB.id):
				reqObj.quitSignUp()
				self.yingXiong_popReq(reqObj)
				break

	def yingXiong_onPlayerLoginOff( self, playerMB, playerName ):
		"""
		玩家下线
		"""
		for matchItem in self.yingXiong_matchItemList:
			if matchItem and matchItem.isItemPlayer(playerMB.id):
				matchItem.onPlayerCancelAffirm( self, playerMB, playerName )
				break

		for reqObj in self.yingXiong_reqList:
			if reqObj and reqObj.isItemPlayer( playerMB.id ):
				reqObj.quitSignUp()
				self.yingXiong_popReq(reqObj)
				break

	def yingXiong_onTeamChange( self, teamMB ):
		"""
		队伍人数变动，取消申请
		"""
		teamReqList = [ reqObj for reqObj in self.yingXiong_reqList if reqObj.getType() == REQ_OBJ_TYPE_TEAM and reqObj.getID() == teamMB.id ]
		if len(teamReqList):
			reqObj = teamReqList[0]
			reqObj.quitSignUp()
			self.yingXiong_popReq(reqObj)

		for matchItem in self.yingXiong_matchItemList:
			matchItem.onTeamChange( self, teamMB.id )

	def yingXiong_pushReq( self, reqObj ):
		"""
		压入请求列表
		"""
		self.yingXiong_reqList.append(reqObj)
		reqObj.nofityClientSignup()

	def yingXiong_popReq( self, reqObj ):
		"""
		弹出请求列表
		"""
		for item in self.yingXiong_reqList:
			if item.getID() == reqObj.getID():
				self.yingXiong_reqList.remove( item )
				break

	def yingXiong_onAffirm( self, playerMB, playerName, result ):
		"""
		是否点击确认框
		"""
		if result:
			for matchItem in self.yingXiong_matchItemList:
				matchItem.onPlayerAffirm( self, playerMB, playerName )
		else:
			for matchItem in self.yingXiong_matchItemList:
				matchItem.onPlayerCancelAffirm( self, playerMB, playerName )  
			

	def yingXiong_tryMatch( self ):
		"""
		尝试匹配
		"""
		t_reqObjList = [ obj for obj in self.yingXiong_reqList if obj.getCamp() == csdefine.CAMP_TAOSIM ]
		d_reqObjList = [ obj for obj in self.yingXiong_reqList if obj.getCamp() == csdefine.CAMP_DEMON ]

		tMatchIndexs = self.getMatchReqObjIndexs( t_reqObjList )
		dMatchIndexs = self.getMatchReqObjIndexs( d_reqObjList )
		if tMatchIndexs and dMatchIndexs:
			t_MatchObj = MatchObj( csdefine.CAMP_TAOSIM,[ t_reqObjList[index] for index in tMatchIndexs ] )
			d_MatchObj = MatchObj( csdefine.CAMP_DEMON, [d_reqObjList[index] for index in dMatchIndexs ] )
			self.yingXiong_pushMatch( t_MatchObj,d_MatchObj )

	def getMatchReqObjIndexs( self, campReqList ):
		"""
		获取一组报名小队中能组成5人战队的小队的index
		"""
		Num = Const.SPACECOPY_CAMP_YXLM_MATCH_NUMBER
		for indexI,reqObjI in enumerate(campReqList):
			NumI = reqObjI.getPlayerNum()
			if NumI == Num:
				return [indexI]
			elif NumI < Num:
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

	def yingXiong_pushMatch( self, matchObjA, matchObjB ):
		"""
		压入已匹配列表
		"""
		timerID = self.addTimer(csconst.SPACECOPY_CAMP_YXLM_AFFIRM_TIME, 0, TIMER_ARG_AFFIRM_WRITE )
		self.yingXiong_matchItemList.append( MatchItem(self, timerID, matchObjA, matchObjB) )

	def yingXiong_removeMatch( self, matchItem ):
		"""
		移除已匹配列表
		"""
		if matchItem not in self.yingXiong_matchItemList:
			KBEDebug.ERROR_MSG("CampYXLMCopyMgr yingXiong_matchItemList has not this Item")
			return

		self.yingXiong_matchItemList.remove(matchItem)

	def yingXiong_pushSuccessMath( self, matchItem ):
		"""
		压入确认匹配成功列表
		"""
		timerID = self.addTimer(3.0, 0, TIMER_ARG_TELEPORT )
		matchItem.setEnterTimer(timerID,3.0)
		self.yingXiong_successMathList.append(matchItem)

	def yingXiong_removeSuccessMatch( self, matchItem ):
		"""
	 	移除确认匹配成功列表
		"""
		if matchItem not in self.yingXiong_successMathList:
			return
		self.yingXiong_successMathList.remove(matchItem)

	def yingXiong_OnCreateTeam( self, captainMB, teamMB ):
		"""
	 	创建队伍回调
		"""
		for matchItem in self.yingXiong_matchItemList:
			if matchItem and matchItem.isItemPlayer( captainMB.id ):
				matchItem.onCreateTeam(self, captainMB, teamMB)
				break

	def yingXiong_onMemberJoinTeam( self, playerMB ):
		"""
		加入队伍回调
		"""
		for matchItem in self.yingXiong_matchItemList:
			if matchItem and matchItem.isItemPlayer( playerMB.id ):
				matchItem.onMemberJoinTeam( self,playerMB )
				break

	def onTimer( self, id, userArg ):
		"""
		"""
		if userArg == TIMER_ARG_AFFIRM_WRITE:
			for matchItem in self.yingXiong_matchItemList:
				if matchItem.matchTimeID == id:
					#matchItem.affirmFailure( self )
					pass
					break
		elif userArg == TIMER_ARG_TELEPORT:
			for matchItem in self.yingXiong_successMathList:
				if matchItem.enterSpaceTimerID == id:
					matchItem.teleportToCopy( self )
					break


