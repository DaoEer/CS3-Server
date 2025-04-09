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

TIMER_ARG_AFFIRM_WRITE 		= 10
TIMER_ARG_TELEPORT			= 20
TIMER_ARG_MATCH_WRITE		= 30
TIMER_ARG_MATCH_TELEPORT	= 40
SPACE_COPY_CLASS_NAME = "fu_ben_L_SGMZ"
NPC_RANDOM_NUME	= [ "昝腾辉", "骑鹏池", "闻孺", "容彭祖", "长孙卉隆", "况其运", "诸公山", "矫忆轩", "陀家骏", "潜鸿湃", "受晨昊", "澹台景逸" ]

class PlayerData( object ):
	"""
	玩家数据类
	"""
	def __init__( self, mailBox, playerDBID, camp, level, name, profession ):
		self.playerMB = mailBox
		self.playerDBID = playerDBID
		self.camp = camp
		self.level = level
		self.name = name
		self.profession = profession

	def getDictToClient( self ):
		tdict  = {}
		tdict[ "id" ] = str(self.playerMB.id)
		tdict[ "level" ] = str(self.level)
		tdict[ "camp" ] = str(self.camp)
		tdict[ "name" ] = self.name
		tdict[ "profession" ] = str(self.profession)
		return tdict

class ReqTeamInfos( object ):
	"""
	队伍匹配类
	"""
	def __init__( self, playerMB, teamMB, memberDataList, camp, level, profession ):
		self.playerMB =playerMB
		self.teamMB = teamMB
		self.camp = camp
		self.level = level
		self.profession = profession
		self.memberList = []
		for memberData in memberDataList:
			self.memberList.append( PlayerData( memberData["playerMB"], memberData["playerDBID"], memberData["camp"], memberData["level"], memberData["name"], memberData["profession"] ) )

	def getAllPlayerMB( self ):
		return [ member.playerMB for member in self.memberList ]

	def getAllPlayerDBID( self ):
		"""
		"""
		memberDBIDList = []
		for member in self.memberList:
			memberDBIDList.append( member.playerDBID )
		return memberDBIDList

	def isItemPlayer( self, playerID ):
		"""
		判断玩家是否在匹配列表中
		"""
		return playerID in [member.playerMB.id for member in self.memberList ]

	def getTeamPlayerMB( self ):
		return self.playerMB

	def nofityClientSignup( self ):
		self.teamMB.setIsReqCopyCampSGMZ( True )
		self.playerMB.campSGMZOnJoin()
		self.playerMB.client.CampSGMZSignUpSuccess()

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

	def quitSignUp( self ):
		"""
		退出报名
		"""
		self.playerMB.campSGMZOnQuit()
		self.playerMB.statusMessage( csstatus.CAMP_RANDOM_FIT_CANCEL, "" )
		self.playerMB.client.CampSGMZHideAffirmWindow()

	def onMatch( self ):
		"""
		匹配成功
		"""
		self.playerMB.client.CampSGMZOnMatchSuccess()

