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

FIRST_TONG_STARCRAFT_SPACENAME = "fu_ben_L_ZLQJ"
SECOND_TONG_STARCRAFT_SPACENAME_LIST= ["fu_ben_L_ZLQJ","fu_ben_L_ZLQJ"]

class PlayerItem:
	"""
	一个玩家的数据
	"""
	def __init__( self, tongDBID, playerDBID, playerName,groupID = -1 ):
		"""
		"""
		self.tongDBID = tongDBID
		self.playerDBID = playerDBID
		self.playerName = playerName
		self.groupID = groupID

class TongItem:
	"""
	一个帮会的数据
	"""
	def __init__( self, tongDBID, membersInfo,isDistribut):
		"""
		"""
		self.tongDBID = tongDBID
		self.members = {} #{playerDBID:PlayerItem}
		self.memberEnterInfoDict = {}  #playerDBID:玩家进入index
		for memberInfo in membersInfo:
			self.members[memberInfo["dbid"]] = PlayerItem(tongDBID,memberInfo["dbid"],memberInfo["name"],memberInfo.get("groupID",-1))
		if isDistribut:
			self.distributionMemberEnterInfo()

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
 	
	def distributionMemberEnterInfo( self ):
		"""
		分配玩家进入信息
		"""
		spaceObj = KST.g_objFactory.getSpaceObject( FIRST_TONG_STARCRAFT_SPACENAME )
		indexList = spaceObj.getEnterIndexsByEnterInfoLen( Const.TONG_STARCRAFT_GROUP_MEMBER )
		if not indexList:
			KBEDebug.ERROR_MSG(" %s space config is error "%FIRST_TONG_STARCRAFT_SPACENAME)
			return

		for playerDBID,playerItem in self.members.items():
			self.setMemberEnterInfo( playerDBID, playerItem.groupID )

	def setMemberEnterInfo( self,playerDBID,index ):
		"""
		"""
		self.memberEnterInfoDict[playerDBID] = index

	def getMemberEnterInfoIndex( self, playerDBID ):
 		if playerDBID in self.memberEnterInfoDict:
 			return self.memberEnterInfoDict[playerDBID]
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
		self.passFirstList = {} 		#排名{tongDBID:time...}
		self.outTongList = []		#被淘汰的帮会[ tongDBID ]

		self.secondTongList = [] 	#第二场的所有帮会
		self.secondTongToSpaceName = {}	# 第二场帮会对应的spaceName

		self.thirdTongDict = {}

	def clearData( self ):
		"""
		清除数据
		"""
		self.warTong = {}
		self.passFirstList = {}
		self.outTongList = []
		self.secondTongList = []
		self.secondTongToSpaceName = {}
		self.thirdTongDict = {}

	def addWarTongData( self,tongDBID,tongMB, playerDBID, playerMB, joinMembersInfo, isDistribut ):
		"""
		增加帮会数据
		"""
		if tongDBID in self.warTong:
			return False
		self.warTong[tongDBID] = TongItem(tongDBID,joinMembersInfo,isDistribut)
		playerMB.statusMessage( csstatus.TONG_STARCRAFT_SIGNUP_SUCCESS,"" )
		memberDBIDList = self.warTong[tongDBID].getMembersDBIDList()
		if playerDBID in memberDBIDList:
			memberDBIDList.remove(playerDBID)
		tongMB.signUpStarcraftSuccess(memberDBIDList) #通知其他人
		return True

	def firstSignUp( self,tongDBID,tongMB, playerDBID, playerMB, joinMembersInfo ):
		"""
		报名
		"""
		if self.addWarTongData( tongDBID,tongMB, playerDBID, playerMB, joinMembersInfo,True ):
			self.requestFirstNewSpace( tongDBID )

	def onFirstTongStarcraftStart( self ):
		"""
		第一场比赛开始
		"""
		KBEngine.globalData["SpaceManager"].remoteCallDomain(FIRST_TONG_STARCRAFT_SPACENAME,"activeStart",[] )

	def requestFirstNewSpace( self, tongDBID ):
		"""
		预创建第一场副本
		"""
		spaceParams = {}
		spaceParams["spaceKey"] = str(tongDBID)
		spaceParams["tongDBID"] = tongDBID
		spaceParams["camp"] = self.camp
		spaceParams["belongType"] = csdefine.SPACE_BELONG_NORMAL
		KBEngine.globalData["SpaceManager"].remoteCallDomain(FIRST_TONG_STARCRAFT_SPACENAME,"requestNewSpace",(spaceParams,))

	def firstQuerySignUp( self, playerMB ):
		"""
		查询报名消息
		"""
		KBEngine.globalData["TongMgr"].firstQuerySignUp( list(self.warTong.keys()), playerMB )

	def gotoFirstStarcraft( self, tongDBID, playerMB, playerDBID,tongName ):
		"""
		进第一场比赛
		"""
		if tongDBID not in self.warTong:
			KBEDebug.ERROR_MSG("tong(%i) is not signUp"%tongDBID)
			return

		if tongDBID in self.passFirstList:
			KBEDebug.ERROR_MSG("tong(%i) is pass first Starcraft"%tongDBID)
			return
		if tongDBID in self.outTongList:
			KBEDebug.ERROR_MSG(" tong(%i) is out first Starcraft"%tongDBID)
			return

		playerItem = self.warTong[tongDBID].getPlayerItem( playerDBID )
		if not playerItem:
			KBEDebug.ERROR_MSG(" signTong has not this player(%s) Sign "%playerDBID)
			return
		if playerItem.tongDBID != tongDBID:
			KBEDebug.ERROR_MSG("player DBID is error")
			return
		index = self.warTong[tongDBID].getMemberEnterInfoIndex( playerDBID )
		if index == None:
			return
		spaceObj = KST.g_objFactory.getSpaceObject( FIRST_TONG_STARCRAFT_SPACENAME )
		enterPos,enterDir = spaceObj.getEnterInfo( index )
		params = {}
		params["spaceKey"] = str(tongDBID)
		params["stageIndex"] = index
		params["groupID"] = playerItem.groupID
		params["playerDBID"] = playerDBID
		params["tongDBID"] = tongDBID
		params["tongName"] = tongName
		playerMB.gotoSpace( FIRST_TONG_STARCRAFT_SPACENAME,enterPos,enterDir,params )

	def onPassFirstStarcraft( self, tongDBID, passTime ):
		"""
		通关第一场
		"""
		if len( self.passFirstList ) > Const.TONG_STARCRAFT_FIRST_PASS_NUMBER:
			self.outTongList.append( tongDBID )
			return
		self.passFirstList[tongDBID] = passTime
		self.mgr.addPassTong( self.camp,tongDBID )

	def queryPassFirstTongStarcraft( self, playerMB ):
		"""
		查询第一场通关信息
		"""
		KBEngine.globalData["TongMgr"].queryPassFirstTongStarcraft( self.passFirstList,playerMB )

	def openSecondTongStarcraftGroup( self, playerMB ):
		"""
		打开第二场的分组
		"""
		groupOne = [ self.secondTongList[i] for i in range(len(self.secondTongList)) if i % 2 == 0]
		groupTwo = [self.secondTongList[i] for i in range(len(self.secondTongList)) if i % 2 == 1]
		KBEngine.globalData["TongMgr"].openSecondTongStarcraftGroup( groupOne, groupTwo,playerMB )

	def secondSignUp( self,tongDBID,tongMB, playerDBID, playerMB, joinMembersInfo ):
		"""
		报名第二场
		"""
		if tongDBID in self.secondTongList:
			self.addWarTongData( tongDBID,tongMB, playerDBID, playerMB, joinMembersInfo,False )

	def secondStart( self ):
		"""
		第二场比赛开始
		"""
		def getSignUpAmount( groupTong ):
			amount = 0
			for tongDBID in self.warTong.keys():
				if tongDBID in groupTong:
					amount += 1
			return amount
		groupOne = [ self.secondTongList[i] for i in range(len(self.secondTongList)) if i % 2 == 0]
		groupTwo = [self.secondTongList[i] for i in range(len(self.secondTongList)) if i % 2 == 1]

		groupOneAmount = getSignUpAmount( groupOne )
		groupTwoAmount = getSignUpAmount( groupTwo )

		if groupOneAmount < Const.TONG_STARCRAFT_SECOND_SIGN_UP_LESS or groupTwoAmount < Const.TONG_STARCRAFT_SECOND_SIGN_UP_LESS:
			#报名帮会不足提前结束
			return
		def getSpaceKey( groupTong ):
			groupStr = ""
			for tongDBID in groupTong:
				if groupStr == "":
					groupStr = str(tongDBID)
				else:
					groupStr += ("|" + str(tongDBID))
			return groupStr
		
		oneSpaceKey = getSpaceKey( groupOne )
		twoSpaceKey = getSpaceKey( groupTwo )

		tempDict = {}
		index = random.randint(0,1)
		if index == 0:
			self.secondTongToSpaceName[0] = groupOne
			self.secondTongToSpaceName[1] = groupTwo
			tempDict[oneSpaceKey] = 0
			tempDict[twoSpaceKey] = 1
		elif index == 1:
			self.secondTongToSpaceName[1] = groupOne
			self.secondTongToSpaceName[0] = groupTwo
			tempDict[oneSpaceKey] = 1
			tempDict[twoSpaceKey] = 0
		spaceParams1 = {}
		spaceParams1["spaceKey"] = oneSpaceKey
		spaceParams1["camp"] = self.camp
		spaceParams1["belongType"] = csdefine.SPACE_BELONG_NORMAL
		index = tempDict[oneSpaceKey]
		KBEngine.globalData["SpaceManager"].remoteCallDomain(SECOND_TONG_STARCRAFT_SPACENAME_LIST[index],"requestNewSpace",(spaceParams1,))
		spaceParams2 = {}
		spaceParams2["spaceKey"] = twoSpaceKey
		spaceParams2["camp"] = self.camp
		spaceParams2["belongType"] = csdefine.SPACE_BELONG_NORMAL
		index = tempDict[twoSpaceKey]
		KBEngine.globalData["SpaceManager"].remoteCallDomain(SECOND_TONG_STARCRAFT_SPACENAME_LIST[index],"requestNewSpace",(spaceParams2,))

	def gotoSecondStarcraft( self, tongDBID, playerMB, playerDBID,tongName ):
		"""
		进入第二场
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

		groupOne = [ self.secondTongList[i] for i in range(len(self.secondTongList)) if i % 2 == 0]
		groupTwo = [self.secondTongList[i] for i in range(len(self.secondTongList)) if i % 2 == 1]
		index = 0
		params = {}
		params["spaceKey"] = str(tongDBID)
		params["playerDBID"] = playerDBID
		params["tongDBID"] = tongDBID
		params["tongName"] = tongName
		params["camp"] = self.camp
		for spaceIndex, groupTong in self.secondTongToSpaceName.items():
			if tongDBID in groupTong:
				index = groupTong.index(tongDBID)
				spaceObj = KST.g_objFactory.getSpaceObject( SECOND_TONG_STARCRAFT_SPACENAME_LIST[spaceIndex] )
				enterPos,enterDir = spaceObj.getEnterInfo( index )
				playerMB.gotoSpace( SECOND_TONG_STARCRAFT_SPACENAME_LIST[spaceIndex],enterPos,enterDir,params )

	def thirdSignUp( self, tongDBID, tongName ):
		"""
		"""
		if tongDBID not in self.thirdTongDict:
			self.thirdTongDict[tongDBID] = tongName

	def gotoThirdStarcraft( self, tongDBID,side,spaceName,enterPos,enterDir,members ):
		"""
		进第三场
		"""
		if not len( self.thirdTongDict ) == 2:
			return
		if tongDBID not in self.thirdTongDict:
			return
		otherTongDBID = 0
		otherTongName = ""
		for thirdTongDBID,thirdTongName in self.thirdTongDict.items():
			if thirdTongDBID != tongDBID:
				otherTongDBID = thirdTongDBID
				otherTongName = thirdTongName
		for member in members:
			packArgs = {}
			packArgs["tongDBID"] = tongDBID
			packArgs["tongName"] = self.thirdTongDict[tongDBID]
			packArgs["camp"] = self.camp
			packArgs["thirdSide"] = side
			packArgs["otherTongDBID"] = otherTongDBID
			packArgs["otherTongName"] = otherTongName
			member.cell.gotoSpaceUseArg( spaceName, enterPos, enterDir, packArgs )


class TongStarcraftManager( MgrPersistentObject.MgrPersistentObject ):
	"""
	帮会争霸 管理类
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
		taskEvents = { "TongStarcraftManager_FirstTongStarcraftSignUpStart":"onFirstTongStarcraftSignUpStart",
						"TongStarcraftManager_FirstTongStarcraftSignUpEnd":"onFirstTongStarcraftSignUpEnd",
						"TongStarcraftManager_FirstTongStarcraftStartNotice":"onFirstTongStarcraftStartNotice",
						"TongStarcraftManager_FirstTongStarcraftStart":"onFirstTongStarcraftStart",
						"TongStarcraftManager_FirstTongStarcraftEnd":"onFirstTongStarcraftEnd"
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
		pass

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

	def onFirstTongStarcraftStartNotice( self, cmd, *callbackArgs ):
		"""
		帮会争霸第一场活动开始前公告
		"""
		KST.g_baseAppEntity.globalWold( csstatus.TONG_STARCRAFT_FIRST_START_NOTICE,"" )

	def onFirstTongStarcraftStart( self, cmd, *callbackArgs ):
		"""
		帮会争霸第一场活动开始
		"""
		self.taoismWarItem.onFirstTongStarcraftStart()
		self.demonWarItem.onFirstTongStarcraftStart()
		KST.g_baseAppEntity.globalWold( csstatus.TONG_STARCRAFT_FIRST_START,"" )
		KBEngine.globalData["firstTongStarcraftStart"] = 1

	def onFirstTongStarcraftEnd( self, cmd, *callbackArgs ):
		"""
		帮会争霸第一场活动结束
		"""
		KST.g_baseAppEntity.globalWold( csstatus.TONG_STARCRAFT_FIRST_END,"" )
		KBEngine.globalData["firstTongStarcraftStart"] = 0
		if len(self.xianPassFirstTongList) < Const.TONG_STARCRAFT_PASS_FIRST_LESS:
			#KST.g_baseAppEntity.globalWold( csstatus. )
			pass
		if len( self.moPassFirstTongList ) < Const.TONG_STARCRAFT_PASS_FIRST_LESS:
			pass

	def onSecondTongStarcraftSignUpStart( self, cmd, *callbackArgs ):
		"""
		帮会争霸第二场活动开始报名
		"""
		self.taoismWarItem.clearData()
		self.demonWarItem.clearData()
		KST.g_baseAppEntity.globalWold( csstatus.TONG_STARCRAFT_SECOND_SIGN_UP,"" )
		if len(self.xianPassFirstTongList) >= Const.TONG_STARCRAFT_PASS_FIRST_LESS:
			tempStr = "secondTongStarcraft_SignUp_%i"%(csdefine.CAMP_TAOSIM)
			self.taoismWarItem.secondTongList = self.xianPassFirstTongList
			KBEngine.globalData[tempStr] = 1
		if len( self.moPassFirstTongList ) >= Const.TONG_STARCRAFT_PASS_FIRST_LESS:
			tempStr = "secondTongStarcraft_SignUp_%i"%(csdefine.CAMP_DEMON)
			self.demonWarItem.secondTongList = self.moPassFirstTongList
			KBEngine.globalData[tempStr] = 1

	def onSecondTongStarcraftSignUpEnd( self, cmd, *callbackArgs ):
		"""
		帮会争霸第二场活动结束报名
		"""
		if len(self.xianPassFirstTongList) >= Const.TONG_STARCRAFT_PASS_FIRST_LESS:
			tempStr = "secondTongStarcraft_SignUp_%i"%(csdefine.CAMP_TAOSIM)
			KBEngine.globalData[tempStr] = 0
		if len( self.moPassFirstTongList ) >= Const.TONG_STARCRAFT_PASS_FIRST_LESS:
			tempStr = "secondTongStarcraft_SignUp_%i"%(csdefine.CAMP_DEMON)
			KBEngine.globalData[tempStr] = 0

	def onSecondTongStarcraftStartNotice( self, cmd, *callbackArgs ):
		"""
		帮会争霸第二场活动开始公告
		"""
		KST.g_baseAppEntity.globalWold( csstatus.TONG_STARCRAFT_SECOND_START_NOTICE,"" )

	def onSecondTongStarcraftStart( self, cmd, *callbackArgs ):
		"""
		帮会争霸第二场活动开始
		"""
		if len(self.xianPassFirstTongList) >= Const.TONG_STARCRAFT_PASS_FIRST_LESS:
			tempStr = "secondTongStarcraft_Start_%i"%(csdefine.CAMP_TAOSIM)
			self.taoismWarItem.secondStart()
			KBEngine.globalData[tempStr] = 1
		if len( self.moPassFirstTongList ) >= Const.TONG_STARCRAFT_PASS_FIRST_LESS:
			tempStr = "secondTongStarcraft_Start_%i"%(csdefine.CAMP_DEMON)
			self.demonWarItem.secondStart()
			KBEngine.globalData[tempStr] = 1

	def onSecondTongStarcraftEnd( self, cmd, *callbackArgs ):
		"""
		帮会争霸第二场活动结束
		"""
		if len(self.xianPassFirstTongList) >= Const.TONG_STARCRAFT_PASS_FIRST_LESS:
			tempStr = "secondTongStarcraft_Start_%i"%(csdefine.CAMP_TAOSIM)
			KBEngine.globalData[tempStr] = 0
		if len( self.moPassFirstTongList ) >= Const.TONG_STARCRAFT_PASS_FIRST_LESS:
			tempStr = "secondTongStarcraft_Start_%i"%(csdefine.CAMP_DEMON)
			KBEngine.globalData[tempStr] = 0

	def onThirdTongStarcraftEnd( self,tongName,camp ):
		"""
		"""
		campStr = ""
		if camp == csdefine.CAMP_TAOSIM:
			campStr = cschannel_msgs.CAMP_TAOSIM
		elif camp == csdefine.CAMP_DEMON:
			campStr = cschannel_msgs.CAMP_DEMON
		msg = tongName + "|" + campStr
		KST.g_baseAppEntity.globalWold( csstatus.TONG_STARCRAFT_THIRD_FIRST_TONG,msg )
		self.getCampWarItem(camp).clearData()

	def getCampWarItem( self, camp ):
		"""
		"""
		if camp == csdefine.CAMP_TAOSIM:
			return self.taoismWarItem
		else:
			return self.demonWarItem

	def tongStarcraft_firstSignUp( self, camp,tongDBID,tongMB, playerDBID, playerMB, joinMembersInfo ):
		"""
		帮会争霸 第一场报名
		"""
		if not KBEngine.globalData["firstTongStarcraftSignUp"]:
			return

		self.getCampWarItem( camp ).firstSignUp( tongDBID,tongMB, playerDBID, playerMB, joinMembersInfo )

	def tongStarcraft_firstQuerySignUp( self,camp, playerMB ):
		"""
		查看第一场报名成功消息
		"""
		self.getCampWarItem(camp).firstQuerySignUp( playerMB )

	def tongStarcraft_gotoFirstStarcraft( self, camp, tongDBID, playerMB, playerDBID, tongName ):
		"""
		请求进第一场
		"""
		if not KBEngine.globalData["firstTongStarcraftSignUp"]:
			return

		self.getCampWarItem(camp).gotoFirstStarcraft( tongDBID, playerMB, playerDBID, tongName )

	def starcraft_onPassFirstStarcraft( self, camp, tongDBID, passTime ):
		"""
		通关第一场比赛
		"""
		self.getCampWarItem(camp).onPassFirstStarcraft( tongDBID, passTime )

	def tongStarcraft_queryPassFirstTongStarcraft( self, camp, playerMB ):
		"""
		查询第一场通关的信息
		"""
		self.getCampWarItem(camp).queryPassFirstTongStarcraft( playerMB )

	def openSecondTongStarcraftGroup( self, camp, playerMB ):
		"""
		打开第二场的分组
		"""
		tempStr = "secondTongStarcraft_SignUp_%i"%camp
		if KBEngine.globalData.get(tempStr,0):
			self.getCampWarItem( camp ).openSecondTongStarcraftGroup( playerMB )

	def tongStarcraft_SecondSignUp( self, camp,tongDBID,tongMB, playerDBID, playerMB, joinMembersInfo ):
		"""
		报名第二场
		"""
		tempStr = "secondTongStarcraft_SignUp_%i"%camp
		if KBEngine.globalData.get(tempStr,0):
			self.getCampWarItem( camp ).secondSignUp( tongDBID,tongMB, playerDBID, playerMB, joinMembersInfo )

	def tongStarcraft_gotoSecondStarcraft( self, camp, tongDBID, playerMB, playerDBID,tongName ):
		"""
		进第二场
		"""
		tempStr = "secondTongStarcraft_Start_%i"%camp
		if KBEngine.globalData.get(tempStr,0):
			self.getCampWarItem( camp ).gotoSecondStarcraft( tongDBID, playerMB, playerDBID, tongName )

	def tongStarcraft_ThirdSignUp( self, camp, tongDBID, tongName ):
		"""
		通过第二场的帮会  直接报名第三场
		"""
		self.getCampWarItem( camp ).thirdSignUp( tongDBID, tongName )

	def tongStarcraft_gotoThirdStarcraft( self, camp, tongDBID,side,spaceName,enterPos,enterDir,members ):
		"""
		进入第三场
		"""
		self.getCampWarItem( camp ).gotoThirdStarcraft( tongDBID,side,spaceName,enterPos,enterDir,members )

