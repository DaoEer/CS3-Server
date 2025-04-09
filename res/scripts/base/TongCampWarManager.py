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
import Const

TONG_CAMP_WAR_SPACE_TAOSIM = ""		# 仙道SpaceName
TONG_CAMP_WAR_SPACE_DEMON = ""		# 魔道SpaceName

class PlayerItem:
	"""
	一个玩家的数据
	"""
	def __init__( self, tongDBID, playerDBID, playerName ):
		"""
		"""
		self.tongDBID = tongDBID
		self.playerDBID = playerDBID
		self.playerName = playerName

class TongItem:
	"""
	一个帮会的数据
	"""
	def __init__( self, tongDBID, membersInfo,tongName, tongLevel):
		"""
		"""
		self.tongName = tongName
		self.tongDBID = tongDBID
		self.tongLevel = tongLevel
		self.members = {} #{playerDBID:PlayerItem}
		for memberInfo in membersInfo:
			self.members[memberInfo["dbid"]] = PlayerItem(tongDBID,memberInfo["dbid"],memberInfo["name"])

	def getMemberNames( self ):
		"""
		获得报名成员人数
		"""
		memberNames = []
		for member in self.members:
			memberNames.append( member.playerName )
		return memberNames

	def getAllMemberDBIDs( self ):
		"""
		获得所有报名玩家的DBID
		"""
		memberDBIDs = []
		for member in self.members:
			memberDBIDs.append( member.playerDBID )
		return memberDBIDs

	def getPlayerItem( self ):
		"""
		获得玩家的数据
		"""
		if playerDBID in self.members:
			return self.members[playerDBID]
		return None


class CampWarItem:
	"""
	一个阵营的数据
	"""
	def __init__( self, mgr, camp ):
		"""
		"""
		self.mgr = mgr
		self.camp = camp
		self.warTong = {}   		#{tongDBID:TongItem}

	def addTongItem( self, tongDBID, tongMB, playerMB, joinMemberInfo, tongName, tongLevel ):
		"""
		增加帮会数据
		"""
		self.warTong[tongDBID] = TongItem( tongDBID, joinMemberInfo, tongName, tongLevel )

	def tongWarSignUp( self,tongDBID, tongMB, playerMB, joinMemberInfo, tongName, tongLevel ):
		"""s
		"""
		if tongDBID not in self.warTong:
			self.addTongItem( tongDBID, tongMB, playerMB, joinMemberInfo,tongName, tongLevel )
		else:
			del self.warTong[tongDBID]
			self.addTongItem( tongDBID, tongMB, playerMB, joinMemberInfo,tongName, tongLevel )

	def queryTongSignUpData( self, tongDBID, playerMB ):
		"""
		查询报名的帮会成员
		"""
		signUpMemberNames = []
		if tongDBID in self.warTong:
			signUpMemberNames.extend(self.warTong[tongDBID].getMemberNames())
		if hasattr(playerMB, "client") and playerMB.client:
			playerMB.client.OnQueryTongSignUpData( signUpMemberNames,Const.TONG_CAMP_WAR_TONG_MAX_JOIN_MEMBER )

	def getAllMemberDBIDs( self ):
		"""
		获得所有参与帮会阵营战的玩家DBID
		"""
		memberDBIDs = []
		for tongItem in self.warTong.values():
			memberDBIDs.extend( tongItem.getAllMemberDBIDs() )

		return memberDBIDs

	def preCreateTongCampWarSpace( self ):
		"""
		预创建帮会阵营战Space
		"""
		params = {}
		params["spaceKey"] = str( self.camp )
		params["belongType"] = csdefine.SPACE_BELONG_NORMAL
		params["playerDBIDs"] = self.getAllMemberDBIDs()
		if self.camp == csdefine.CAMP_TAOSIM:
			spaceName = TONG_CAMP_WAR_SPACE_TAOSIM
		else:
			spaceName = TONG_CAMP_WAR_SPACE_DEMON
		KBEngine.globalData["SpaceManager"].remoteCallDomain( spaceName,"requestNewSpace",(params,) )

	def gotoTongCampWar( self, tongDBID, playerMB, playerDBID ):
		"""
		"""
		if tongDBID not in self.warTong:
			KBEDebug.ERROR_MSG(" tong(%i) is not signUp0"%tongDBID)
			return
		playerItem = self.warTong[tongDBID].getPlayerItem( playerDBID )
		if not playerItem:
			KBEDebug.ERROR_MSG(" signTong has not this player(%s) Sign "%playerDBID)
			return
		if playerItem.tongDBID != tongDBID:
			KBEDebug.ERROR_MSG("player DBID is error")
			return
		if self.camp == csdefine.CAMP_TAOSIM:
			spaceName = TONG_CAMP_WAR_SPACE_TAOSIM
		else:
			spaceName = TONG_CAMP_WAR_SPACE_DEMON
		spaceObj = KST.g_objFactory.getSpaceObject( spaceName )
		enterPos, enterDir = spaceObj.getEnterPosInfo()
		params = {}
		params["spaceKey"] = str( self.camp )
		params["belongType"] = csdefine.SPACE_BELONG_NORMAL
		params["camp"] = self.camp
		params["tongDBID"] = tongDBID
		params["tongName"] = self.warTong[tongDBID].tongName
		params["tongLevel"] = self.warTong[tongDBID].tongLevel
		playerMB.gotoSpace( spaceName, enterPos, enterDir, params )