class MatchObj( object ):
	"""
	一个匹配战队
	"""
	def __init__( self, reqObjList, playerMB, camp, teamMB ):
		self.playerMB = playerMB
		self.camp = camp
		self.teamMB = teamMB
		self.reqObjList = reqObjList
		self.isAffirm1 = False			#队长是否确认

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

	def isAffirm( self ):
		"""
		队长是否已确认
		"""
		return self.isAffirm1

	def onPlayerAffirm( self, playerMB ):
		"""
		队长点击确认
		"""
		self.isAffirm1 = True

	def isSelfTeamReqObj( self, teamID ):
		"""
		是此战队中的某个队伍
		""" 
		for reqObj in self.reqObjList:
			if reqObj.getID() == teamID:
				return True
		return False

	def getTeamPlayerMB( self ):
		"""
		获得队长
		"""
		return self.playerMB

	def getDictToClient( self ):
		"""
		打包一个战队数据发给客户端
		"""
		memberListDict = []
		for reqObj in self.reqObjList:
			memberListDict.extend(reqObj.getDictToClient())
		return memberListDict

	def doOnMatch( self, mgr ):
		"""
		执行匹配完后的工作
		"""
		for reqObj in self.reqObjList:
			mgr.miZhen_popReq(reqObj)
			reqObj.onMatch()

	def onPlayerCancelAffirm( self, mgr, playerMB, playerName ):
		"""
		某玩家队长取消确认
		"""
		for reqObj in self.reqObjList:
			reqObj.teamMB.setIsReqCopyCampSGMZ(False)
			playerMB.statusMessage( csstatus.CAMP_RANDOM_FIT_CANCEL, "" )

	def onEnemyTeamCancelAffirm( self, mgr ):
		"""
		敌方战队玩家取消确认
		"""
		playerMB = self.getTeamPlayerMB()
		playerMB.campSGMZOnQuit()
		playerMB.client.CampSGMZHideAffirmWindow()
		for reqObj in self.reqObjList:
			mgr.miZhen_pushReq(reqObj)

	def getAllPlayerDBID( self ):
		"""
		"""
		memberDBIDList = []
		for reqObj in self.reqObjList:
			memberDBIDList.extend( reqObj.getAllPlayerDBID() )
		return memberDBIDList

	def showEnterSGMZTime( self, time ):
		"""
		"""
		for playerMB in self.getAllPlayerMB():
			playerMB.client.ShowEnterSGMZTime( time )

	def onTeamChange( self, mgr, teamID ):
		"""
		此战队中的某个队伍改变了
		"""
		playerMB = self.getTeamPlayerMB()
		playerMB.campSGMZOnQuit()
		playerMB.client.CampSGMZHideAffirmWindow()

		for reqObj in self.reqObjList:
			if reqObj.getID() == teamID:
				pass
			else:
				mgr.miZhen_pushReq( reqObj )
				playerMB.statusMessage( csstatus.CAMP_RANDOM_FIT_LEAVE,"" )

	def onEnemyTeamChange( self, mgr ):
		"""
		敌对战队的某个队伍改变了
		"""
		playerMB = self.getTeamPlayerMB()
		playerMB.campSGMZOnQuit()
		playerMB.client.CampSGMZHideAffirmWindow()
		playerMB.statusMessage( csstatus.CAMP_RANDOM_FIT_LEAVE )	#敌方战队人员发生改变，你已重新排队。
		
		for reqObj in self.reqObjList:
			mgr.miZhen_pushReq( reqObj )

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
		self.enterRoute = random.sample( range( 0, 4 ), 2 )

	def isItemPlayer( self, playerID ):
		"""
		"""
		return self.objectA.isItemPlayer(playerID) or self.objectB.isItemPlayer(playerID)

	def setEnterTimer( self, timerID, time ):
		"""
		设置进入副本倒计时
		"""
		self.enterSpaceTimerID = timerID 
		self.objectA.showEnterSGMZTime( time )
		self.objectB.showEnterSGMZTime( time )

	def isAllAffirm( self ):
		"""
		两队队长是否全部点确认
		"""
		return self.objectA.isAffirm() and self.objectB.isAffirm()

	def onPlayerAffirm( self, mgr, playerMB, playerName ):
		"""
		玩家点确认
		"""
		if not self.objectA.isItemPlayer(playerMB.id) and not self.objectB.isItemPlayer( playerMB.id ):
			return

		affirmData = {}
		affirmData["xianTeamData"] = self.objectA.getDictToClient()
		affirmData["moTeamData"] = self.objectB.getDictToClient()
		#发送两队的数据给玩家 "Root":[{},{}....]
		if self.objectA.isItemPlayer( playerMB.id ):
			for playerMB in self.objectA.getAllPlayerMB():
				playerMB.client.CampSGMZShowAffirmData( Functions.toJsonString( [affirmData] ) )
			self.objectA.onPlayerAffirm( playerMB )

		if self.objectB.isItemPlayer( playerMB.id ):
			for playerMB in self.objectB.getAllPlayerMB():
				playerMB.client.CampSGMZShowAffirmData( Functions.toJsonString( [affirmData] ) )
			self.objectB.onPlayerAffirm( playerMB )

		if self.isAllAffirm():
			self.onMatchObjSuccess( mgr )

	def onMatchObjSuccess( self, mgr ):
		"""
		某个战队队伍匹配成功
		"""
		if not self.objectA.teamMB or not self.objectB.teamMB:
			return
		spaceParams = {}
		routeParams = {}
		routeParams[self.objectA.camp] = self.getEnterRoute()[0]
		routeParams[self.objectB.camp] = self.getEnterRoute()[1]
		spaceParams["spaceKey"] = SPACE_COPY_CLASS_NAME
		spaceParams["belongType"] = csdefine.SPACE_BELONG_NORMAL
		spaceParams["routeParams"] = routeParams
		spaceParams[self.objectA.teamMB.id] = self.objectA.getAllPlayerDBID()
		spaceParams[self.objectB.teamMB.id] = self.objectB.getAllPlayerDBID()
		spaceParams["teamInfos"] = [self.objectA.camp, self.objectB.camp ]
		KBEngine.globalData["SpaceManager"].remoteCallDomain( SPACE_COPY_CLASS_NAME, "requestNewSpace",(spaceParams,))
		mgr.miZhen_removeMatch( self )
		mgr.miZhen_pushSuccessMath( self )

	def onPlayerCancelAffirm( self, mgr, playerMB, playerName ):
		"""
		玩家取消确认
		"""
		if not self.objectA.isItemPlayer(playerMB.id) and not self.objectB.isItemPlayer(playerMB.id):
			return

		if self.objectA.isItemPlayer( playerMB.id ):
			self.objectA.onPlayerCancelAffirm( mgr, playerMB, playerName )
			self.objectB.onEnemyTeamCancelAffirm( mgr )

		if self.objectB.isItemPlayer( playerMB.id ):
			self.objectB.onPlayerCancelAffirm( mgr, playerMB, playerName )
			self.objectA.onEnemyTeamCancelAffirm( mgr )

		mgr.miZhen_removeMatch(self)

	def onTeamChange( self, mgr, teamID ):
		"""
		当队伍发生改变
		"""
		if self.objectA.isSelfTeamReqObj( teamID ):
			self.objectA.onTeamChange( mgr, teamID )
			self.objectB.onEnemyTeamChange( mgr )
			mgr.miZhen_removeMatch( self )

		if self.objectB.isSelfTeamReqObj( teamID ):
			self.objectB.onTeamChange( mgr, teamID )
			self.objectA.onEnemyTeamChange( mgr )
			mgr.miZhen_removeMatch( self )

	def getEnterRoute( self ):
		"""
		获取进去的路线
		"""
		return self.enterRoute
		
	def teleportToCopy( self, mgr ):
		"""
		传送玩家
		"""
		#仙
		pos,direction = self.getEnterInfos( csdefine.CAMP_TAOSIM, self.getEnterRoute()[0] )
		for playerMB in self.objectA.getAllPlayerMB():
			playerMB.cell.gotoSpace( SPACE_COPY_CLASS_NAME, pos, direction )
		self.objectA.getTeamPlayerMB().campSGMZOnQuit()

		#魔
		pos,direction = self.getEnterInfos( csdefine.CAMP_DEMON, self.getEnterRoute()[1] )
		for playerMB in self.objectB.getAllPlayerMB():
			playerMB.cell.gotoSpace( SPACE_COPY_CLASS_NAME, pos, direction )
		self.objectA.getTeamPlayerMB().campSGMZOnQuit()

		self.objectA.teamMB.setIsReqCopyCampSGMZ(False)
		self.objectB.teamMB.setIsReqCopyCampSGMZ(False)

		mgr.miZhen_removeSuccessMatch( self )

	def getEnterInfos( self, camp, index ):
		"""
		获取玩家要进入的坐标
		"""
		spaceObj = KST.g_objFactory.getSpaceObject( SPACE_COPY_CLASS_NAME )
		return spaceObj.getEnterPos( camp, index )

