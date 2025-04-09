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
import Const
import cschannel_msgs

FIRST_TONG_STARCRAFT_SPACENAME = "fu_ben_L_BHZBZ_03"

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
	def __init__( self, tongName,tongDBID, membersInfo):
		"""
		"""
		self.tongDBID = tongDBID
		self.tongName = tongName
		self.members = {} #{playerDBID:PlayerItem}
		for memberInfo in membersInfo:
			self.members[memberInfo["dbid"]] = PlayerItem(tongDBID,memberInfo["dbid"],memberInfo["name"])

	def getMembersDBIDList( self ):
		"""
		获得成员的DBID列表
		"""
		return list(self.members.keys())

	def getPlayerItem( self, playerDBID ):
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
		self.warSignUpTongDBIDs = []
		self.warTong = {}   		#{tongDBID:TongItem}
		self.passFirstList = {} 		#排名{tongDBID:time...}
		self.secondTongToSpaceName = {}#第一场帮会对应的spaceName

	def getWarTongs( self ):
		"""
		获得参加帮会争霸的帮会
		"""
		return list(self.warTong.keys())

	def clearData( self ):
		"""
		清除数据
		"""
		self.warTong = {}
		self.passFirstList = {}

	def firstQuerySignUp( self, playerMB ):
		"""
		查询帮会争霸第一场已报名的帮会
		"""
		firstTongNames = []
		secondTongNames = []
		for tongDBID in self.warSignUpTongDBIDs:
			index = self.warSignUpTongDBIDs.index(tongDBID)
			if index%2 == 0:
				firstTongNames.append( self.warTong[tongDBID].tongName )
			else:
				secondTongNames.append( self.warTong[tongDBID].tongName )

		if hasattr(playerMB, "client" ) and playerMB.client:
			playerMB.client.ShowTongStarcraftFirstSignUpTong( firstTongNames, secondTongNames )

	def addWarTongData( self,tongName,tongDBID,tongMB, playerDBID, playerMB, joinMembersInfo ):
		"""
		增加帮会数据
		"""
		if tongDBID in self.warTong:
			return
		self.warTong[tongDBID] = TongItem(tongName,tongDBID,joinMembersInfo)
		self.warSignUpTongDBIDs.append(tongDBID)
		playerMB.statusMessage( csstatus.TONG_STARCRAFT_SIGNUP_SUCCESS,"" )
		memberDBIDList = self.warTong[tongDBID].getMembersDBIDList()
		if playerDBID in memberDBIDList:
			memberDBIDList.remove(playerDBID)
		tongMB.signUpStarcraftSuccess(memberDBIDList) #通知其他人

	def firstSignUp( self,tongName,tongDBID,tongMB, playerDBID, playerMB, joinMembersInfo ):
		"""
		报名
		"""
		if len(self.getWarTongs()) >= Const.TONG_STARCRAFT_FIRST_SIGN_UP_MAX:
			return
		self.addWarTongData( tongName,tongDBID,tongMB, playerDBID, playerMB, joinMembersInfo )

	def firstStart( self ):
		"""
		第一场开始
		"""
		def getSpaceKey( groupTong ):
			groupStr = ""
			for tongDBID in groupTong:
				if groupStr == "":
					groupStr = str(tongDBID)
				else:
					groupStr += ("|" + str(tongDBID))
			return groupStr
		groupOne = [self.warSignUpTongDBIDs[i] for i in range(len(self.warSignUpTongDBIDs)) if i%2 == 0]
		groupTwo = [ self.warSignUpTongDBIDs[i] for i in range(len(self.warSignUpTongDBIDs)) if i%2 == 1 ]
		oneSpaceKey = getSpaceKey( groupOne )
		twoSpaceKey = getSpaceKey( groupTwo )

		spaceParams1 = {}
		spaceParams1["spaceKey"] = oneSpaceKey
		spaceParams1["camp"] = self.camp
		spaceParams1["belongType"] = csdefine.SPACE_BELONG_NORMAL
		KBEngine.globalData["SpaceManager"].remoteCallDomain(FIRST_TONG_STARCRAFT_SPACENAME,"requestNewSpace",(spaceParams1,))

		spaceParams2 = {}
		spaceParams2["spaceKey"] = twoSpaceKey
		spaceParams2["camp"] = self.camp
		spaceParams2["belongType"] = csdefine.SPACE_BELONG_NORMAL
		KBEngine.globalData["SpaceManager"].remoteCallDomain(FIRST_TONG_STARCRAFT_SPACENAME,"requestNewSpace",(spaceParams2,))

	def gotoFirstTongStarcraft( self, tongDBID, playerMB, playerDBID ):
		"""
		进入帮会争霸第一场
		"""
		if tongDBID not in self.warTong:
			KBEDebug.ERROR_MSG("tong(%i) is not signUp"%tongDBID)
			return
		playerItem = self.warTong[tongDBID].getPlayerItem( playerDBID )
		if not playerItem:
			KBEDebug.ERROR_MSG(" signTong has not this player(%s) Sign "%playerDBID)
			return
		if playerItem.tongDBID != tongDBID:
			KBEDebug.ERROR_MSG("player DBID is error")
			return
		params = {}
		params["spaceKey"] = str(tongDBID)
		params["playerDBID"] = playerDBID
		params["tongDBID"] = tongDBID
		params["tongName"] = self.warTong[tongDBID].tongName
		params["camp"] = self.camp
		spaceObject = KST.g_objFactory.getSpaceObject( FIRST_TONG_STARCRAFT_SPACENAME )
		groupOne = [tongDBID for i in range(len(self.warSignUpTongDBIDs)) if i%2 == 0]
		groupTwo = [ tongDBID for i in range(len(self.warSignUpTongDBIDs)) if i%2 == 1 ]
		index = -1
		if tongDBID in groupOne:
			index = groupOne.index( tongDBID )
		else:
			index = groupTwo.index(tongDBID)
		enterPos, enterDir = spaceObject.getEnterInfo( index )
		playerMB.gotoSpace( FIRST_TONG_STARCRAFT_SPACENAME, enterPos, enterDir, params )