class TongCampWarManager( MgrPersistentObject.MgrPersistentObject ):
	"""
	CST-8722 帮会阵营战管理器
	"""
	def __init__( self ) :
		MgrPersistentObject.MgrPersistentObject.__init__( self )
		self.taoismWarItem = CampWarItem( self, csdefine.CAMP_TAOSIM )
		self.demonWarItem = CampWarItem( self, csdefine.CAMP_DEMON )
		self.onCompleteInit()
	
	def onTongInitOver( self ):
		"""
		所有帮会初始化完成
		"""
		taskEvents = {  "TongCampWarManager_Notice":"onTongCampWarNotice",
						"TongCampWarManager_SignUpStart":"onTongCampWarSignUpStart",
						"TongCampWarManager_SignUpEnd":"onTongCampWarSignUpEnd",
						"TongCampWarManager_StartNotice":"onTongCampWarStartNotice",
						"TongCampWarManager_Start":"onTongCampWarStart",
						"TongCampWarManager_End":"onTongCampWarEnd",
		 }
		for taskName, callbackName in taskEvents.items():
			for scriptID, cmd in g_CrondDatas.getCrondTaskCmds(taskName):
		 		KBEngine.globalData["CrondManager"].addScheme( scriptID, cmd, self, callbackName, -1,() )

	def onTongCampWarNotice( self, cmd, *callbackArgs ):
		"""
		帮会阵营战公告
		"""
		KST.g_baseAppEntity.globalWold( csstatus.TONG_CAMP_WAR_NOTICE, "" )

	def onTongCampWarSignUpStart( self, cmd, *callbackArgs ):
		"""
		帮会阵营战报名开始
		"""
		KBEngine.globalData["TongCampWarSignUpStart"] = 1

	def onTongCampWarSignUpEnd( self, cmd, *callbackArgs ):
		"""
		帮会阵营战报名结束
		"""
		KBEngine.globalData["TongCampWarSignUpStart"] = 0
		KST.g_baseAppEntity.globalWold( csstatus.TONG_CAMP_WAR_SGIN_UP_END, "" )

	def onTongCampWarStartNotice( self, cmd, *callbackArgs ):
		"""
		帮会阵营战开始公告
		"""
		#进行空间预创建
		self.preCreateTongCampWarSpace()

	def onTongCampWarStart( self, cmd, *callbackArgs ):
		"""
		帮会阵营战开始
		"""
		KBEngine.globalData["TongCampWarStart"] = 1
		KST.g_baseAppEntity.globalWold( csstatus.TONG_CAMP_WAR_START, "" )

	def onTongCampWarEnd( self, cmd, *callbackArgs ):
		"""
		帮会阵营战结束
		"""
		KBEngine.globalData["TongCampWarStart"] = 0

	def getCampWarItem( self, camp ):
		"""
		"""
		if camp == csdefine.CAMP_TAOSIM:
			return self.taoismWarItem
		else:
			return self.demonWarItem

	def preCreateTongCampWarSpace( self ):
		"""
		进行空间预创建
		"""
		self.taoismWarItem.preCreateTongCampWarSpace()
		self.demonWarItem.preCreateTongCampWarSpace()

	def queryTongSignUpData( self, camp, tongDBID, playerMB ):
		"""
		查询帮会报名的数据
		"""
		if not KBEngine.globalData.get("TongCampWarSignUpStart",0):

			return
		self.getCampWarItem(camp).queryTongSignUpData( tongDBID, playerMB )

	def tongCampWarSignUp( self, camp, tongDBID,tongMB, playerMB, joinMemberInfo, tongName, tongLevel ):
		"""
		报名帮会阵营战
		"""
		if not KBEngine.globalData.get("TongCampWarSignUpStart",0):
			return
		self.getCampWarItem( camp ).tongWarSignUp( tongDBID, tongMB, playerMB, joinMemberInfo, tongName, tongLevel )

	def gotoTongCampWar( self, camp, tongDBID, playerMB,playerDBID ):
		"""
		进入帮会阵营战
		"""
		if not KBEngine.globalData.get("TongCampWarStart",0):
			return

		self.getCampWarItem( camp ).gotoTongCampWar( tongDBID, playerMB, playerDBID )