class CampSGMZCopyMgr( MgrPersistentObject.MgrPersistentObject ):
	"""
	上古密阵 管理类
	"""
	def __init__( self ) :
		MgrPersistentObject.MgrPersistentObject.__init__( self )
		self.miZhen_reqList = [] 			#所有请求参与的队伍列表
		self.miZhen_matchItemList = [] 		#所有已匹配的列表
		self.miZhen_successMathList = []	#已匹配成功的列表
		self.miZhen_manMachine = []			#已匹配人机的列表
		self.miZhen_successMathMan = []		#已匹配成功的人机列表
		self.manMemberData = []				#人机数据
		self.isManMachine = False			#匹配到的是否为人机
		self.route = 0
		self.onCompleteInit()

	def miZhen_reqTeam( self, playerMB, teamMB, camp, memberDataList, level, profession ):
		"""
		队伍申请
		"""
		if not len(memberDataList):
			return
		if teamMB.id in [obj.getID() for obj in self.miZhen_reqList ]:		#已成功报名，请勿重复报名！
			playerMB.statusMessage( csstatus.DEFAULT_STATUS_MESSAGE,"unused" )
			return

		#memberData { "playerMB":玩家BaseMailbox,"playerDBID":玩家DBID,"level":玩家等级,"name":玩家的名字 }
		reqObj = ReqTeamInfos( playerMB, teamMB, memberDataList, camp, level, profession )
		self.miZhen_pushReq( reqObj )
		self.miZhen_tryMatch()

	def miZhen_cancelSignUp( self, playerMB ):
		"""
		取消报名
		"""
		for reqObj in self.miZhen_reqList:
			if reqObj and reqObj.isItemPlayer(playerMB.id):
				reqObj.quitSignUp()
				self.miZhen_popReq(reqObj)
				break

	def miZhen_pushReq( self, reqObj ):
		"""
		压入请求列表
		"""
		self.miZhen_reqList.append( reqObj )
		reqObj.nofityClientSignup()

	def miZhen_popReq( self, reqObj ):
		"""
		弹出请求列表
		"""
		for item in self.miZhen_reqList:
			if item.getID() == reqObj.getID():
				self.miZhen_reqList.remove( item )
				break

	def miZhen_tryMatch( self ):
		"""
		尝试匹配
		"""
		t_MatchObj = d_MatchObj = None
		for team in self.miZhen_reqList:
			if team.camp == csdefine.CAMP_TAOSIM:
				t_MatchObj = MatchObj( [team], team.playerMB, team.camp , team.teamMB )
			elif team.camp == csdefine.CAMP_DEMON:
				d_MatchObj = MatchObj( [team], team.playerMB, team.camp , team.teamMB )
		if t_MatchObj and d_MatchObj:
			self.miZhen_pushMatch( t_MatchObj, d_MatchObj )
		else:
			self.addTimer( csconst.SPACECOPY_CAMP_SGMZ_MATCH_TIME, 0, TIMER_ARG_MATCH_WRITE )

	def miZhen_pushMatch( self, matchObjA, matchObjB ):
		"""
		压入已匹配列表
		"""
		timerID = self.addTimer( csconst.SPACECOPY_CAMP_SGMZ_AFFIRM_TIME, 0, TIMER_ARG_AFFIRM_WRITE )
		self.miZhen_matchItemList.append( MatchItem(self, timerID, matchObjA, matchObjB) )

	def miZhen_removeMatch( self, matchItem ):
		"""
		移除已匹配列表
		"""
		if matchItem not in self.miZhen_matchItemList:
			KBEDebug.ERROR_MSG("CampSGMZCopyMgr miZhen_matchItemList has not this Item")
			return
		self.miZhen_matchItemList.remove(matchItem)

	def miZhen_pushSuccessMath( self, matchItem ):
		"""
		压入确认匹配成功列表
		"""
		timerID = self.addTimer( 3.0, 0, TIMER_ARG_TELEPORT )
		matchItem.setEnterTimer( timerID, 3.0 )
		self.miZhen_successMathList.append( matchItem )

	def miZhen_removeSuccessMatch( self, matchItem ):
		"""
	 	移除确认匹配成功列表
		"""
		if matchItem not in self.miZhen_successMathList:
			return
		self.miZhen_successMathList.remove(matchItem)

	def miZhen_onAffirm( self, playerMB, playerName, result ):
		"""
		是否点击确认框
		"""
		if result:
			if self.isManMachine:
				self.onMatchSuccess( playerMB )
			else:
				for matchItem in self.miZhen_matchItemList:
					matchItem.onPlayerAffirm( self, playerMB, playerName )
		else:
			for matchItem in self.miZhen_matchItemList:
				matchItem.onPlayerCancelAffirm( self, playerMB, playerName )

	def miZhen_onTeamChange( self, teamMB ):
		"""
		队伍人数变动，取消申请
		"""
		teamReqList = [ reqObj for reqObj in self.miZhen_reqList if reqObj.getID() == teamMB.id ]
		if len( teamReqList ):
			reqObj = teamReqList[0]
			reqObj.quitSignUp()
			self.miZhen_popReq( reqObj )

		for matchItem in self.miZhen_matchItemList:
			matchItem.onTeamChange( self, teamMB.id )

	def miZhen_onPlayerLoginOff( self, playerMB, playerName ):
		"""
		玩家下线
		"""
		for matchItem in self.miZhen_matchItemList:
			if matchItem and matchItem.isItemPlayer(playerMB.id):
				matchItem.onPlayerCancelAffirm( self, playerMB, playerName )
				break

		for reqObj in self.miZhen_reqList:
			if reqObj and reqObj.isItemPlayer( playerMB.id ):
				reqObj.quitSignUp()
				self.miZhen_popReq(reqObj)
				break

	def onTimer( self, id, userArg ):
		"""
		"""
		if userArg == TIMER_ARG_TELEPORT:
			for matchItem in self.miZhen_successMathList:
				if matchItem.enterSpaceTimerID == id:
					matchItem.teleportToCopy( self )
					break

		if userArg == TIMER_ARG_MATCH_WRITE and len( self.miZhen_reqList ):
			for reqObj in list(self.miZhen_reqList):
				self.isManMachine = True
				reqObj.onMatch()		# 通知匹配成功
				self.miZhen_manMachine.append( reqObj )
				break

		if userArg == TIMER_ARG_MATCH_TELEPORT:
			for reqObj in self.miZhen_successMathMan:
				if reqObj in self.miZhen_manMachine:
					self.miZhen_manMachine.remove( reqObj )
				self.teleportToCopy( reqObj )
				break
				
	def onMatchSuccess( self, playerMB ):
		"""
		人机匹配成功
		"""
		self.isManMachine = False
		for reqObj in self.miZhen_manMachine:
			num = len( reqObj.getAllPlayerMB() )
			affirmData = {}
			affirmData["xianTeamData"] = reqObj.getDictToClient()
			affirmData["moTeamData"] = self.getDictToClient( num, reqObj )
			#发送两队的数据给玩家 "Root":[{},{}....]
			for player in reqObj.getAllPlayerMB():
				player.client.CampSGMZShowAffirmData( Functions.toJsonString( [affirmData] ) )
				player.client.ShowEnterSGMZTime( 3.0 )
			spaceParams = {}
			spaceParams["spaceKey"] = SPACE_COPY_CLASS_NAME
			spaceParams["belongType"] = csdefine.SPACE_BELONG_NORMAL
			spaceParams[reqObj.teamMB.id] = reqObj.getAllPlayerDBID()
			spaceParams["teamInfos"] = ( [reqObj.teamMB.id] )
			KBEngine.globalData["SpaceManager"].remoteCallDomain( SPACE_COPY_CLASS_NAME, "requestNewSpace",(spaceParams,))
			self.miZhen_popReq( reqObj )
			self.miZhen_successMathMan.append( reqObj )
			self.addTimer( 3.0, 0, TIMER_ARG_MATCH_TELEPORT )
			
	def getDictToClient( self, num, reqObj ):
		"""
		人机数据
		"""
		self.manMemberData = []
		randomNameList = random.sample( NPC_RANDOM_NUME, num )
		for member in range( num ):
			tdict  = {}
			tdict[ "id" ] = ""
			tdict[ "level" ] = str(reqObj.level)
			tdict[ "camp" ] = str(random.choice( [csdefine.CAMP_TAOSIM, csdefine.CAMP_DEMON] ))
			tdict[ "profession" ] = str(random.choice([csdefine.CLASS_FIGHTER, csdefine.CLASS_SWORDMAN, csdefine.CLASS_ARCHER, csdefine.CLASS_MAGE]))
			tdict[ "name" ] = randomNameList[member]
			self.manMemberData.append( tdict )
		return self.manMemberData

	def getEnterRoute( self ):
		"""
		获取进去的路线
		"""
		return random.sample( range( 0, 4 ), 1 )
		
	def teleportToCopy( self, reqObj ):
		"""
		传送玩家
		"""
		self.route = self.getEnterRoute()[0]
		pos, direction = self.getEnterInfos( csdefine.CAMP_TAOSIM, self.route )
		for playerMB in reqObj.getAllPlayerMB():
			playerMB.cell.gotoSpace( SPACE_COPY_CLASS_NAME, pos, direction )
		reqObj.getTeamPlayerMB().campSGMZOnQuit()
		reqObj.teamMB.setIsReqCopyCampSGMZ(False)
		self.miZhen_successMathMan.remove( reqObj )

	def getEnterInfos( self, camp, index ):
		"""
		获取玩家要进入的坐标
		"""
		spaceObj = KST.g_objFactory.getSpaceObject( SPACE_COPY_CLASS_NAME )
		return spaceObj.getEnterPos( camp, index )

	def onEnterSpaceCopySGMZ( self, playerMB ):
		"""
		玩家进入副本
		"""
		if self.manMemberData:
			playerMB.cell.onManMachineData( self.manMemberData, self.route )