class TongStarcraftManager7904( MgrPersistentObject.MgrPersistentObject ):
	"""
	CST-7904 帮会争霸 管理类
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
		taskEvents = { 
						"TongStarcraftManager7904_TongStarcraftSignUpNotice":"onTongStarcraftSignUpNotice",
						"TongStarcraftManager7904_FirstTongStarcraftSignUpStart":"onFirstTongStarcraftSignUpStart",
						"TongStarcraftManager7904_FirstTongStarcraftSignUpEnd":"onFirstTongStarcraftSignUpEnd",
						"TongStarcraftManager7904_FirstTongStarcraftStartNotice":"onFirstTongStarcraftStartNotice",
						"TongStarcraftManager7904_FirstTongStarcraftStart":"onFirstTongStarcraftStart",
						"TongStarcraftManager7904_FirstTongStarcraftEnd":"onFirstTongStarcraftEnd"
		 }
		for taskName, callbackName in taskEvents.items():
			for scriptID, cmd in g_CrondDatas.getCrondTaskCmds(taskName):
		 		KBEngine.globalData["CrondManager"].addScheme( scriptID, cmd, self, callbackName, -1,() )

	def addPassTong( self, camp,tongDBID ):
		"""
		增加通关帮会
		"""
		if camp == csdefine.CAMP_TAOSIM:
			self.xianPassFirstTongList.append(tongDBID)
		elif camp == csdefine.CAMP_DEMON:
			self.moPassFirstTongList.append(tongDBID)

	def onTongStarcraftSignUpNotice( self, cmd, *callbackArgs ):
		"""
		帮会争霸 活动公告
		"""
		KST.g_baseAppEntity.globalWold( csstatus.TONG_STARCRAFT_FIRST_SIGN_UP_NOTICE,"" )

	def onFirstTongStarcraftSignUpStart( self, cmd, *callbackArgs ):
		"""
		帮会争霸第一场活动开始报名
		"""
		self.taoismWarItem.clearData()
		self.demonWarItem.clearData()
		KST.g_baseAppEntity.globalWold( csstatus.TONG_STARCRAFT_FIRST_SIGN_UP,"" )
		KBEngine.globalData["firstTongStarcraftSignUp"] = 1

	def onFirstTongStarcraftSignUpEnd( self, cmd, *callbackArgs ):
		"""
		帮会争霸第一场活动结束报名
		"""
		KBEngine.globalData["firstTongStarcraftSignUp"] = 0
		if len(self.taoismWarItem.getWarTongs()) < Const.TONG_STARCRAFT_FIRST_SIGN_UP_LESS:
			pass
		if len(self.demonWarItem.getWarTongs()) < Const.TONG_STARCRAFT_FIRST_SIGN_UP_LESS:
			pass

	def onFirstTongStarcraftStartNotice( self, cmd, *callbackArgs ):
		"""
		帮会争霸第一场活动开始前公告
		"""
		KST.g_baseAppEntity.globalWold( csstatus.TONG_STARCRAFT_FIRST_START_NOTICE,"" )

	def onFirstTongStarcraftStart( self, cmd, *callbackArgs ):
		"""
		帮会争霸第一场活动开始
		"""
		#KST.g_baseAppEntity.globalWold( csstatus.TONG_STARCRAFT_FIRST_START,"" )
		if len(self.taoismWarItem.getWarTongs()) >= Const.TONG_STARCRAFT_FIRST_SIGN_UP_LESS:
			tempStr = "firstTongStarcraftStart_%i"%( csdefine.CAMP_TAOSIM )
			self.taoismWarItem.firstStart()
			KBEngine.globalData[tempStr] = 1
		if len( self.demonWarItem.getWarTongs()) >= Const.TONG_STARCRAFT_FIRST_SIGN_UP_LESS:
			tempStr = "firstTongStarcraftStart_%i"%( csdefine.CAMP_DEMON )
			self.demonWarItem.firstStart()
			KBEngine.globalData[tempStr] = 1

	def onFirstTongStarcraftEnd( self, cmd, *callbackArgs ):
		"""
		帮会争霸第一场活动结束
		"""
		if len(self.taoismWarItem.getWarTongs()) >= Const.TONG_STARCRAFT_FIRST_SIGN_UP_LESS:
			tempStr = "firstTongStarcraftStart_%i"%( csdefine.CAMP_TAOSIM )
			KBEngine.globalData[tempStr] = 0
		if len( self.demonWarItem.getWarTongs()) >= Const.TONG_STARCRAFT_FIRST_SIGN_UP_LESS:
			tempStr = "firstTongStarcraftStart_%i"%( csdefine.CAMP_DEMON )
			KBEngine.globalData[tempStr] = 0

	def getCampWarItem( self, camp ):
		"""
		"""
		if camp == csdefine.CAMP_TAOSIM:
			return self.taoismWarItem
		else:
			return self.demonWarItem

	def tongStarcraft_firstQuerySignUp( self, camp, playerMB ):
		"""
		查询帮会争霸第一场已报名的帮会
		"""
		if not KBEngine.globalData["firstTongStarcraftSignUp"]:
			return
		self.getCampWarItem( camp ).firstQuerySignUp( playerMB )
		
	def firstTongStarcraftSignUp( self, tongName,camp,tongDBID,tongMB, playerDBID, playerMB, joinMembersInfo ):
		"""
		帮会争霸 第一场报名
		"""
		if not KBEngine.globalData["firstTongStarcraftSignUp"]:
			return

		self.getCampWarItem( camp ).firstSignUp( tongName,tongDBID,tongMB, playerDBID,playerMB,joinMembersInfo )

	def gotoFirstTongStarcraft( self, camp, tongDBID, playerMB, playerDBID ):
		"""
		进入帮会争霸 第一场
		"""
		tempStr = "firstTongStarcraftStart_%i"%camp
		if KBEngine.globalData.get(tempStr,0):
			self.getCampWarItem( camp ).gotoFirstTongStarcraft( tongDBID, playerMB, playerDBID )

