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
from ConfigObject.BHZBPointDataLoader import g_BHZBPointDataLoader
import copy
import random
import csconst
import Functions
import time
from Functions import Functor
import datetime

#BHZB_STAND_MAP_SPACE = ["fu_ben_L_BHZB_XDSP","fu_ben_L_BHZB_MDSP"]
# 帮会争霸大本营在大地图中位置信息
BHZB_HOME_BARRACKS_POSITIONS = [(98440,113260,-29331),(6510,101430,-27826),(-64457,96550,-25081),(-93320,71090,-22581),(-85520,15986,-25788),(-93327,-34160,-24916),(-97746,-95785,-25253),(-28160,-98080,-27661),(3144,-61520,-29001),(2470,-111858,-23087),(107610,-117790,-19509),(124338,-55730,-19468),(108550,-7700,-26473),(115785,58547,-25755),(28310,490,-26403)]

class PlayerItem:
	"""
	一个玩家的数据
	"""
	def __init__( self, tongDBID, playerDBID,groupID,isCaptain):
		"""
		"""
		self.tongDBID = tongDBID
		self.playerDBID = playerDBID
		self.groupID = groupID
		self.isCaptain = isCaptain
		self.playerMB = None 
		self.teamMB = None
		self.captainID = 0

	def setTeamMB( self, teamMB ):
		"""
		"""
		self.teamMB = teamMB

	def setPlayerMB( self, playerMB ):
		"""
		"""
		self.playerMB = playerMB

	def getTeamMB( self ):
		"""
		"""
		return self.teamMB

	def getPlayMB( self ):
		return self.playerMB

	def setCaptainID( self, captainID ):
		"""
		"""
		self.captainID = captainID

	def getCaptainID( self ):
		"""
		"""
		return self.captainID

	def setIsCaptain( self, isCaptain ):
		self.isCaptain = isCaptain

	def setGroupID( self, groupID ):
		self.groupID = groupID

	def getGroupID( self ):
		return self.groupID

	def getPlayerDBID( self ):
		return self.playerDBID

class TongItem:
	"""
	一个帮会的数据
	"""
	def __init__( self, tongDBID,tongName,tonglevel,membersInfos,camp):
		"""
		"""
		self.tongDBID = tongDBID
		self.tongName = tongName
		self.tonglevel = tonglevel
		self.camp = camp
		self.members = {} #{playerDBID:PlayerItem}
		self.groupWriteToJoin = {}
		self.groupJoinTeamList = {}
		for memberInfo in membersInfos:
			if not memberInfo.captainDBID:
				continue
			captainDBID = int(memberInfo.captainDBID)
			self.members[captainDBID] = PlayerItem(tongDBID,captainDBID,memberInfo.groupID,True)
			for memberDBID in memberInfo.memberDBIDs:
				if not memberDBID:
					continue
				self.members[int(memberDBID)] = PlayerItem(tongDBID,int(memberDBID),memberInfo.groupID,False)

	def initMembers( self, members ):
		"""
		增加帮会成员
		"""
		for member in members:
			self.members[member.playerDBID] = PlayerItem(member.tongDBID, member.playerDBID, member.groupID, member.isCaptain )

	def changeSignUpBHZBMember( self, signUpMembers ):
		"""
		"""
		self.members.clear()
		for memberInfo in signUpMembers:
			if not memberInfo.captainDBID:
				continue
			captainDBID = int(memberInfo.captainDBID)
			self.members[captainDBID] = PlayerItem(self.tongDBID,captainDBID,memberInfo.groupID,True)
			for memberDBID in memberInfo.memberDBIDs:
				if not memberDBID:
					continue
				self.members[int(memberDBID)] = PlayerItem(self.tongDBID,int(memberDBID),memberInfo.groupID,False)

	def getTongName( self ):
		"""
		"""
		return self.tongName

	def getTongCamp( self ):
		return self.camp

	def getMembersDBIDList( self ):
		"""
		获得成员DBID列表
		"""
		return list( self.members.keys() )

	def enterBHZBHomeBarracks( self, playerDBID, playerMB ):
		"""
		进入帮会争霸大本营
		"""
		if playerDBID in self.members:
			spaceObj = KST.g_objFactory.getSpaceObject( csconst.BHZB_HOME_BARRACKS_SPACE[0] )
			groupID = self.members[playerDBID].getGroupID()
			enterPos, enterDir = spaceObj.getEnterInfo()
			pickArgs = {}
			pickArgs["groupID"] = groupID 
			playerMB.cell.gotoSpaceUseArg(csconst.BHZB_HOME_BARRACKS_SPACE[0],enterPos,enterDir,pickArgs)
			captainID, teamMB,playerDBID = self.getTeamInfoByGroupID( groupID )
			if captainID > 0:
				playerMB.onBHZBJoinTeam( captainID, teamMB )
				return
			if groupID in self.groupWriteToJoin:
				self.groupWriteToJoin[groupID].append( (playerMB,playerDBID) )
			else:
				playerMB.onEnterBHZBCreateTeam()
				self.groupWriteToJoin[groupID] = []
		else:
			playerMB.statusMessage( csstatus.BHZB_TONG_SIGN_UP_FORBID_MEMBER,"" )

	def enterBHZBStandMap( self,playerDBID, playerMB, position, direction, pickArgs ):
		"""
		进入帮会争霸沙盘大地图
		"""
		if playerDBID in self.members:
			playerMB.gotoSpace( BHZB_STAND_MAP_SPACE[self.camp-1], position, direction, pickArgs )

	def onBHZBCreateTeam( self,  playerDBID, captainMB, teamMB ):
		"""
		"""
		if playerDBID in self.members:
			self.members[playerDBID].setTeamMB( teamMB )
			self.members[playerDBID].setPlayerMB( captainMB )
			self.members[playerDBID].setCaptainID( captainMB.id )

		groupID = self.members[playerDBID].getGroupID()
		if groupID in self.groupWriteToJoin:
			for info in self.groupWriteToJoin[groupID]:
				#captainID, teamMB,playerDBID = self.getTeamInfoByGroupID( groupID )
				info[0].onBHZBJoinTeam( captainMB.id, teamMB )


	def onBHZBMemberJoinTeam( self ,playerDBID, playerMB ):
		"""
		"""
		#还需要一个移交队长
		if playerDBID in self.members:
			groupID = self.members[playerDBID].getGroupID()
			if groupID in self.groupWriteToJoin:
				if groupID not in self.groupJoinTeamList:
					self.groupJoinTeamList[groupID] = []
				dbids = [i[1] for i in self.groupWriteToJoin[groupID] ]
				if self.groupWriteToJoin[groupID] and playerDBID in dbids:
					self.groupJoinTeamList[groupID].append( playerMB )
				if len( self.groupJoinTeamList[groupID] ) == len( self.groupWriteToJoin[groupID] ):
					del self.groupWriteToJoin[groupID]
					del self.groupJoinTeamList[groupID]
			self.members[playerDBID].setPlayerMB( playerMB )
			if self.members[playerDBID].isCaptain:
				captainID, teamMB,playerDBID = self.getTeamInfoByGroupID( self.members[playerDBID].getGroupID() )
				playerMB.onBHZBChangeCaptain( teamMB )

	def onBHZBChangeCaptain( self, playerDBID, playerMB ):
		"""
		"""
		if playerDBID in self.members:
			captainID, teamMB,srcPlayerDBID = self.getTeamInfoByGroupID( self.members[playerDBID].getGroupID() )
			self.members[srcPlayerDBID].setCaptainID(0)
			self.members[srcPlayerDBID].setTeamMB(None)
			self.members[playerDBID].setCaptainID(playerMB.id)
			self.members[playerDBID].setTeamMB( teamMB )


	def onRoleLoginBHZB( self, playerDBID, playerMB,curCaptainID ):
		"""
		玩家在帮会争霸中重登
		"""
		if playerDBID not in self.members:
			return
		groupID = self.members[playerDBID].getGroupID()
		captainID, teamMB,srcPlayerDBID = self.getTeamInfoByGroupID( groupID )
		if curCaptainID > 0: #当前有队伍
			teamMB.popOfflineTimeKey()
			playerMB.onBHZBJoinTeam( captainID, teamMB )
		else: #当前没有队伍
			playerMB.onEnterBHZBCreateTeam()

	def bhzbTeamMemberLoginOut( self, playerDBID ):
		"""
		"""
		if playerDBID not in self.members:
			return
		groupID = self.members[playerDBID].getGroupID()
		captainID, teamMB,srcPlayerDBID = self.getTeamInfoByGroupID( groupID )
		if captainID > 0 and teamMB:
			teamMB.popOfflineTimeKey()

	def changeBHZBMemberTeam( self, newTeamMembers ):
		"""
		改变帮会成员组队信息
		"""
		srcTeamInfo = {}
		newTeamInfo = {}
		newTeamMemberDict ={}
		allNewTeamPlayerDBIDs = []
		for member in self.members.values():
			if member.getGroupID() not in srcTeamInfo:
				srcTeamInfo[member.getGroupID()] = []
			srcTeamInfo[member.getGroupID()].append( member.getPlayerDBID() )
		for newTeamMember in newTeamMembers:
			if newTeamMember.getGroupID() not in newTeamInfo:
				newTeamInfo[newTeamMember.getGroupID()] = []
			playerDBIDs = [int(i) for i in newTeamMember.getAllMemberDBIDs() if i]
			newTeamInfo[newTeamMember.getGroupID()].extend( playerDBIDs )
			newTeamMemberDict[newTeamMember.getGroupID()] = newTeamMember
			allNewTeamPlayerDBIDs.extend( playerDBIDs )
		
		recordSrcTeamCaptain = {} # 只是记录队员没有变，但是队长变了的
		for groupID,playerDBIDs in srcTeamInfo.items():
			newPlayerDBIDs = newTeamInfo.get(groupID,[])
			playerDBIDs.sort()
			newPlayerDBIDs.sort()
			if playerDBIDs == newPlayerDBIDs: #改组队员信息没有改变
				captainID,teamMB,playerDBID = self.getTeamInfoByGroupID( groupID )
				newCaptainDBID = int(newTeamMemberDict[groupID].captainDBID)
				recordSrcTeamCaptain[groupID] = playerDBID
				if playerDBID != newCaptainDBID: #说明队长换了
					if teamMB != None:
						teamMB.disband()
						self.members[playerDBID].setTeamMB(None)
						for playerDBID in playerDBIDs:
							self.members[playerDBID].setGroupID(0)
							self.members[playerDBID].setIsCaptain(False)
							self.members[playerDBID].setCaptainID(0)			
			else:
				captainID,teamMB,playerDBID = self.getTeamInfoByGroupID( groupID )
				if teamMB!=None:
					teamMB.disband()
					self.members[playerDBID].setTeamMB(None)
					for playerDBID in playerDBIDs:
						self.members[playerDBID].setGroupID(0)
						self.members[playerDBID].setIsCaptain(False)
						self.members[playerDBID].setCaptainID(0)
			# else:
			# 	KBEDebug.ERROR_MSG("-------newPlayerDBIDs---",newPlayerDBIDs)
			# 	KBEDebug.ERROR_MSG("-------playerDBIDs---",playerDBIDs)
			# 	captainID,teamMB,playerDBID = self.getTeamInfoByGroupID( groupID )
			# 	if len(newPlayerDBIDs) <= 0:
			# 		if captainID > 0:
			# 			teamMB.disband()
			# 		for dbid in playerDBIDs:
			# 			self.members[dbid].setGroupID(0)
			# 			self.members[dbid].setIsCaptain(False)
			# 			self.members[dbid].setTeamMB(None)
			# 			self.members[dbid].setCaptainID(0)
			# 	else: # 如果有数据
			# 		newCaptainDBID = int(newTeamMemberDict[groupID].captainDBID)
			# 		KBEDebug.ERROR_MSG("//////////////////newCaptainDBID////",newCaptainDBID)
			# 		if playerDBID == newCaptainDBID: #说明队长没有换 队员换了
			# 			for dbid in playerDBIDs:
			# 				if dbid not in allNewTeamPlayerDBIDs: #如果队员不在这里面
			# 					srcGroupID = self.members[dbid].getGroupID()
			# 					if srcGroupID != groupID:
			# 						continue
			# 					srcCaptainID,srcTeamMB,srcPlayerDBID = self.getTeamInfoByGroupID( srcGroupID )
			# 					self.members[dbid].setGroupID(0)
			# 					KBEDebug.ERROR_MSG("***********************")
			# 					if srcTeamMB and self.members[dbid].getPlayMB() != None:
			# 						srcTeamMB.onBHZBLeaveTeam( self.members[dbid].getPlayMB().id,self.members[dbid].getPlayMB().id )
								
			# 			for dbid in newPlayerDBIDs:
			# 				if dbid not in playerDBIDs:
			# 					self.members[dbid].setGroupID( groupID )
			# 					if playerDBID != dbid:
			# 						self.members[dbid].setIsCaptain(False)
			# 					if self.members[dbid].getPlayMB() != None:
			# 						self.members[dbid].getPlayMB().onBHZBJoinTeam( captainID, teamMB )
								
			# 		else:
			# 			if playerDBID:
			# 				if self.members[playerDBID].getPlayMB() != None:
			# 					self.members[playerDBID].getPlayMB().disbandTeamFB()
			# 				self.members[playerDBID].setTeamMB(None)
			# 				self.members[playerDBID].setCaptainID(0)	
			# 			for dbid in playerDBIDs:
			# 				self.members[dbid].setGroupID(0)
			# 			for dbid in newPlayerDBIDs:
			# 				self.members[dbid].setGroupID(groupID)
			# 				if dbid != newCaptainDBID:
			# 					if groupID not in self.groupWriteToJoin:
			# 						self.groupWriteToJoin[groupID] = []
			# 					if self.members[dbid].getPlayMB() != None:
			# 						self.groupWriteToJoin[groupID].append( (self.members[dbid].getPlayMB(), dbid) )
			# 			if self.members[newCaptainDBID].getPlayMB() != None:
			# 				self.members[newCaptainDBID].setIsCaptain( True )
			# 				self.members[newCaptainDBID].getPlayMB().onEnterBHZBCreateTeam()
	
		for groupID,playerDBIDs in newTeamInfo.items():
			if not len(playerDBIDs):
				continue
			srcPlayerDBIDs = srcTeamInfo.get(groupID,[])
			playerDBIDs.sort()
			srcPlayerDBIDs.sort()
			if newTeamMemberDict[groupID].captainDBID:
				newCaptainDBID = int(newTeamMemberDict[groupID].captainDBID)
			else:
				newCaptainDBID = int(playerDBIDs[0])
			if playerDBIDs == srcPlayerDBIDs and newCaptainDBID == recordSrcTeamCaptain[groupID]:
				continue

			
			for dbid in playerDBIDs:
				self.members[dbid].setGroupID(groupID)
				self.members[dbid].setIsCaptain(False)
				if dbid != newCaptainDBID:
					if groupID not in self.groupWriteToJoin:
						self.groupWriteToJoin[groupID] = []
					if self.members[dbid].getPlayMB() != None:
						self.groupWriteToJoin[groupID].append( (self.members[dbid].getPlayMB(), dbid) )
			if self.members[newCaptainDBID].getPlayMB() != None:
				self.members[newCaptainDBID].setIsCaptain( True )
				self.members[newCaptainDBID].getPlayMB().onEnterBHZBCreateTeam()


	def getTeamInfoByGroupID( self, groupID ):
		"""
		获得队伍信息
		"""
		captainID = 0
		teamMB = None
		playerDBID = 0
		for member in self.members.values():
			if member.getGroupID() == groupID and member.getCaptainID() > 0:
				captainID = member.getCaptainID()
				teamMB = member.getTeamMB()
				playerDBID = member.getPlayerDBID()
				break
		return captainID, teamMB,playerDBID


# class CampWarItem:
# 	"""
# 	一个阵营的数据
# 	"""
# 	def __init__( self, mgr, camp, tongDatas,distributHomeBarracks ):
# 		"""
# 		"""
# 		self.mgr = mgr
# 		self.camp = camp
# 		self.warTong = {}   		#{tongDBID:TongItem}
# 		self.distributHomeBarracks = distributHomeBarracks # 分配大本营的归属帮会
# 		for tongDBID, tongData in tongDatas.items():
# 			self.warTong[tongDBID] = TongItem( tongData.tongDBID, tongData.tongName, tongData.tongLevel, [] )
# 			self.warTong[tongDBID].initMembers( list(tongData.members.values()) )

# 	def clearData( self ):
# 		"""
# 		"""
# 		self.warTong.clear()

# 	def getWarTong( self ):
# 		"""
# 		"""
# 		return self.warTong

# 	def getWarTongItemByTongDBID( self, tongDBID ):
# 		if tongDBID in self.warTong:
# 			return self.warTong[tongDBID]
# 		return None

# 	def getSignUpAllTongDBIDs( self ):
# 		return list( self.warTong.keys() )

# 	def removeWarTong( self, tongDBID ):
# 		"""
# 		"""
# 		del self.warTong[tongDBID]

# 	def setDistributHomeBarracks( self, distributHomeBarracks ):
# 		"""
# 		"""
# 		self.distributHomeBarracks = distributHomeBarracks

# 	def addWarTongData( self, tongDBID, tongName, tonglevel, signCostMoney, tongMB, playerMB, signUpMembers, playerDBID,activity, tongMemNum ):
# 		"""
# 		增加帮会数据
# 		"""
# 		if tongDBID in self.warTong:
# 			return
# 		self.warTong[tongDBID] = TongItem(tongDBID,tongName,tonglevel,signUpMembers)

# 		self.mgr.addWarTongData( self.camp, tongDBID, tongName, tonglevel, signUpMembers,activity, tongMemNum )
# 		playerMB.statusMessage( csstatus.BHZB_TONG_SIGN_UP_SUCCESS,"" )
# 		memberDBIDList = self.warTong[tongDBID].getMembersDBIDList()
# 		if playerDBID in memberDBIDList:
# 			memberDBIDList.remove(playerDBID)
# 		tongMB.signUpBHZBSuccess(memberDBIDList,signCostMoney) #通知其他人

# 	def removeWarTongData( self, tongDBID ):
# 		"""
# 		"""
# 		if tongDBID in self.warTong:
# 			del self.warTong[tongDBID]

# 	def signUPBHZB( self, tongDBID, tongName, tonglevel, signCostMoney, tongMB, playerMB, signUpMembers, playerDBID,activity, tongMemNum ):
# 		"""
# 		"""
# 		self.addWarTongData( tongDBID, tongName, tonglevel, signCostMoney, tongMB, playerMB, signUpMembers, playerDBID,activity, tongMemNum )

# 	def changeSignUpBHZBMember( self, tongDBID, signUpMembers ):
# 		"""
# 		"""
# 		if tongDBID in self.warTong:
# 			self.warTong[tongDBID].changeSignUpBHZBMember( signUpMembers )

# 	def enterBHZBHomeBarracks( self, tongDBID, playerDBID, playerMB ):
# 		"""
# 		进入帮会争霸大本营
# 		"""
# 		if tongDBID in self.warTong:
# 			self.warTong[tongDBID].enterBHZBHomeBarracks( playerDBID, playerMB, self.camp )

# 	def enterBHZBStandMap( self,  tongDBID, playerDBID, playerMB, position, direction, pickArgs  ):
# 		"""
# 		进入帮会争霸沙盘大地图
# 		"""
# 		if tongDBID in self.warTong:
# 			self.warTong[tongDBID].enterBHZBStandMap( playerDBID, playerMB, position, direction, pickArgs, self.camp )

# 	def prepareRequestHomeBarracksSpace( self, pointDatas ):
# 		"""
# 		预创建大本营副本
# 		"""
# 		for tongDBID in self.warTong.keys():
# 			spaceParams = {}
# 			spaceParams["spaceKey"] = str(tongDBID)
# 			spaceParams["belongType"] = csdefine.SPACE_BELONG_TONG
# 			spaceParams["camp"] = self.camp
# 			spaceParams["pointDatas"] = pointDatas
# 			spaceParams["distributHomeBarracks"] = self.distributHomeBarracks
# 			KBEngine.globalData["SpaceManager"].remoteCallDomain(csconst.BHZB_HOME_BARRACKS_SPACE[self.camp -1],"requestNewSpace",(spaceParams,))
# 		# amount = len(self.warTong.keys())
# 		# if amount == 0:
# 		# 	return
# 		# spaceObj = KST.g_objFactory.getSpaceObject( csconst.BHZB_HOME_BARRACKS_SPACE[self.camp - 1] )
# 		# triggerLineTongAmount = spaceObj.getTriggerLineTongAmount()
# 		# spaceNum = amount//triggerLineTongAmount + 1
# 		# tongDBIDs = list( self.warTong.keys() )
# 		# realCreateNum = 0
# 		# while realCreateNum < spaceNum:
# 		# 	begin = realCreateNum*triggerLineTongAmount
# 		# 	end = (realCreateNum + 1) * triggerLineTongAmount
# 		# 	tempList = tongDBIDs[begin:end]
# 		# 	spaceParams = {}
# 		# 	spaceParams["spaceKey"] = str(realCreateNum + 1)
# 		# 	spaceParams["belongType"] = csdefine.SPACE_BELONG_NORMAL
# 		# 	spaceParams["tongDBIDs"] = tempList
# 		# 	KBEngine.globalData["SpaceManager"].remoteCallDomain(csconst.BHZB_HOME_BARRACKS_SPACE[self.camp -1],"requestNewSpace",(spaceParams,))
# 		# 	realCreateNum += 1

# 	# def prepareRequestStandMapSpacce( self ):
# 	# 	"""
# 	# 	预创建沙盘大地图副本
# 	# 	"""
# 	# 	spaceKey = ""
# 	# 	tongNameDict = {}
# 	# 	for tongDBID in self.warTong.keys():
# 	# 		if spaceKey:
# 	# 			spaceKey = spaceKey + "|" + str(tongDBID)
# 	# 		else:
# 	# 			spaceKey = spaceKey + str(tongDBID)
# 	# 		tongNameDict[tongDBID] = self.warTong[tongDBID].getTongName()
# 	# 	spaceParams = {}
# 	# 	spaceParams["spaceKey"] = spaceKey
# 	# 	spaceParams["belongType"] = csdefine.SPACE_BELONG_NORMAL
# 	# 	spaceParams["camp"] = self.camp
# 	# 	spaceParams["tongNameDict"] = tongNameDict
# 	# 	spaceParams["distributHomeBarracks"] = self.distributHomeBarracks
# 	# 	KBEngine.globalData["SpaceManager"].remoteCallDomain(BHZB_STAND_MAP_SPACE[self.camp -1],"requestNewSpace",(spaceParams,))

# 	def onBHZBCreateTeam( self, tongDBID, playerDBID, captainMB, teamMB ):
# 		"""
# 		"""
# 		if tongDBID in self.warTong:
# 			self.warTong[tongDBID].onBHZBCreateTeam( playerDBID, captainMB, teamMB )

# 	def onBHZBMemberJoinTeam( self,tongDBID, playerDBID,playerMB ):
# 		"""
# 		"""
# 		if tongDBID in self.warTong:
# 			self.warTong[tongDBID].onBHZBMemberJoinTeam( playerDBID, playerMB )

# 	def onBHZBChangeCaptain( self, tongDBID, playerDBID,playerMB ):
# 		"""
# 		"""
# 		if tongDBID in self.warTong:
# 			self.warTong[tongDBID].onBHZBChangeCaptain( playerDBID, playerMB )

# 	def changeBHZBMemberTeam( self, tongDBID, newTeamMembers ):
# 		"""
# 		"""
# 		if tongDBID in self.warTong:
# 			self.warTong[tongDBID].changeBHZBMemberTeam( newTeamMembers )

# 	def onRoleLoginBHZB( self, tongDBID, playerDBID,playerMB,curCaptainID ):
# 		"""
# 		"""
# 		if tongDBID in self.warTong:
# 			self.warTong[tongDBID].onRoleLoginBHZB( playerDBID, playerMB,curCaptainID )

# 	def bhzbTeamMemberLoginOut( self, tongDBID, playerDBID ):
# 		"""
# 		"""
# 		if tongDBID in self.warTong:
# 			self.warTong[tongDBID].bhzbTeamMemberLoginOut( playerDBID )

class TongWarItem:
	"""
	帮会争霸帮会数据
	"""
	def __init__( self, mgr, tongDatas,distributHomeBarracks ):
		"""
		"""
		self.mgr = mgr
		self.warTong = {}   		#{tongDBID:TongItem}
		self.distributHomeBarracks = distributHomeBarracks # 分配大本营的归属帮会
		for tongDBID, tongData in tongDatas.items():
			self.warTong[tongDBID] = TongItem( tongData.tongDBID, tongData.tongName, tongData.tongLevel, [],tongData.camp )
			self.warTong[tongDBID].initMembers( list(tongData.members.values()) )

	def clearData( self ):
		"""
		"""
		self.warTong.clear()

	def getWarTong( self ):
		"""
		"""
		return self.warTong

	def getWarTongItemByTongDBID( self, tongDBID ):
		if tongDBID in self.warTong:
			return self.warTong[tongDBID]
		return None

	def getSignUpAllTongDBIDs( self ):
		return list( self.warTong.keys() )

	def removeWarTong( self, tongDBID ):
		"""
		"""
		del self.warTong[tongDBID]

	def setDistributHomeBarracks( self, distributHomeBarracks ):
		"""
		"""
		self.distributHomeBarracks = distributHomeBarracks

	def addWarTongData( self, tongDBID, tongName, tonglevel, signCostMoney, tongMB, playerMB, signUpMembers, playerDBID,activity, tongMemNum,camp ):
		"""
		增加帮会数据
		"""
		if tongDBID in self.warTong:
			return
		self.warTong[tongDBID] = TongItem(tongDBID,tongName,tonglevel,signUpMembers,camp)

		self.mgr.addWarTongData( camp, tongDBID, tongName, tonglevel, signUpMembers,activity, tongMemNum )
		playerMB.statusMessage( csstatus.BHZB_TONG_SIGN_UP_SUCCESS,"" )
		memberDBIDList = self.warTong[tongDBID].getMembersDBIDList()
		if playerDBID in memberDBIDList:
			memberDBIDList.remove(playerDBID)
		tongMB.signUpBHZBSuccess(memberDBIDList,signCostMoney) #通知其他人

	def removeWarTongData( self, tongDBID ):
		"""
		"""
		if tongDBID in self.warTong:
			del self.warTong[tongDBID]

	def signUPBHZB( self, tongDBID, tongName, tonglevel, signCostMoney, tongMB, playerMB, signUpMembers, playerDBID,activity, tongMemNum,camp ):
		"""
		"""
		self.addWarTongData( tongDBID, tongName, tonglevel, signCostMoney, tongMB, playerMB, signUpMembers, playerDBID,activity, tongMemNum,camp )

	def changeSignUpBHZBMember( self, tongDBID, signUpMembers ):
		"""
		"""
		if tongDBID in self.warTong:
			self.warTong[tongDBID].changeSignUpBHZBMember( signUpMembers )

	def enterBHZBHomeBarracks( self, tongDBID, playerDBID, playerMB ):
		"""
		进入帮会争霸大本营
		"""
		if tongDBID in self.warTong:
			self.warTong[tongDBID].enterBHZBHomeBarracks( playerDBID, playerMB )

	def enterBHZBStandMap( self,  tongDBID, playerDBID, playerMB, position, direction, pickArgs  ):
		"""
		进入帮会争霸沙盘大地图
		"""
		if tongDBID in self.warTong:
			self.warTong[tongDBID].enterBHZBStandMap( playerDBID, playerMB, position, direction, pickArgs )

	def prepareRequestHomeBarracksSpace( self, pointDatas ):
		"""
		预创建大本营副本
		"""
		for tongDBID in self.warTong.keys():
			spaceParams = {}
			spaceParams["spaceKey"] = str(tongDBID)
			spaceParams["belongType"] = csdefine.SPACE_BELONG_TONG
			spaceParams["camp"] = self.warTong[tongDBID].getTongCamp()
			spaceParams["pointDatas"] = pointDatas
			spaceParams["distributHomeBarracks"] = self.distributHomeBarracks
			KBEngine.globalData["SpaceManager"].remoteCallDomain(csconst.BHZB_HOME_BARRACKS_SPACE[0],"requestNewSpace",(spaceParams,))
		# amount = len(self.warTong.keys())
		# if amount == 0:
		# 	return
		# spaceObj = KST.g_objFactory.getSpaceObject( csconst.BHZB_HOME_BARRACKS_SPACE[self.camp - 1] )
		# triggerLineTongAmount = spaceObj.getTriggerLineTongAmount()
		# spaceNum = amount//triggerLineTongAmount + 1
		# tongDBIDs = list( self.warTong.keys() )
		# realCreateNum = 0
		# while realCreateNum < spaceNum:
		# 	begin = realCreateNum*triggerLineTongAmount
		# 	end = (realCreateNum + 1) * triggerLineTongAmount
		# 	tempList = tongDBIDs[begin:end]
		# 	spaceParams = {}
		# 	spaceParams["spaceKey"] = str(realCreateNum + 1)
		# 	spaceParams["belongType"] = csdefine.SPACE_BELONG_NORMAL
		# 	spaceParams["tongDBIDs"] = tempList
		# 	KBEngine.globalData["SpaceManager"].remoteCallDomain(csconst.BHZB_HOME_BARRACKS_SPACE[self.camp -1],"requestNewSpace",(spaceParams,))
		# 	realCreateNum += 1

	# def prepareRequestStandMapSpacce( self ):
	# 	"""
	# 	预创建沙盘大地图副本
	# 	"""
	# 	spaceKey = ""
	# 	tongNameDict = {}
	# 	for tongDBID in self.warTong.keys():
	# 		if spaceKey:
	# 			spaceKey = spaceKey + "|" + str(tongDBID)
	# 		else:
	# 			spaceKey = spaceKey + str(tongDBID)
	# 		tongNameDict[tongDBID] = self.warTong[tongDBID].getTongName()
	# 	spaceParams = {}
	# 	spaceParams["spaceKey"] = spaceKey
	# 	spaceParams["belongType"] = csdefine.SPACE_BELONG_NORMAL
	# 	spaceParams["camp"] = self.camp
	# 	spaceParams["tongNameDict"] = tongNameDict
	# 	spaceParams["distributHomeBarracks"] = self.distributHomeBarracks
	# 	KBEngine.globalData["SpaceManager"].remoteCallDomain(BHZB_STAND_MAP_SPACE[self.camp -1],"requestNewSpace",(spaceParams,))

	def onBHZBCreateTeam( self, tongDBID, playerDBID, captainMB, teamMB ):
		"""
		"""
		if tongDBID in self.warTong:
			self.warTong[tongDBID].onBHZBCreateTeam( playerDBID, captainMB, teamMB )

	def onBHZBMemberJoinTeam( self,tongDBID, playerDBID,playerMB ):
		"""
		"""
		if tongDBID in self.warTong:
			self.warTong[tongDBID].onBHZBMemberJoinTeam( playerDBID, playerMB )

	def onBHZBChangeCaptain( self, tongDBID, playerDBID,playerMB ):
		"""
		"""
		if tongDBID in self.warTong:
			self.warTong[tongDBID].onBHZBChangeCaptain( playerDBID, playerMB )

	def changeBHZBMemberTeam( self, tongDBID, newTeamMembers ):
		"""
		"""
		if tongDBID in self.warTong:
			self.warTong[tongDBID].changeBHZBMemberTeam( newTeamMembers )

	def onRoleLoginBHZB( self, tongDBID, playerDBID,playerMB,curCaptainID ):
		"""
		"""
		if tongDBID in self.warTong:
			self.warTong[tongDBID].onRoleLoginBHZB( playerDBID, playerMB,curCaptainID )

	def bhzbTeamMemberLoginOut( self, tongDBID, playerDBID ):
		"""
		"""
		if tongDBID in self.warTong:
			self.warTong[tongDBID].bhzbTeamMemberLoginOut( playerDBID )


class BHZBManager( MgrPersistentObject.MgrPersistentObject ):
	"""
	CST-9910 帮会争霸 管理类
	"""
	def __init__( self ) :
		MgrPersistentObject.MgrPersistentObject.__init__( self )
		self.register()
		# self.taoismWarItem = CampWarItem( self, csdefine.CAMP_TAOSIM, self.taoismTongDataMgr,self.taoismTongNpcHomeBarracks )
		# self.demonWarItem = CampWarItem( self, csdefine.CAMP_DEMON, self.demonTongDataMgr, self.demonTongNpcHomeBarracks )
		self.tongWarItem = TongWarItem( self, self.tongDataMgr,self.tongNpcHomeBarracks )
		self.recordReward = {}
		self.tongIntegralRankDBIDs = []
		self.sendTongRewardTimerID = 0
		self.currentStartTimes = ""
		self.onCompleteInit()
	
	def register( self ):
		"""
		所有帮会初始化完成
		"""
		taskEvents = { 
						"BHZBSignUpStart":"onBHZBSignUpStart",
						"BHZBSignUpEnd":"onBHZBSignUpEnd",
						"BHZBSureTong":"onBHZBSureTong",
						"BHZBSureTongMem":"onBHZBSureTongMem",
						"BHZBStart":"onBHZBStart",
						"BHZBEnd":"onBHZBEnd",
		}
		for taskName, callbackName in taskEvents.items():
			for scriptID, cmd in g_CrondDatas.getCrondTaskCmds(taskName):
				KBEngine.globalData["CrondManager"].addScheme( scriptID, cmd, self, callbackName, -1,() )


	def onBHZBSignUpStart( self, cmd ):
		"""
		帮会争霸 报名开始
		"""
		KBEngine.globalData["BHZBSignUpStart"] = 1
		KBEngine.globalData["BHZBSignUpMem"] = 0

	def onBHZBSignUpEnd( self, cmd ):
		"""
		帮会争霸 报名开始
		"""
		KBEngine.globalData["BHZBSignUpStart"] = 0
		#self.calcJoinWarTong( csdefine.CAMP_DEMON )

	def onBHZBSureTong( self, cmd ):
		"""
		确认报名帮会名单
		"""
		self.calcJoinWarTong(0)
		if not self.checkBHZBStart( 0 ):
			KST.g_baseAppEntity.globalWold(csstatus.BHZB_TONG_START_FAIL,"")
			return

		if self.checkBHZBStart( 0 ):
			self.statusBHZBStart( csdefine.CAMP_TAOSIM )
			self.statusBHZBStart( csdefine.CAMP_DEMON )
			for tongDBID in self.getCampWarItem( csdefine.CAMP_TAOSIM ).getWarTong().keys():
				KBEngine.globalData["TongMgr"].sureBHZBTongSendMail( tongDBID )

	def onBHZBSureTongMem( self, cmd ):
		"""
		确认报名帮会人名
		"""
		KBEngine.globalData["BHZBSignUpMem"] = 1
		if self.checkBHZBStart( 0 ):
			for tongDBID,tongItem in self.getCampWarItem( csdefine.CAMP_TAOSIM ).getWarTong().items():
				KBEngine.globalData["TongMgr"].sureBHZBTongMemberSendMail( tongDBID, tongItem.getMembersDBIDList() )

	def onBHZBStart( self, cmd ):
		"""
		帮会争霸 活动开始
		"""
		# self.taoismWarItem.prepareRequestHomeBarracksSpace()
		# self.demonWarItem.prepareRequestHomeBarracksSpace()
		# self.taoismWarItem.prepareRequestStandMapSpacce()
		# self.demonWarItem.prepareRequestStandMapSpacce()
		if self.checkBHZBStart( 0 ):
			KBEngine.globalData["BHZBStart"] = 1
			self.initPointDatas(0)
			self.distributHomeBarracksData( 0 )
			self.getCampWarItem(0).setDistributHomeBarracks( self.tongNpcHomeBarracks )
			self.getCampWarItem(0).prepareRequestHomeBarracksSpace( self.pointDatas )

			if len(str( datetime.datetime.now().month)) == 1:
				month = "0" + str( datetime.datetime.now().month)
			else:
				month = str( datetime.datetime.now().month)
			if len(str( datetime.datetime.now().day)) == 1:
				day = "0" + str( datetime.datetime.now().day)
			else:
				day = str( datetime.datetime.now().day)

			self.currentStartTimes = str( datetime.datetime.now().year) + month + day

			# self.getCampWarItem( csdefine.CAMP_TAOSIM ).prepareRequestStandMapSpacce()

		# if self.checkBHZBStart( csdefine.CAMP_DEMON ):
		# 	KBEngine.globalData["BHZBStart_2"] = 1
		# 	self.initPointDatas(csdefine.CAMP_DEMON)
		# 	self.distributHomeBarracksData( csdefine.CAMP_DEMON )
		# 	self.getCampWarItem( csdefine.CAMP_DEMON ).setDistributHomeBarracks( self.demonTongNpcHomeBarracks )
		# 	self.getCampWarItem( csdefine.CAMP_DEMON ).prepareRequestHomeBarracksSpace( self.demonPointDatas )
			# self.getCampWarItem( csdefine.CAMP_DEMON ).prepareRequestStandMapSpacce()

	def onBHZBEnd( self, cmd ):
		"""
		帮会争霸 活动结束
		"""
		KBEngine.globalData["BHZBSignUpMem"] = 0
		KBEngine.globalData["BHZBStart"] = 0
		self.clearBHZBPointData(0)
		self.clearAllPointTimer(0)
		self.clearTongSignMemberData(0)
		self.tongWarItem.clearData()
		self.tongDataMgr.clear()
		self.tongIntegralMgr.clear()
		self.signUpTongDataMgr.clear()
		self.pointDatas.clear()
		self.pointSpaceSaveInfoMgr.clear()
		self.tongNpcHomeBarracks = {}
		for spaceScriptID in csconst.BHZB_HOME_BARRACKS_SPACE:
			KBEngine.globalData["SpaceManager"].remoteCallDomain( spaceScriptID,"onBHZBEnd",())
		self.recordReward = {}
		self.tongIntegralRankDBIDs = []
		self.sendTongRewardTimerID = 0
		KBEngine.globalData["TongMgr"].clearAllTongSignMemberData()
		self.writeToDB()

	def calcAllBHZBTongIntegral( self ):
		"""
		计算历届帮会争霸的数据
		"""
		if self.currentStartTimes in self.allTongIntegralMgr:
			return

		allTongIntegralList = sorted(self.allTongIntegralMgr.items(),key = lambda x:x[0],reverse = False)
		tempAllTongIntegralList = allTongIntegralList[len(allTongIntegralList) // 4 * 4:]
		tempTotalTongIntegralDict = {}
		for tempTongIntegralData in tempAllTongIntegralList:
			for tongObj in tempTongIntegralData[1].values():
				if tongObj.tongDBID not in tempTotalTongIntegralDict:
					tempTotalTongIntegralDict[tongObj.tongDBID] = 0
				tempTotalTongIntegralDict[tongObj.tongDBID] += tongObj.integral

		for tongDBID, integralData in self.tongIntegralMgr.items():
			self.allTongIntegralMgr.addALLBHZBTongIntegralRankData( tongDBID, integralData.tongName,integralData.tongLevel, integralData.camp, self.currentStartTimes,integralData.integral )
			totalIntegral = self.allTongIntegralMgr.getCurrentBHZBTongIntegralData( self.currentStartTimes, tongDBID )
			if tongDBID in tempTotalTongIntegralDict:
				totalIntegral += tempTotalTongIntegralDict[tongDBID]
			self.allTongIntegralMgr.setBHZBTongTotalIntegral( self.currentStartTimes, tongDBID, totalIntegral )

	def getCampWarItem( self, camp ):
		"""
		"""
		return self.tongWarItem

	def getCampWarTongData( self, camp ):
		"""
		"""
		return self.tongDataMgr

	def getCampIntegralRankTongData( self, camp ):
		"""
		"""
		return self.tongIntegralMgr

	def getCampSignupTongData( self, camp ):
		"""
		"""
		return self.signUpTongDataMgr

	def getCampPointDatas( self, camp ):
		"""
		"""
		return self.pointDatas

	def getCampPointSpaceSaveInfoMgr( self, camp):
		"""
		"""
		return self.pointSpaceSaveInfoMgr

	def clearAllPointTimer( self, camp ):
		"""
		清除所有据点timer
		"""
		for pointItem in self.getCampPointDatas( camp ).values():
			repeatAddIntegralID = pointItem.getRepeatAddIntegralID()
			if repeatAddIntegralID > 0:
				self.popTimer( repeatAddIntegralID )
				pointItem.setRepeatAddIntegralID( 0 )

	def clearBHZBPointData( self, camp ):
		"""
		清除帮会争霸据点数据
		"""
		for pointItem in self.getCampPointDatas( camp ).values():
			if pointItem.getNotifyID() > 0:
				self.popTimer(pointItem.getNotifyID())
				pointItem.setNotifyID(0)

			playerDBID = pointItem.getPointDeclarePlayerDBID()
			pointItem.setPointDeclareData( 0,0,"","",0,0 )
			self.setBHZBPointState( camp, pointItem, csdefine.NPCEXTPOINT_STATE_CAN_BE_DECLARE )
			self.setBHZBPointReadyEndTime( camp, pointItem, "" )
			pointItem.clearPointJoinAttackMembers()
			pointItem.clearPointJoinProtectMembers()
			pointItem.setJoinProtectGroupTeam( 0 )
			tongDBIDs = list(self.getCampWarItem( camp ).getWarTong().keys())
			KBEngine.globalData["SpaceManager"].remoteCallDomain( csconst.BHZB_HOME_BARRACKS_SPACE[0],"updataBHZBPointJoinProtectTeamID",( camp,tongDBIDs, pointItem.getPointIndex(),pointItem.getJoinProtectGroupTeam()))
			if playerDBID:
				KBEngine.lookUpEntityByDBID( "Role", playerDBID, Functor( self.notifyCancelDeclarePoint ) )

	def clearTongSignMemberData( self, camp ):
		"""
		清除报名帮会争霸帮会的成员数据
		"""
		for tongDBID in self.getCampWarItem(camp).getSignUpAllTongDBIDs():
			KBEngine.globalData["TongMgr"].clearTongSignMemberData(tongDBID)

	def notifyCancelDeclarePoint( self, target ):
		"""
		将玩家宣战取消
		"""
		if target is False:
			return
		if target is True:
			return

		target.cell.setIsDeclarePointBHZB( False )

	def calcJoinWarTong( self, camp ):
		"""
		计算出参与活动帮会
		"""
		signUpTongs = sorted(self.getCampSignupTongData(camp).values(), key = lambda x:x.activity, reverse= True)
		if len(signUpTongs) > Const.BHZB_JOIN_TONG_NUMBER:
			tongs = signUpTongs[0:Const.BHZB_JOIN_TONG_NUMBER]
		else:
			tongs = signUpTongs[:]
		tongDBIDs = [x.tongDBID for x in tongs ]
		for tongDBID in self.getCampWarItem(camp).getSignUpAllTongDBIDs():
			if tongDBID not in tongDBIDs:
				self.removeWarTongData( camp,tongDBID )

	def checkBHZBStart( self, camp ):
		"""
		检查帮会争霸是否开启
		"""
		spaceObj = KST.g_objFactory.getSpaceObject( csconst.BHZB_HOME_BARRACKS_SPACE[0] )
		num = spaceObj.getNeedTongNum()
		if len(self.getCampWarItem(camp).getWarTong()) < num:
			return False
		return True

	def statusBHZBStart( self, camp ):
		"""
		发送活动开始的公告  确认最终参赛帮会
		"""
		msg = ""
		for tong in self.getCampWarItem( camp ).getWarTong().values():
			if tong.getTongCamp() == camp:
				if msg:
					msg += "、" + tong.getTongName()
				else:
					msg += tong.getTongName()
		if camp == csdefine.CAMP_TAOSIM:
			campName = cschannel_msgs.CAMP_TAOSIM
		else:
			campName = cschannel_msgs.CAMP_DEMON

		if msg == "":
			return
		statusMsg = campName + "|" + msg

		KST.g_baseAppEntity.globalWold(csstatus.BHZB_TONG_JOIN_SUCCESS, statusMsg)

	def signUPBHZB( self, camp, tongDBID, tongName, tonglevel, signCostMoney, tongMB, playerMB, signUpMembers, playerDBID, needTongMemAmount,needTongLevel, tongMoney,activity, tongMemNum ):
		"""
		帮会争霸报名
		"""
		if tongDBID in self.getCampWarItem(camp ).getWarTong().keys():
			playerMB.statusMessage( csstatus.BHZB_TONG_SIGN_UP_FORBID_ALREADY,"" )
			return
		if tonglevel < needTongLevel:
			playerMB.statusMessage( csstatus.BHZB_TONG_SIGN_UP_FORBID_LEVEL,"" )
			return
		if tongMoney < signCostMoney:
			playerMB.statusMessage( csstatus.BHZB_TONG_SIGN_UP_FORBID_MONEY,"" )
			return
		if len(signUpMembers) < needTongMemAmount:
			playerMB.statusMessage( csstatus.BHZB_TONG_SIGN_UP_FORBID_MEM_AMOUNT,"" )
			return
		self.getCampWarItem( camp ).signUPBHZB( tongDBID, tongName, tonglevel, signCostMoney, tongMB, playerMB, signUpMembers, playerDBID,activity, tongMemNum,camp )

	def changeSignUpBHZBMember( self, camp, tongDBID, signUpMembers ):
		"""
		改变参加帮会争霸人员
		"""
		if tongDBID in self.getCampWarItem(camp).getWarTong().keys():
			self.getCampWarItem(camp).changeSignUpBHZBMember( tongDBID, signUpMembers )
			self.getCampWarTongData( camp ).changeSignUpBHZBMember( tongDBID, signUpMembers )

	def addWarTongData( self, camp, tongDBID, tongName, tongLevel, signUpMembers, activity, tongMemNum ):
		"""
		增加帮会数据
		"""
		self.getCampWarTongData( camp ).addWarTongData( camp,tongDBID, tongName, tongLevel, signUpMembers )
		self.getCampIntegralRankTongData( camp ).addTongIntegralRankData( tongDBID, tongName, tongLevel,camp )
		self.getCampSignupTongData(camp).addSignUpTongData( tongDBID, tongName, tongLevel, activity, tongMemNum,camp )

	def removeWarTongData( self, camp,tongDBID ):
		"""
		移除帮会数据
		"""
		self.getCampWarItem( camp ).removeWarTongData( tongDBID )
		self.getCampWarTongData( camp ).removeTongData( tongDBID )
		self.getCampIntegralRankTongData( camp ).removeTongIntegralRankData( tongDBID )
		self.getCampSignupTongData( camp ).removeSignUpTongData( tongDBID )
		KBEngine.globalData["TongMgr"].joinBHZBWarFail( tongDBID )

	def updateWarTongActivity( self, camp, tongDBID, activity ):
		"""
		增加帮会活跃度
		"""
		if tongDBID in self.getCampWarItem(camp).getWarTong().keys():
			self.getCampSignupTongData(camp).setTongActivity( tongDBID, activity )

	def enterBHZBHomeBarracks( self, camp, tongDBID, playerDBID, playerMB ):
		"""
		进入帮会争霸大本营
		"""
		if KBEngine.globalData.get("BHZBStart",0):
			self.getCampWarItem( camp ).enterBHZBHomeBarracks( tongDBID, playerDBID, playerMB )
		else:
			playerMB.statusMessage( csstatus.BHZB_TONG_NOT_START,"" )

	def enterBHZBStandMap( self, camp, tongDBID, playerDBID, playerMB, position, direction, pickArgs ):
		"""
		进入帮会争霸沙盘大地图
		"""
		pass
		#self.getCampWarItem( camp ).enterBHZBStandMap( tongDBID, playerDBID, playerMB, position, direction, pickArgs )

	def requestBHZBPointDatas( self, camp, spaceMB ):
		"""
		请求帮会争霸据点数据
		"""
		pass
		# spaceMB.cell.onRequestBHZBPointDatasCB( list(self.getCampPointDatas( camp ).values()) )

	def initPointDatas( self, camp ):
		"""
		初始化据点数据
		"""
		for index in g_BHZBPointDataLoader.getAllBHZBPointIndexs():
			if index in self.getCampPointDatas( camp ):
				continue
			pointItem = g_BHZBPointDataLoader.getBHZBPointItemByPointIndex( index )
			if not pointItem:
				KBEDebug.ERROR_MSG("BHZBPointDataLoader has not point Index (%i)"%index)
				continue
			self.getCampPointDatas( camp ).addNPCPointData( index,0,"",0,"",pointItem.getPointType(),csdefine.NPCEXTPOINT_STATE_CAN_BE_DECLARE)
		
	def requestGotoNPCExtPointWar( self, playerDBID, index, spaceScriptID, occupyPlayerDBID, declareTongDBID, occupyTongDBID, pointType, npcName, npcEntity, declareTongName,declarePlayerDBID,declarePlayerName ):
		"""
		请求进入据点争夺战
		"""
		KBEngine.lookUpEntityByDBID( "Role",playerDBID,Functor( self.requestGotoNPCExtPointWarCallBack, index, spaceScriptID, occupyPlayerDBID, declareTongDBID, occupyTongDBID, pointType, npcName, npcEntity,declareTongName,declarePlayerDBID,declarePlayerName ) )

	def requestGotoNPCExtPointWarCallBack( self, index, spaceScriptID, occupyPlayerDBID, declareTongDBID, occupyTongDBID,pointType, npcName,npcEntity, declareTongName,declarePlayerDBID,declarePlayerName, target ):
		"""
		"""
		if target is False:
			return
		if target is True:
			return
		target.cell.requestGotoNPCExtPointWar( index, spaceScriptID, occupyPlayerDBID, declareTongDBID, occupyTongDBID, pointType, npcName,npcEntity,declareTongName,declarePlayerDBID,declarePlayerName )

	def addTongOccupyPointAmount( self, camp, tongDBID ):
		"""
		增加帮会占领据点数
		"""
		self.getCampIntegralRankTongData( camp ).addTongOccupyPointAmount( tongDBID )
		occupyAmount = self.getCampIntegralRankTongData( camp ).getTongOccupyPointAmount( tongDBID )
		for spaceScriptID in self.getAllBHZBSpaceScriptID():
			KBEngine.globalData["SpaceManager"].remoteCallDomain(spaceScriptID,"updateBHZBWarDetailOccupyNumber",( camp,tongDBID,occupyAmount ))

	def reduceTongOccupyPoint( self, camp, tongDBID ):
		"""
		减少帮会占领据点数
		"""
		self.getCampIntegralRankTongData( camp ).reduceTongOccupyPoint( tongDBID )
		occupyAmount = self.getCampIntegralRankTongData( camp ).getTongOccupyPointAmount( tongDBID )
		for spaceScriptID in self.getAllBHZBSpaceScriptID():
			KBEngine.globalData["SpaceManager"].remoteCallDomain(spaceScriptID,"updateBHZBWarDetailOccupyNumber",( camp,tongDBID,occupyAmount ))

	def addTongIntegral( self, camp, tongDBID, integral ):
		"""
		"""
		self.getCampIntegralRankTongData( camp ).addTongIntegral( tongDBID, integral )
		tongIntegralRankList = sorted(self.getCampIntegralRankTongData( camp ).values(), key = lambda x:x.integral, reverse= True)
		rankTongDBIDs = [ i.tongDBID for i in tongIntegralRankList ]
		rank = 1
		if tongDBID in rankTongDBIDs:
			rank = rankTongDBIDs.index( tongDBID ) + 1
		curIntegral = self.getCampIntegralRankTongData(camp).getTongIntegral(tongDBID)
		for spaceScriptID in self.getAllBHZBSpaceScriptID():
			KBEngine.globalData["SpaceManager"].remoteCallDomain(spaceScriptID,"updateBHZBWarDetailIntegralData",(camp,tongDBID,curIntegral,rank))

	def openBHZBIntegralRank( self, camp, playerMB ):
		"""
		打开帮会争霸积分排名
		"""
		tongIntegralRankList = list(self.getCampIntegralRankTongData( camp ).values())
		if hasattr( playerMB, "client" ) and playerMB.client:
			playerMB.client.OpenBHZBIntegralRank( tongIntegralRankList )

	def addOccupyPointDatas( self, camp, lineNumber, index, pointType,occupyTongDBID,occupyTongName,occupyPlayerDBID,occupyPlayerName ):
		"""
		更新帮会争霸占领数据
		"""
		self.pointDatas.updateOccupyPointData( lineNumber, index, pointType,occupyTongDBID,occupyTongName,occupyPlayerDBID,occupyPlayerName )
		KBEngine.globalData["SpaceManager"].remoteCallDomain(BHZB_STAND_MAP_SPACE[camp-1],"notifySpacePointOccupy",( lineNumber, index, occupyTongDBID,occupyTongName,occupyPlayerDBID,occupyPlayerName))

	def changeNPCPointData( self, camp, lineNumber, index ):
		"""
		define method
		更新据点数据
		"""
		KBEngine.globalData["SpaceManager"].remoteCallDomain( BHZB_STAND_MAP_SPACE[camp-1],"notifySpacePointState",( lineNumber, index ) )

	def openSignUpBHZBRankWin( self, camp, playerMB ):
		"""
		打开帮会争霸报名帮会排名
		"""
		#signUpBHZBRanks = list( self.getCampSignupTongData( camp ).values() )
		signUpBHZBRanks = sorted(self.getCampSignupTongData( camp ).values(), key = lambda x:x.activity, reverse= True)
		if hasattr( playerMB, "client" ) and playerMB.client:
			playerMB.client.OpenSignUpBHZBRankWin( signUpBHZBRanks )

	def onBHZBCreateTeam( self, camp, tongDBID, playerDBID,captainMB, teamMB ):
		"""
		创建队伍
		""" 
		self.getCampWarItem( camp ).onBHZBCreateTeam( tongDBID, playerDBID, captainMB, teamMB )

	def onBHZBMemberJoinTeam( self, camp, tongDBID, playerDBID,playerMB ):
		"""
		加入队伍
		"""
		self.getCampWarItem( camp ).onBHZBMemberJoinTeam( tongDBID, playerDBID,playerMB )

	def onBHZBChangeCaptain( self, camp, tongDBID, playerDBID,playerMB ):
		"""
		移交队长
		"""
		self.getCampWarItem( camp ).onBHZBChangeCaptain( tongDBID, playerDBID,playerMB )

	def sureAllIsBHZBMember( self, camp, tongDBID, newTeamMembers, playerMB, tongMB ):
		"""
		确认是否全部是参加帮会争霸的成员
		"""
		if not self.isAllJoinBHZBMember( camp, tongDBID, newTeamMembers ):
			playerMB.statusMessage( csstatus.BHZB_NOT_JOIN_CANNOT_CHANGE_TEAM,"" )
			return
		tongMB.OnSureAllIsBHZBMember( newTeamMembers )

	def changeBHZBMemberTeam( self, camp, tongDBID, newTeamMembers ):
		"""
		改变队伍的组队信息
		""" 
		self.getCampWarItem( camp ).changeBHZBMemberTeam( tongDBID, newTeamMembers )

	def isAllJoinBHZBMember( self, camp,tongDBID,signUpMembers ):
		"""
		是否全部是参加帮会争霸的成员
		"""
		dstAllMemberDBIDs = []
		for signUpMember in signUpMembers:
			dstAllMemberDBIDs.extend( [ int(i) for i in signUpMember.getAllMemberDBIDs() if i ] )
		tongItem = self.getCampWarItem(camp).getWarTongItemByTongDBID(tongDBID)
		srcAllMemberDBIDs = []
		if tongItem != None:
			srcAllMemberDBIDs = tongItem.getMembersDBIDList()

		for dbid in dstAllMemberDBIDs:
			if dbid not in srcAllMemberDBIDs:
				return False
		return True

	def onRoleLoginBHZB( self, camp, tongDBID, playerDBID,playerMB,curCaptainID ):
		"""
		玩家重登
		"""
		self.getCampWarItem( camp ).onRoleLoginBHZB( tongDBID, playerDBID,playerMB, curCaptainID)

	def changeMemberGroup( self, spaceChildType, camp, tongDBID, groupDict ):
		"""
		define method
		改变玩家所在的组
		"""
		pass
		# if spaceChildType == csdefine.SPACE_TYPE_CHILD_BHZB_HOME_BARRACKS:
		# 	KBEngine.globalData["SpaceManager"].remoteCallDomain( csconst.BHZB_HOME_BARRACKS_SPACE[camp-1],"changeMemberGroup",( tongDBID, groupDict) )
		# if spaceChildType == csdefine.SPACE_TYPE_CHILD_BHZB_STAND_MAP:
		# 	KBEngine.globalData["SpaceManager"].remoteCallDomain( BHZB_STAND_MAP_SPACE[camp-1],"changeMemberGroup",( tongDBID, groupDict) )

	def initNPCPointDataToHomeBarracks( self, camp, standMapSpaceKey, npcPointDatas ):
		"""
		define method
		初始化沙盘据点数据到大本营中
		"""
		pass
		#KBEngine.globalData["SpaceManager"].remoteCallDomain( csconst.BHZB_HOME_BARRACKS_SPACE[camp-1],"initNPCPointDatas",( standMapSpaceKey,npcPointDatas) )
	
	def updataNPCPointRestEndTime( self, standMapSpaceKey, camp, pointIndex, restEndTime ):
		"""
		更新据点重置时间
		"""
		pass 		
		#KBEngine.globalData["SpaceManager"].remoteCallDomain( csconst.BHZB_HOME_BARRACKS_SPACE[camp-1],"updataNPCPointRestEndTime",( standMapSpaceKey,pointIndex, restEndTime) )

	def updataNPCPointReadyEndTime( self, standMapSpaceKey, camp, pointIndex, readyEndTime ):
		"""
		更新据点准备时间
		""" 
		pass		
		#KBEngine.globalData["SpaceManager"].remoteCallDomain( csconst.BHZB_HOME_BARRACKS_SPACE[camp-1],"updataNPCPointReadyEndTime",( standMapSpaceKey,pointIndex, readyEndTime) )

	def updataNPCPointDeclareWarState( self, standMapSpaceKey, camp, pointIndex, declareWarState ):
		"""
		更新据点状态
		""" 		
		pass
		#KBEngine.globalData["SpaceManager"].remoteCallDomain( csconst.BHZB_HOME_BARRACKS_SPACE[camp-1],"updataNPCPointDeclareWarState",( standMapSpaceKey,pointIndex, declareWarState) )

	def updataNPCPointOccupyTongDBID( self, standMapSpaceKey, camp, pointIndex, occupyTongDBID ):
		"""
		更新据点占领帮会
		"""
		pass
		#KBEngine.globalData["SpaceManager"].remoteCallDomain( csconst.BHZB_HOME_BARRACKS_SPACE[camp-1],"updataNPCPointOccupyTongDBID",( standMapSpaceKey,pointIndex, occupyTongDBID) )

	def updataHomeBarracksDataToAllMember( self, standMapSpaceKey, camp, homeBarrackDatas ):
		"""
		更新大本营数据到所有成员
		"""
		pass
		# KBEngine.globalData["SpaceManager"].remoteCallDomain( csconst.BHZB_HOME_BARRACKS_SPACE[camp-1],"updataHomeBarracksDataToAllMember",( standMapSpaceKey,homeBarrackDatas )  )

	def requestGotoBHZBHomeBarrack( self, camp,playerMB ):
		"""
		请求传送到大本营
		"""
		spaceObj = KST.g_objFactory.getSpaceObject( csconst.BHZB_HOME_BARRACKS_SPACE[0] )
		enterPos, enterDir = spaceObj.getEnterInfo()
		playerMB.cell.gotoSpaceUseArg(csconst.BHZB_HOME_BARRACKS_SPACE[0],enterPos,enterDir,{})

	def updataMemberPositionToClient( self, standMapSpaceKey, camp, memberPosDatas ):
		"""
		更新成员位置信息到客户端
		"""
		KBEngine.globalData["SpaceManager"].remoteCallDomain( csconst.BHZB_HOME_BARRACKS_SPACE[0],"updataMemberPositionToClient",(standMapSpaceKey, memberPosDatas))
	
	def distributHomeBarracksData( self, camp ):
		"""
		分配大本营数据
		"""
		tongItems = list(self.getCampWarItem( camp ).getWarTong().values())
		tongNum = len(tongItems)
		tongIndexPosList = random.sample(list(range(0,len(BHZB_HOME_BARRACKS_POSITIONS))) ,tongNum)

		for i in range(0,tongNum):
			tempDict = {}
			tempDict["index"] = tongIndexPosList[i]
			tempDict["position"] = BHZB_HOME_BARRACKS_POSITIONS[tongIndexPosList[i]]
			tempDict["belongTongDBID"] = tongItems[i].tongDBID
			tempDict["name"] = tongItems[i].getTongName()
			self.tongNpcHomeBarracks[ tempDict["index"] ] = tempDict

	def requestPointDetails( self, camp, pointIndex, playerMB ):
		"""
		请求帮会争霸某个据点详情
		"""
		if pointIndex not in self.getCampPointDatas( camp ):
			return
		pointItem = self.getCampPointDatas(camp)[pointIndex]
		pointCfgItem = g_BHZBPointDataLoader.getBHZBPointItemByPointIndex( pointIndex )
		pointName = pointCfgItem.getPointName()
		pointType = pointItem.getPointType()
		pointState = pointItem.getPointDeclareWarState()
		maxJoinPlayerNum = pointCfgItem.getMaxJoinPlayerNum()
		if pointItem.getPointDeclareWarState() == csdefine.NPCEXTPOINT_STATE_CAN_BE_DECLARE:
			if playerMB.client:
				playerMB.client.OpenNPCExtPointDetails( pointName, pointType, pointState, [],[],maxJoinPlayerNum,"",[],[],[])
		else:
			occupyTongName = ""
			occupyJoinMemberNum = 0
			occupyTongDBID = ""
			joinProtectMembers = []
			if pointItem.getPointOccupyTongDBID() > 0:
				occupyTongName = pointItem.getPointOccupyTongName()
				occupyJoinMemberNum = len(pointItem.getPointJoinProtectMembers())
				occupyTongDBID = str( pointItem.getPointOccupyTongDBID() )
				joinProtectMembers = [str(i) for i in pointItem.getPointJoinProtectMembers()]

			declareTongName = ""
			declareJoinMemberNum = 0
			declareTongDBID = ""
			joinAttackMembers = []
			if pointItem.getPointDeclareTongDBID() > 0:
				declareTongName = pointItem.getPointDeclareTongName()
				declareJoinMemberNum = len(pointItem.getPointJoinAttackMembers())
				declareTongDBID = str( pointItem.getPointDeclareTongDBID() )
				joinAttackMembers = [str(i) for i in pointItem.getPointJoinAttackMembers()]

			endTime = pointItem.getPointReadyEndTime()
			if pointItem.getPointDeclareWarState() in [csdefine.NPCEXTPOINT_STATE_REST,csdefine.NPCEXTPOINT_STATE_DEFENSE]:
				endTime = pointItem.getPointRestEndTime()
			if playerMB.client:
				playerMB.client.OpenNPCExtPointDetails( pointName, pointType, pointState,[declareTongName,occupyTongName],[declareJoinMemberNum,occupyJoinMemberNum],maxJoinPlayerNum,endTime,[declareTongDBID,occupyTongDBID],joinAttackMembers,joinProtectMembers )

	def declareBHZBPoint( self, tongDBID, camp, pointIndex, playerMB, playerDBIDs, playerName, tongName, groupID, tongMB, allMemLocalSpaceScriptID ):
		"""
		define method
		宣战某个据点
		"""
		isAllMemNotInSpace = True
		for spaceScriptID in allMemLocalSpaceScriptID:
			if spaceScriptID in self.getAllBHZBSpaceScriptID():
				isAllMemNotInSpace = False
				break
		if isAllMemNotInSpace:
			KBEDebug.ERROR_MSG("All member not in home space")
			return
		if not KBEngine.globalData.get("BHZBStart",0):
			return
		if pointIndex not in self.getCampPointDatas( camp ):
			return
		pointItem = self.getCampPointDatas(camp)[pointIndex]
		if pointItem.getPointDeclareWarState() == csdefine.NPCEXTPOINT_STATE_CAN_NOT_BE_DECLARE:
			playerMB.statusMessage( csstatus.BHZB_POINT_STATE_DECLARE,"" )
			return
		if pointItem.getPointDeclareWarState() == csdefine.NPCEXTPOINT_STATE_FIGHT:
			playerMB.statusMessage( csstatus.BHZB_POINT_ALREADY_TO_JOIN_ATTACK,"" )
			return
		if pointItem.getPointDeclareWarState() == csdefine.NPCEXTPOINT_STATE_REST:
			playerMB.statusMessage( csstatus.BHZB_POINT_ALREADY_TO_JOIN_PROTECT,"" )
			return

		if tongDBID == pointItem.occupyTongDBID:
			return
		
		pointItem.setPointDeclareData( groupID, tongDBID, tongName, playerName, Functions.getTime(),groupID )
		self.setBHZBPointState( camp, pointItem, csdefine.NPCEXTPOINT_STATE_CAN_NOT_BE_DECLARE )
		pointCfgItem = g_BHZBPointDataLoader.getBHZBPointItemByPointIndex( pointIndex )
		tongMB.setbhzbSignUpMembersIsActive( groupID, True, pointIndex )
		tongMB.callBHZBTeamToAttack( groupID,pointCfgItem.getPointName() )
		if pointItem.getPointOccupyTongDBID() > 0:
			self.statusMsgToTongMember( camp, pointItem.getPointOccupyTongDBID(),csstatus.BHZB_TONG_POINT_BE_DECLARE, pointCfgItem.getPointName() )
			statusArgs = "{0}|{1}".format( pointCfgItem.getPointName(), tongName)
			self.statusMsgToTongMember( camp, pointItem.getPointOccupyTongDBID(),csstatus.BHZB_POINT_BE_DECLARE_BY_OTHER_TONG, statusArgs )
			self.addBHZBWarMsgData( camp,pointItem.getPointOccupyTongDBID(),csstatus.BHZB_POINT_BE_DECLARE_BY_OTHER_TONG,statusArgs )
		readyEndTime = Functions.getTime()
		if pointCfgItem:
			readyEndTime = int(pointCfgItem.getReadyTime() * csconst.TIME_ENLARGE_MULTIPLE) + Functions.getTime() 
		self.setBHZBPointReadyEndTime( camp, pointItem, str(readyEndTime) )
		for playerDBID in playerDBIDs:
			pointItem.addPointJoinAttackMembers( playerDBID )
		remainTime = self.getBHZBPointRemainReadyTime( camp, pointIndex )
		if remainTime > 0:
			notfiyID = self.addTimerCallBack( remainTime, "onEnterBHZBPointWar", ( camp, pointIndex,groupID ) )
			pointItem.setNotifyID( notfiyID )
		else:
			self.onEnterBHZBPointWar( camp, pointIndex,groupID )

		for spaceScriptID in self.getAllBHZBSpaceScriptID():
			KBEngine.globalData["SpaceManager"].remoteCallDomain(spaceScriptID, "updateBHZBWarDetailTeamData",( camp,tongDBID,groupID,pointIndex,pointItem.getPointDeclareWarState(),pointCfgItem.getPointName() ))

	def setBHZBPointState( self, camp,pointItem, pointState ):
		"""
		设置帮会争霸据点状态
		"""
		tongDBIDs = list(self.getCampWarItem( camp ).getWarTong().keys())
		pointItem.setPointState( pointState )
		KBEngine.globalData["SpaceManager"].remoteCallDomain( csconst.BHZB_HOME_BARRACKS_SPACE[0],"updataNPCPointDeclareWarState", (camp,tongDBIDs, pointItem.getPointIndex(),pointItem.getPointDeclareWarState()) )
		KBEngine.globalData["SpaceManager"].remoteCallDomain( csconst.BHZB_HOME_BARRACKS_SPACE[0], "updateNPCPointAttackGroupTeamID",(camp,tongDBIDs,pointItem.getPointIndex(),pointItem.getAttackGroupTeamID(),pointItem.getPointDeclareTongDBID()) )
		if pointItem.getPointOccupyTongDBID() > 0:
			pointCfgItem = g_BHZBPointDataLoader.getBHZBPointItemByPointIndex( pointItem.getPointIndex() )
			for spaceScriptID in self.getAllBHZBSpaceScriptID():
				KBEngine.globalData["SpaceManager"].remoteCallDomain(spaceScriptID, "updateBHZBWarDetailOccupyPointData",( camp, pointItem.getPointOccupyTongDBID(), pointItem.getPointIndex(), pointItem.getPointDeclareWarState(),pointCfgItem.getPointName() ))

	def setBHZBPointReadyEndTime( self, camp, pointItem, readyEndTime ):
		"""
		设置帮会争霸据点准备结束时间
		"""
		tongDBIDs = list(self.getCampWarItem( camp ).getWarTong().keys())
		pointItem.setPointReadyEndTime( readyEndTime )
		KBEngine.globalData["SpaceManager"].remoteCallDomain( csconst.BHZB_HOME_BARRACKS_SPACE[0],"updataNPCPointReadyEndTime", (camp, tongDBIDs, pointItem.getPointIndex(),pointItem.getPointReadyEndTime()) )

	def onEnterBHZBPointWar( self, camp, pointIndex,groupID ):
		"""
		进入据点争夺战
		""" 
		if pointIndex not in self.getCampPointDatas( camp ):
			return
		pointItem = self.getCampPointDatas(camp)[pointIndex]
		if pointItem.getNotifyID() > 0:
			self.popTimer(pointItem.getNotifyID())
			pointItem.setNotifyID(0)
		self.setBHZBPointState( camp, pointItem, csdefine.NPCEXTPOINT_STATE_FIGHT )
		self.setBHZBPointReadyEndTime( camp, pointItem, "" )
		pointCfgItem = g_BHZBPointDataLoader.getBHZBPointItemByPointIndex( pointIndex )
		for spaceScriptID in self.getAllBHZBSpaceScriptID():
			KBEngine.globalData["SpaceManager"].remoteCallDomain(spaceScriptID, "updateBHZBWarDetailTeamData",( camp,pointItem.getPointDeclareTongDBID(),groupID,pointIndex,pointItem.getPointDeclareWarState(),pointCfgItem.getPointName() ))
		if pointItem.getPointOccupyTongDBID() > 0:
			spaceScriptID = pointCfgItem.getPointEnterPVPSpaceScriptID()
		else:
			spaceScriptID = pointCfgItem.getPointEnterPVESpaceScriptID()

		tempDict = self.getPointDataByPointIndex( camp, pointIndex )

		KBEngine.globalData["SpaceManager"].remoteCallDomain( csconst.BHZB_HOME_BARRACKS_SPACE[0],"onEnterBHZBPointWar",(camp,pointItem.getPointDeclareTongDBID(),spaceScriptID, tempDict, pointItem.getPointJoinAttackMembers() ) )
		if pointItem.getPointOccupyTongDBID() > 0:
			KBEngine.globalData["SpaceManager"].remoteCallDomain( csconst.BHZB_HOME_BARRACKS_SPACE[0],"onEnterBHZBPointWar", (camp,pointItem.getPointOccupyTongDBID(),spaceScriptID, tempDict, pointItem.getPointJoinProtectMembers() ) )
			if len(pointItem.getPointJoinProtectMembers()) > 0:
				for spaceScriptID in self.getAllBHZBSpaceScriptID():
					KBEngine.globalData["SpaceManager"].remoteCallDomain(spaceScriptID, "updateBHZBWarDetailTeamData",( camp,pointItem.getPointOccupyTongDBID(),pointItem.getJoinProtectGroupTeam(),pointIndex,pointItem.getPointDeclareWarState(),pointCfgItem.getPointName() ))

	def getPointDataByPointIndex( self, camp,pointIndex ):
		"""
		获得据点相关数据
		"""
		if pointIndex not in self.getCampPointDatas( camp ):
			return {}
		pointItem = self.getCampPointDatas(camp)[pointIndex]
		pointCfgItem = g_BHZBPointDataLoader.getBHZBPointItemByPointIndex( pointIndex )
		tempDict = {}
		tempDict["pointIndex"] = pointIndex
		tempDict["pointType"] = pointItem.getPointType()
		tempDict["belongDBID"] = pointItem.getPointOccupyPlayerDBID()
		tempDict["belongTongDBID"] = pointItem.getPointOccupyTongDBID()
		tempDict["belongTongName"] = pointItem.getPointOccupyTongName()
		tempDict["declareTongDBID"] = pointItem.getPointDeclareTongDBID()
		tempDict["declareTongName"] = pointItem.getPointDeclareTongName()
		tempDict["declarePlayerDBID"] = pointItem.getPointDeclarePlayerDBID()
		tempDict["declarePlayerName"] = pointItem.getPointtDeclarePlayerName()
		tempDict["joinProtectGroupTeam"] = pointItem.getJoinProtectGroupTeam()
		tempDict["camp"] = camp
		tempDict["pointName"] = pointCfgItem.getPointName()
		return tempDict

	def getBHZBPointRemainReadyTime( self, camp,pointIndex ):
		"""
		获得据点剩余准备时间
		"""
		if pointIndex not in self.getCampPointDatas( camp ):
			return -1
		pointItem = self.getCampPointDatas(camp)[pointIndex]
		readyEndTime = pointItem.getPointReadyEndTime()
		if readyEndTime:
			remainTime = int(readyEndTime) - Functions.getTime()
		else:
			return -1
		if remainTime >= 0 :
			return Functions.convertTime( remainTime )
		return -1

	def cancelDeclareBHZBPoint( self, tongDBID, camp, pointIndex,groupID, tongMB):
		"""
		取消宣战某个据点
		"""
		if pointIndex not in self.getCampPointDatas( camp ):
			return
		pointItem = self.getCampPointDatas(camp)[pointIndex]
		if pointItem.getPointDeclareWarState() != csdefine.NPCEXTPOINT_STATE_CAN_NOT_BE_DECLARE:
			return

		if pointItem.getNotifyID() > 0:
			self.popTimer(pointItem.getNotifyID())
			pointItem.setNotifyID(0)
		pointItem.setPointDeclareData( 0,0,"","",0,0 )
		self.setBHZBPointState( camp, pointItem, csdefine.NPCEXTPOINT_STATE_CAN_BE_DECLARE )
		tongMB.setbhzbSignUpMembersIsActive( groupID, False,0)
		self.setBHZBPointReadyEndTime( camp, pointItem, "" )
		for spaceScriptID in self.getAllBHZBSpaceScriptID():
			KBEngine.globalData["SpaceManager"].remoteCallDomain(spaceScriptID, "removeBHZBWarDetailTeamData",( camp,tongDBID, groupID)  )
		for playerDBID in pointItem.getPointJoinProtectMembers():
			KBEngine.lookUpEntityByDBID( "Role", playerDBID, Functor( self.statusMsgJoinProtectCallBack, csstatus.BHZB_TONG_POINT_ENEMY_CANCEL ) )
		for playerDBID in pointItem.getPointJoinAttackMembers():
			KBEngine.lookUpEntityByDBID( "Role", playerDBID, Functor( self.statusMsgJoinProtectCallBack, csstatus.BHZB_JUN_SHI_CANCEL_ORDER ) )
		if len(pointItem.getPointJoinProtectMembers()) > 0:
			protectTeamID = pointItem.getJoinProtectGroupTeam()
			KBEngine.globalData["TongMgr"].cancelProtectBHZBPoint( pointItem.getPointOccupyTongDBID(),protectTeamID )
			for spaceScriptID in self.getAllBHZBSpaceScriptID():
				KBEngine.globalData["SpaceManager"].remoteCallDomain(spaceScriptID, "removeBHZBWarDetailTeamData",( camp,pointItem.getPointOccupyTongDBID(), protectTeamID)  )
		pointItem.clearPointJoinAttackMembers()
		pointItem.clearPointJoinProtectMembers()
		pointItem.setJoinProtectGroupTeam( 0 )
		tongDBIDs = list(self.getCampWarItem( camp ).getWarTong().keys())
		KBEngine.globalData["SpaceManager"].remoteCallDomain( csconst.BHZB_HOME_BARRACKS_SPACE[0],"updataBHZBPointJoinProtectTeamID",( camp,tongDBIDs, pointItem.getPointIndex(),pointItem.getJoinProtectGroupTeam()))

	def statusMsgJoinProtectCallBack( self, msgID, target ):
		"""
		提示回防玩家 对方已取消宣战
		"""
		if target is False:
			return
		if target is True:
			return
		target.statusMessage( msgID,"" )

	def joinBHZBPointFight( self, tongDBID, camp, pointIndex, playerMB, playerDBIDs,groupID,tongMB ):
		"""
		参加据点争夺战
		"""
		if pointIndex not in self.getCampPointDatas( camp ):
			return
		pointItem = self.getCampPointDatas(camp)[pointIndex]
		if pointItem.getPointDeclareWarState() == csdefine.NPCEXTPOINT_STATE_CAN_BE_DECLARE:
			playerMB.statusMessage( csstatus.BHZB_POINT_DEFENSE_FORBID_JOIN_ATTACK,"" )
			return
		if pointItem.getPointDeclareWarState() not in [csdefine.NPCEXTPOINT_STATE_CAN_NOT_BE_DECLARE,csdefine.NPCEXTPOINT_STATE_FIGHT]:
			return
		if tongDBID != pointItem.getPointOccupyTongDBID():
			return
		remainTime = self.getBHZBPointRemainReadyTime( camp, pointIndex )
		if remainTime < 0:
			return
		
		pointCfgItem = g_BHZBPointDataLoader.getBHZBPointItemByPointIndex( pointIndex )
		
		# if tongDBID == pointItem.getPointDeclareTongDBID():
		# 	if playerDBID in self.getCampPointDatas(camp).getAllBHZBPointJoinAttackMembers():
		# 		playerMB.statusMessage( csstatus.BHZB_POINT_JOIN_ATTACK_OTHER_POINT,"" )
		# 		return
		# 	if playerDBID in self.getCampPointDatas(camp).getAllBHZBPointJoinProtectMembers():
		# 		playerMB.statusMessage( csstatus.BHZB_POINT_ALREADY_TO_JOIN_PROTECT,"" )
		# 		return

		# if tongDBID == pointItem.getPointOccupyTongDBID():
		# 	if playerDBID in self.getCampPointDatas(camp).getAllBHZBPointJoinProtectMembers():
		# 		playerMB.statusMessage( csstatus.BHZB_POINT_JOIN_PROTECT_OTHER_POINT,"" )
		# 		return
		# 	if playerDBID in self.getCampPointDatas(camp).getAllBHZBPointJoinAttackMembers():
		# 		playerMB.statusMessage( csstatus.BHZB_POINT_ALREADY_TO_JOIN_ATTACK,"" )
		# 		return

		tongDBIDs = list(self.getCampWarItem( camp ).getWarTong().keys())
		# if tongDBID == pointItem.getPointDeclareTongDBID():
		# 	if len(pointItem.getPointJoinAttackMembers()) >= pointCfgItem.getMaxJoinPlayerNum():
		# 		playerMB.statusMessage( csstatus.BHZB_POINT_FORBID_JOINATTACK,"" )
		# 		return
		# 	pointItem.addPointJoinAttackMembers( playerDBID )
		# 	KBEngine.globalData["SpaceManager"].remoteCallDomain( csconst.BHZB_HOME_BARRACKS_SPACE[0],"updataBHZBPointJoinAttackMembers",(tongDBIDs, pointItem.getPointIndex(),pointItem.getPointJoinAttackMembers()))

		if tongDBID == pointItem.getPointOccupyTongDBID():
			if len( pointItem.getPointJoinProtectMembers() ) > 0:
				playerMB.statusMessage( csstatus.BHZB_POINT_FORBID_JOINPROTECT,"" )
				return
			tongMB.setbhzbSignUpMembersIsActive( groupID, True, pointIndex )
			tongMB.callBHZBTeamToProtect( groupID,pointCfgItem.getPointName() )
			for playerDBID in playerDBIDs:
				pointItem.addPointJoinProtectMembers( playerDBID )
			KBEngine.globalData["SpaceManager"].remoteCallDomain( csconst.BHZB_HOME_BARRACKS_SPACE[0],"updataBHZBPointJoinProtectMembers",(camp,tongDBIDs, pointItem.getPointIndex(),pointItem.getPointJoinProtectMembers()))
			pointItem.setJoinProtectGroupTeam( groupID )
			KBEngine.globalData["SpaceManager"].remoteCallDomain( csconst.BHZB_HOME_BARRACKS_SPACE[0],"updataBHZBPointJoinProtectTeamID",( camp,tongDBIDs, pointItem.getPointIndex(),pointItem.getJoinProtectGroupTeam()))
			for spaceScriptID in self.getAllBHZBSpaceScriptID():
				KBEngine.globalData["SpaceManager"].remoteCallDomain(spaceScriptID, "updateBHZBWarDetailTeamData",( camp,tongDBID,groupID,pointIndex,pointItem.getPointDeclareWarState(),pointCfgItem.getPointName() ))

	def cancelJoinBHZBPointFight( self, tongDBID, camp, pointIndex, tongMB ):
		"""
		撤销回防
		"""
		if pointIndex not in self.getCampPointDatas( camp ):
			return
		pointItem = self.getCampPointDatas(camp)[pointIndex]
		if pointItem.getPointDeclareWarState() != csdefine.NPCEXTPOINT_STATE_CAN_NOT_BE_DECLARE:
			return

		tongDBIDs = list(self.getCampWarItem( camp ).getWarTong().keys())
		if tongDBID == pointItem.getPointOccupyTongDBID():
			if len( pointItem.getPointJoinProtectMembers() ) <= 0:
				return
			groupID = pointItem.getJoinProtectGroupTeam()
			tongMB.setbhzbSignUpMembersIsActive( groupID, False, 0 )
			for playerDBID in pointItem.getPointJoinProtectMembers():
				KBEngine.lookUpEntityByDBID( "Role", playerDBID, Functor( self.statusMsgJoinProtectCallBack, csstatus.BHZB_JUN_SHI_CANCEL_ORDER ) )
			pointItem.clearPointJoinProtectMembers()
			pointItem.setJoinProtectGroupTeam(0)
			KBEngine.globalData["SpaceManager"].remoteCallDomain( csconst.BHZB_HOME_BARRACKS_SPACE[0],"updataBHZBPointJoinProtectMembers",(camp,tongDBIDs, pointItem.getPointIndex(),pointItem.getPointJoinProtectMembers()))
			KBEngine.globalData["SpaceManager"].remoteCallDomain( csconst.BHZB_HOME_BARRACKS_SPACE[0],"updataBHZBPointJoinProtectTeamID",( camp,tongDBIDs, pointItem.getPointIndex(),pointItem.getJoinProtectGroupTeam()))
			for spaceScriptID in self.getAllBHZBSpaceScriptID():
				KBEngine.globalData["SpaceManager"].remoteCallDomain(spaceScriptID, "removeBHZBWarDetailTeamData",( camp,pointItem.getPointOccupyTongDBID(), groupID)  )

	def onBHZBPointWarFail( self, camp, pointIndex, groupID ):
		"""
		据点争夺战结束
		"""
		if pointIndex not in self.getCampPointDatas( camp ):
			return
		pointItem = self.getCampPointDatas(camp)[pointIndex]
		if pointItem.getNotifyID() > 0:
			self.popTimer(pointItem.getNotifyID())
			pointItem.setNotifyID(0)
		tongDBID = pointItem.getPointDeclareTongDBID()
		pointItem.setPointDeclareData( 0,0,"","",0,0 )
		self.setBHZBPointState( camp, pointItem,csdefine.NPCEXTPOINT_STATE_REST )

		pointItem.clearPointJoinAttackMembers()
		pointItem.clearPointJoinProtectMembers()
		tongDBIDs = list(self.getCampWarItem( camp ).getWarTong().keys())
		pointItem.setIsEnterDefense(False)
		pointCfgItem = g_BHZBPointDataLoader.getBHZBPointItemByPointIndex( pointIndex )
		restEndTime = Functions.getTime()
		if pointCfgItem:
			restEndTime = int( pointCfgItem.getRestTime() * csconst.TIME_ENLARGE_MULTIPLE ) + Functions.getTime()
		self.setBHZBPointRestEndTime( camp, pointItem, str(restEndTime) )
		self.addTimerCallBack( pointCfgItem.getRestTime(), "setBHZBPointState",( camp, pointItem, csdefine.NPCEXTPOINT_STATE_CAN_BE_DECLARE ) )
		
		lastTongDBID = pointItem.getPointOccupyTongDBID()
		if lastTongDBID:
			KBEngine.globalData["TongMgr"].onBHZBPointWarEnd( lastTongDBID, pointItem.getPointIndex() )
			for spaceScriptID in self.getAllBHZBSpaceScriptID():
				if pointItem.getJoinProtectGroupTeam() > 0:
					KBEngine.globalData["SpaceManager"].remoteCallDomain(spaceScriptID, "removeBHZBWarDetailTeamData",( camp,lastTongDBID, pointItem.getJoinProtectGroupTeam())  )
			if pointItem.getJoinProtectGroupTeam() > 0:
				succTeamArgs = "{0}|{1}".format( cschannel_msgs.ChineseNumber[pointItem.getJoinProtectGroupTeam()],pointCfgItem.getPointName() )
				self.statusMsgToTongMember( camp, lastTongDBID,csstatus.BHZB_TEAM_PROTECT_POINT_SUCCESS,succTeamArgs)
				self.addBHZBWarMsgData( camp, lastTongDBID,csstatus.BHZB_TEAM_PROTECT_POINT_SUCCESS,succTeamArgs)
		if tongDBID:
			KBEngine.globalData["TongMgr"].onBHZBPointWarEnd( tongDBID, pointItem.getPointIndex() )
			for spaceScriptID in self.getAllBHZBSpaceScriptID():
				KBEngine.globalData["SpaceManager"].remoteCallDomain(spaceScriptID, "removeBHZBWarDetailTeamData",( camp,tongDBID, groupID)  )

			failTeamArgs = "{0}|{1}".format( cschannel_msgs.ChineseNumber[groupID],pointCfgItem.getPointName() )
			self.statusMsgToTongMember( camp, tongDBID,csstatus.BHZB_TEAM_OCCUPY_POINT_FAIL,failTeamArgs)
			self.addBHZBWarMsgData( camp, tongDBID,csstatus.BHZB_TEAM_OCCUPY_POINT_FAIL,failTeamArgs )

		pointItem.setJoinProtectGroupTeam( 0 )
		KBEngine.globalData["SpaceManager"].remoteCallDomain( csconst.BHZB_HOME_BARRACKS_SPACE[0],"updataBHZBPointJoinProtectTeamID",( camp,tongDBIDs, pointItem.getPointIndex(),pointItem.getJoinProtectGroupTeam()))

	def onBHZBPointWarSuccess( self, camp, pointIndex, groupID ):
		"""
		改变帮会争霸据点占领数据
		"""
		if pointIndex not in self.getCampPointDatas( camp ):
			return
		pointItem = self.getCampPointDatas(camp)[pointIndex]
		pointCfgItem = g_BHZBPointDataLoader.getBHZBPointItemByPointIndex( pointIndex )
		tongDBID = pointItem.getPointDeclareTongDBID()
		self.addTongOccupyPointAmount( camp, tongDBID  )
		lastTongDBID = pointItem.getPointOccupyTongDBID()
		self.reduceTongOccupyPoint( camp, lastTongDBID )
		self.setBHZBPointOccupyData( camp, pointItem )
		args = "{0}|{1}".format(pointItem.getPointOccupyTongName(),pointCfgItem.getPointName())
		self.statusMsgToAllMember( camp,csstatus.BHZB_TONG_OCCUPY_POINT,args )
		succTeamArgs = "{0}|{1}".format(cschannel_msgs.ChineseNumber[groupID],pointCfgItem.getPointName())
		self.statusMsgToTongMember( camp, tongDBID,csstatus.BHZB_TEAM_OCCUPY_POINT_SUCCESS,succTeamArgs)
		self.addBHZBWarMsgData( camp, tongDBID, csstatus.BHZB_TEAM_OCCUPY_POINT_SUCCESS,succTeamArgs )
		if lastTongDBID:
			tempArgs = "{0}|{1}".format(pointCfgItem.getPointName(),pointItem.getPointOccupyTongName())
			self.statusMsgToTongMember( camp, lastTongDBID,csstatus.BHZB_TONG_BE_OCCUPY_POINT ,tempArgs )
			self.addBHZBWarMsgData( camp, lastTongDBID, csstatus.BHZB_TONG_BE_OCCUPY_POINT, tempArgs )
			if pointItem.getJoinProtectGroupTeam() > 0:
				teamArgs = "{0}|{1}".format( cschannel_msgs.ChineseNumber[pointItem.getJoinProtectGroupTeam()],pointCfgItem.getPointName() )
				self.statusMsgToTongMember( camp, lastTongDBID, csstatus.BHZB_TEAM_PROTECT_POINT_FAIL,teamArgs )
				self.addBHZBWarMsgData( camp, lastTongDBID, csstatus.BHZB_TEAM_PROTECT_POINT_FAIL,teamArgs )
		if pointItem.getNotifyID() > 0:
			self.popTimer(pointItem.getNotifyID())
			pointItem.setNotifyID(0)
		self.setBHZBPointState( camp, pointItem,csdefine.NPCEXTPOINT_STATE_REST )
		pointItem.clearPointJoinAttackMembers()
		pointItem.clearPointJoinProtectMembers()
		tongDBIDs = list(self.getCampWarItem( camp ).getWarTong().keys())
		pointItem.setIsEnterDefense(False)
		restEndTime = Functions.getTime()
		if pointCfgItem:
			restEndTime = int( pointCfgItem.getRestTime() * csconst.TIME_ENLARGE_MULTIPLE ) + Functions.getTime()
		self.setBHZBPointRestEndTime( camp, pointItem, str(restEndTime) )
		self.addTimerCallBack( pointCfgItem.getRestTime(), "setBHZBPointState",( camp, pointItem, csdefine.NPCEXTPOINT_STATE_CAN_BE_DECLARE ) )
		if lastTongDBID:
			KBEngine.globalData["TongMgr"].onBHZBPointWarEnd( lastTongDBID, pointItem.getPointIndex() )
			for spaceScriptID in self.getAllBHZBSpaceScriptID():
				if pointItem.getJoinProtectGroupTeam() > 0:
					KBEngine.globalData["SpaceManager"].remoteCallDomain(spaceScriptID, "removeBHZBWarDetailTeamData",( camp,lastTongDBID, pointItem.getJoinProtectGroupTeam())  )
			for spaceScriptID in self.getAllBHZBSpaceScriptID():
					KBEngine.globalData["SpaceManager"].remoteCallDomain(spaceScriptID,"removeBHZBWarrDetailOccupyPoint",( camp, lastTongDBID, pointIndex ))
		if tongDBID:
			KBEngine.globalData["TongMgr"].onBHZBPointWarEnd( tongDBID, pointItem.getPointIndex() )
			for spaceScriptID in self.getAllBHZBSpaceScriptID():
				KBEngine.globalData["SpaceManager"].remoteCallDomain(spaceScriptID, "removeBHZBWarDetailTeamData",( camp,tongDBID, groupID)  )
		pointItem.setJoinProtectGroupTeam( 0 )
		KBEngine.globalData["SpaceManager"].remoteCallDomain( csconst.BHZB_HOME_BARRACKS_SPACE[0],"updataBHZBPointJoinProtectTeamID",( camp,tongDBIDs, pointItem.getPointIndex(),pointItem.getJoinProtectGroupTeam()))

	def setBHZBPointOccupyData( self, camp ,pointItem ):
		"""
		设置帮会争霸据点占领数据
		"""
		tongDBIDs = list(self.getCampWarItem( camp ).getWarTong().keys())
		playerDBID = pointItem.getPointDeclarePlayerDBID()
		playerName = pointItem.getPointtDeclarePlayerName()
		tongDBID = pointItem.getPointDeclareTongDBID()
		tongName = pointItem.getPointDeclareTongName()
		pointItem.setPointOccupyData( playerDBID,playerName,tongDBID,tongName )
		pointItem.setPointDeclareData( 0,0,"","",0,0 )
		KBEngine.globalData["SpaceManager"].remoteCallDomain( csconst.BHZB_HOME_BARRACKS_SPACE[0],"updataNPCPointOccupyData",( camp,tongDBIDs, pointItem.getPointIndex(),playerDBID,playerName,tongDBID,tongName )),

	def setBHZBPointRestEndTime( self, camp, pointItem, restEndTime ):
		"""
		设置帮会争霸据点结束时间
		"""
		tongDBIDs = list(self.getCampWarItem( camp ).getWarTong().keys())
		pointItem.setPointRestEndTime( restEndTime )
		KBEngine.globalData["SpaceManager"].remoteCallDomain( csconst.BHZB_HOME_BARRACKS_SPACE[0],"updataNPCPointRestEndTime",(camp,tongDBIDs,pointItem.getPointIndex(),restEndTime))

	def defenseBHZBPoint( self, tongDBID, camp, pointIndex, playerMB, groupID,playerDBIDs, tongMB ):
		"""
		布防帮会争霸据点
		"""
		if not KBEngine.globalData.get("BHZBStart",0):
			return
		if pointIndex not in self.getCampPointDatas( camp ):
			return
		pointItem = self.getCampPointDatas(camp)[pointIndex]
		if tongDBID != pointItem.getPointOccupyTongDBID():
			return

		if pointItem.getIsEnterDefense():
			playerMB.statusMessage( csstatus.BHZB_POINT_STATE_DEFENSE,"" )
			return
		# if playerDBID in self.getCampPointDatas(camp).getAllBHZBPointJoinAttackMembers():
		# 	playerMB.statusMessage( csstatus.BHZB_POINT_DEFENSE_FORBID_JOIN_ATTACK,"" )
		# 	return
		# if playerDBID in self.getCampPointDatas(camp).getAllBHZBPointJoinProtectMembers():
		# 	playerMB.statusMessage( csstatus.BHZB_POINT_DEFENSE_FORBID_JOIN_PROTECT,"" )
		# 	return

		restEndTime = pointItem.getPointRestEndTime()
		remainTime = int(Functions.convertTime( int(restEndTime) ) - time.time())
		if remainTime <= 0:
			return
		self.setBHZBPointState( camp, pointItem, csdefine.NPCEXTPOINT_STATE_DEFENSE )
		tongMB.setbhzbSignUpMembersIsActive( groupID,True, pointIndex )
		pointCfgItem = g_BHZBPointDataLoader.getBHZBPointItemByPointIndex( pointIndex )
		for spaceScriptID in self.getAllBHZBSpaceScriptID():
			KBEngine.globalData["SpaceManager"].remoteCallDomain(spaceScriptID, "updateBHZBWarDetailTeamData",( camp,tongDBID,groupID,pointIndex,pointItem.getPointDeclareWarState(),pointCfgItem.getPointName() ))
		spaceScriptID = pointCfgItem.getPointEnterPVPSpaceScriptID()
		pickArgs = {}
		pickArgs["camp"] = camp
		pickArgs["pointIndex"] = pointIndex
		pickArgs["belongTongDBID"] = tongDBID
		pickArgs["isEnterDefense"] = True
		pickArgs["spaceLife"] = remainTime
		pickArgs["groupID"] = groupID
		KBEngine.globalData["SpaceManager"].remoteCallDomain( csconst.BHZB_HOME_BARRACKS_SPACE[0], "defenseBHZBPoint", ( camp,tongDBID,spaceScriptID, pickArgs, playerDBIDs ) )
		pointItem.setIsEnterDefense( True )

	def saveBHZBPointSpaceInfo( self, camp, pointIndex, spaceSaveInfos, tongDBID, groupID ):
		"""
		保存帮会争霸据点布防数据
		"""
		self.getCampPointSpaceSaveInfoMgr( camp ).updataBHZBPointSpaceSaveInfo( pointIndex,spaceSaveInfos )
		self.writeToDB()

		KBEngine.globalData["TongMgr"].onBHZBPointWarEnd( tongDBID, pointIndex )
		for spaceScriptID in self.getAllBHZBSpaceScriptID():
			KBEngine.globalData["SpaceManager"].remoteCallDomain(spaceScriptID, "removeBHZBWarDetailTeamData",( camp,tongDBID, groupID)  )
		if pointIndex not in self.getCampPointDatas( camp ):
			return
		pointItem = self.getCampPointDatas(camp)[pointIndex]
		if pointItem.getPointDeclareWarState() == csdefine.NPCEXTPOINT_STATE_CAN_BE_DECLARE:
			return
		self.setBHZBPointState( camp, pointItem,csdefine.NPCEXTPOINT_STATE_REST )

	def requestBHZBPointSpaceSaveInfo( self, camp, pointIndex, spaceMB ):
		"""
		请求帮会争霸据点布防数据
		"""
		spaceSaveInfos = self.getCampPointSpaceSaveInfoMgr( camp ).getBHZBPointSpaceSaveInfo( pointIndex )
		spaceMB.requestBHZBPointSpaceSaveInfoCB( spaceSaveInfos )
		
	def occupyPointAddIntergral( self, camp, pointIndex, integral, repeatAddIntegral, repeatTime ):
		"""
		占领据点增加积分
		"""
		if pointIndex not in self.getCampPointDatas( camp ):
			return
		pointItem = self.getCampPointDatas(camp)[pointIndex]
		tongDBID = pointItem.getPointOccupyTongDBID()
		self.addTongIntegral( camp, tongDBID, integral )

		repeatAddIntegralID = pointItem.getRepeatAddIntegralID()
		if repeatAddIntegralID > 0:
			self.popTimer( repeatAddIntegralID )
			pointItem.setRepeatAddIntegralID( 0 )
		if repeatTime > 0:
			repeatID = self.addTimerRepeat( repeatTime,"addTongIntegral",( camp, tongDBID, repeatAddIntegral ) )
			pointItem.setRepeatAddIntegralID( repeatID )

	def showBHZBIntegralRankWin( self, camp, playerMB, delayCloseTime ):
		"""
		打开帮会争霸报名帮会排名
		"""
		KBEngine.globalData["BHZBStart"] = 0
		self.clearBHZBPointData( camp )
		tongIntegralRankList = list(self.getCampIntegralRankTongData( camp ).values())
		if hasattr( playerMB, "client" ) and playerMB.client:
			playerMB.client.ShowBHZBIntegralRankWin( tongIntegralRankList, delayCloseTime )

	def sendBHZBRewardToMembers( self,camp,tongDBID,memberDBIDs,firstRankRewardGifts,secondRankRewardGifts,thirdRankRewardGifts,rankRewardTongMoneys,rankRewardContributionGifts,firstTongLeaderReward,secondTongLeaderReward ):
		"""
		发送帮会争霸奖励给成员
		"""
		tongIntegralRankList = sorted(self.getCampIntegralRankTongData( camp ).values(), key = lambda x:x.integral, reverse= True)
		if not len(self.tongIntegralRankDBIDs):
			self.tongIntegralRankDBIDs = [ i.tongDBID for i in tongIntegralRankList ]
		if tongDBID not in self.tongIntegralRankDBIDs:
			return
		index = self.tongIntegralRankDBIDs.index( tongDBID )
		if len(rankRewardTongMoneys) > index:
			rankRewardTongMoney = rankRewardTongMoneys[index]
		else:
			rankRewardTongMoney = rankRewardTongMoneys[-1]
		if len( rankRewardContributionGifts ) > index:
			rankRewardContributionGift = rankRewardContributionGifts[index]
		else:
			rankRewardContributionGift = rankRewardContributionGifts[-1]

		allTongMemberDBIDs = []	
		tongItem = self.getCampWarItem( camp ).getWarTongItemByTongDBID( tongDBID )
		if tongItem != None:
			allTongMemberDBIDs = tongItem.getMembersDBIDList()

		if index == 0:
			self.recordReward[index] = ( tongDBID,firstTongLeaderReward,index )
			KBEngine.globalData["TongMgr"].sendBHZBRewardToMembers( tongDBID, allTongMemberDBIDs,firstRankRewardGifts, rankRewardTongMoney,rankRewardContributionGift, index )
		elif index == 1:
			self.recordReward[index] = ( tongDBID,secondTongLeaderReward,index )
			KBEngine.globalData["TongMgr"].sendBHZBRewardToMembers( tongDBID, allTongMemberDBIDs,secondRankRewardGifts, rankRewardTongMoney,rankRewardContributionGift, index )
		elif index == 2:
			self.recordReward[index] = ( tongDBID,"",index )
			KBEngine.globalData["TongMgr"].sendBHZBRewardToMembers( tongDBID, allTongMemberDBIDs,thirdRankRewardGifts, rankRewardTongMoney,rankRewardContributionGift, index )
		else:
			KBEngine.globalData["TongMgr"].sendBHZBRewardToMembers( tongDBID, allTongMemberDBIDs,[], rankRewardTongMoney, rankRewardContributionGift, index )
		if self.sendTongRewardTimerID <= 0:
			self.sendTongRewardTimerID = self.addTimerCallBack(2.0,"sendTongLeaderReward",())

	def sendTongLeaderReward( self ):
		"""
		发送帮主奖励
		"""
		self.calcAllBHZBTongIntegral()
		if len( self.recordReward ):
			for rank in range(0,len(self.recordReward)):
				KBEngine.globalData["TongMgr"].sendTongLeaderReward( self.recordReward[rank][0],self.recordReward[rank][1],self.recordReward[rank][2] )
			self.recordReward.clear()
			self.sendTongRewardTimerID = 0

		side = random.randint( csdefine.BELONG_SIDE_ATTACK, csdefine.BELONG_SIDE_PROTECT )
		if side == csdefine.BELONG_SIDE_ATTACK:
			otherSide = csdefine.BELONG_SIDE_PROTECT
		else:
			otherSide = csdefine.BELONG_SIDE_ATTACK
		taosimTongObj = self.getBHZBFirstRankByCamp( csdefine.CAMP_TAOSIM )
		demonTongObj = self.getBHZBFirstRankByCamp( csdefine.CAMP_DEMON )
		
		self.globalWoldBHZBRank(csdefine.CAMP_TAOSIM,taosimTongObj)
		self.globalWoldBHZBRank(csdefine.CAMP_DEMON,demonTongObj)
		allTongIntegralList = sorted(self.allTongIntegralMgr.items(),key = lambda x:x[0],reverse = False)
		tempAllTongIntegralList = allTongIntegralList[len(allTongIntegralList) // 4 * 4:]
		if len(tempAllTongIntegralList) == 3:
			self.globalWoldBHZBJoinCampWar( csdefine.CAMP_TAOSIM,taosimTongObj )
			self.globalWoldBHZBJoinCampWar( csdefine.CAMP_DEMON,demonTongObj )
			self.globalWoldBHZBSendToJoinCampWarMail( taosimTongObj, side )
			self.globalWoldBHZBSendToJoinCampWarMail( demonTongObj, otherSide )

	def getBHZBFirstRankByCamp( self, camp ):
		"""
		获得帮会争霸阵营第一名
		"""
		tempTongRanks = []
		allTongIntegralList = sorted(self.allTongIntegralMgr.items(),key = lambda x:x[0],reverse = False)
		tempAllTongIntegralList = allTongIntegralList[len(allTongIntegralList) // 4 * 4:]
		for tempTongIntegralData in tempAllTongIntegralList:
			for tongObj in tempTongIntegralData[1].values():
				if tongObj.getCamp() == camp:
					tempTongRanks.append( tongObj )
		tongRanks = sorted( tempTongRanks, key= lambda x:x.getBHZBTongTotalIntegral(),reverse= True )
		if tongRanks:
			return tongRanks[0]
		return None		

	def globalWoldBHZBRank( self, camp, tongObj ):
		"""
		广播帮会争霸排行
		"""	
		if tongObj != None:
			tongName = tongObj.getTongName()
			if camp == csdefine.CAMP_TAOSIM:
				campStr = cschannel_msgs.CAMP_TAOSIM
			else:
				campStr = cschannel_msgs.CAMP_DEMON
			msg = tongName + "|" + campStr + "|" + str( tongObj.getBHZBTongTotalIntegral() )
			KST.g_baseAppEntity.globalWold( csstatus.BHZB_END_GLOBALWOLD_RANK, msg )

	def globalWoldBHZBJoinCampWar( self, camp, tongObj ):
		"""
		广播参与阵营争霸战场
		"""
		if tongObj != None:
			tongName = tongObj.getTongName()
			if camp == csdefine.CAMP_TAOSIM:
				campStr = cschannel_msgs.CAMP_TAOSIM
				enemyCampStr = cschannel_msgs.CAMP_DEMON
			else:
				campStr = cschannel_msgs.CAMP_DEMON
				enemyCampStr = cschannel_msgs.CAMP_TAOSIM
			tempMsg = campStr + "|" + tongName + "|" + campStr + "|" + campStr + "|" + campStr + "|" + enemyCampStr
			KST.g_baseAppEntity.globalWold( csstatus.BHZB_END_GLOBALWOLD_TO_JOIN_CAMP_WAR, tempMsg  )
	
	def globalWoldBHZBSendToJoinCampWarMail( self, tongObj, side ):
		"""
		发送邮件
		"""
		if tongObj != None:
			date = datetime.datetime.now() + datetime.timedelta( days = 7 )
			KBEngine.globalData["TongMgr"].sendToJoinCampWarMail(tongObj.getTongDBID(),date.month, date.day, side)

	def statusMsgToTongMember( self, camp,tongDBID, msgID, msgArgs ):
		"""
		给某个帮会发送消息给成员
		"""
		KBEngine.globalData["SpaceManager"].remoteCallDomain( csconst.BHZB_HOME_BARRACKS_SPACE[0],"statusMsgToTongMember",(camp,tongDBID,msgID,msgArgs))
		for spaceScriptID in g_BHZBPointDataLoader.getAllBHZBPVEAndPVPSpace():
			KBEngine.globalData["SpaceManager"].remoteCallDomain(spaceScriptID, "statusMsgToTongMember",( camp,tongDBID,msgID,msgArgs ))

	def statusMsgToAllMember( self, camp, msgID, msgArgs ):
		"""
		给所有成员发送消息
		"""
		KBEngine.globalData["SpaceManager"].remoteCallDomain( csconst.BHZB_HOME_BARRACKS_SPACE[0],"statusMsgToAllMember",(camp,msgID,msgArgs))

		for spaceScriptID in g_BHZBPointDataLoader.getAllBHZBPVEAndPVPSpace():
			KBEngine.globalData["SpaceManager"].remoteCallDomain(spaceScriptID, "statusMsgToAllMember",( camp,msgID,msgArgs ))

	def getAllBHZBSpaceScriptID( self ):
		"""
		"""
		pointSpace = g_BHZBPointDataLoader.getAllBHZBPVEAndPVPSpace()
		pointSpace.extend( list(set(csconst.BHZB_HOME_BARRACKS_SPACE)) ) 
		return pointSpace

	def addBHZBWarMsgData( self, camp,tongDBID, statusID, statusArgs ):
		"""
		增加帮会争霸详情提示消息数据
		"""
		for spaceScriptID in self.getAllBHZBSpaceScriptID():
			KBEngine.globalData["SpaceManager"].remoteCallDomain(spaceScriptID,"addBHZBWarMsgData",( camp,tongDBID, statusID, statusArgs ))

	def checkIsLoginToBHZBPoint( self, roleMB, tongDBID, spaceScriptID,playerDBID, groupID, pointIndex ):
		"""
		检查是否重新进入帮会争霸据点
		"""
		if pointIndex:
			self.OnLoginToBHZBPoint( roleMB, groupID, pointIndex, spaceScriptID,tongDBID, playerDBID )

	def OnLoginToBHZBPoint( self, roleMB, groupID, pointIndex, spaceScriptID,tongDBID,playerDBID ):
		"""
		"""
		camp = csconst.BHZB_HOME_BARRACKS_SPACE.index( spaceScriptID ) + 1
		if pointIndex not in self.getCampPointDatas( camp ):
			return
		pointItem = self.getCampPointDatas(camp)[pointIndex]
		pointCfgItem = g_BHZBPointDataLoader.getBHZBPointItemByPointIndex( pointIndex )
		if pointItem.getPointOccupyTongDBID() > 0:
			pointScriptID = pointCfgItem.getPointEnterPVPSpaceScriptID()
		else:
			pointScriptID = pointCfgItem.getPointEnterPVESpaceScriptID()

		spaceObj = KST.g_objFactory.getSpaceObject( pointScriptID )
		tempDict = self.getPointDataByPointIndex( camp, pointIndex )
		declareTongDBID = tempDict.get("declareTongDBID")
		if tongDBID == declareTongDBID:
			enterInfo = spaceObj.getAttackEnterInfo()
			tempDict.update( {"belongSide":csdefine.BELONG_SIDE_ATTACK} )
		else:
			enterInfo = spaceObj.getProtectEnterInfo()
			tempDict.update( {"belongSide":csdefine.BELONG_SIDE_PROTECT} )

		tempDict.update( {"belongType":csdefine.SPACE_BELONG_NORMAL} )
		tempDict.update( {"playerDBID":playerDBID} )
		tempDict.update( {"spaceKey":"{0}|{1}|{2}".format(camp, pointIndex, pointItem.getPointOccupyTongDBID() )} )
		roleMB.cell.gotoSpaceUseArg( pointScriptID, enterInfo[0],enterInfo[1],tempDict)

	def onBHZBMemberOffLine( self, tongDBID, camp, pointIndex, groupID, tongMB ):
		"""
		帮会争霸成员下线
		"""
		if pointIndex not in self.getCampPointDatas( camp ):
			return
		pointItem = self.getCampPointDatas(camp)[pointIndex]
		if pointItem.getPointDeclareWarState() != csdefine.NPCEXTPOINT_STATE_CAN_NOT_BE_DECLARE:
			return
		self.cancelDeclareBHZBPoint( tongDBID, camp, pointIndex, groupID,tongMB )

	def requestOpenBHZBNpcPointMap( self, camp, roleMB ):
		"""
		请求打开据点大地图
		"""
		if hasattr(roleMB,"client") and roleMB.client:
			roleMB.client.InitBHZBNPCPointDatas( list(self.getCampPointDatas( camp ).values()) )
		
	def bhzbTeamMemberLoginOut( self, camp, tongDBID, playerDBID ):
		"""
		帮会争霸组队成员下线
		"""
		self.getCampWarItem( camp ).bhzbTeamMemberLoginOut(tongDBID,playerDBID)

	def queryAllBHZBIntegralData( self, playerMB, npcID ):
		"""
		查询帮会争霸历史战报
		"""
		allBHZBTongIntegralDatas = []
		for startTimes, tempTongIntegralData in self.allTongIntegralMgr.items():
			tongIntegralRankList = sorted(tempTongIntegralData.values(), key = lambda x:x.integral, reverse= True)
			allBHZBTongIntegralDatas.extend( tongIntegralRankList )

		if hasattr( playerMB, "client" ) and playerMB.client:
			playerMB.client.QueryAllBHZBIntegralData( allBHZBTongIntegralDatas, npcID )

	def gmAddBHZBTongIntegralRecordStartTimes( self,cmd ):
		"""
		增加帮会争霸战报记录
		"""
		allTongIntegralList = sorted(self.allTongIntegralMgr.items(),key = lambda x:x[0],reverse = False)
		if allTongIntegralList:
			self.currentStartTimes = str(int(allTongIntegralList[-1][0]) + 1)
		else:
			if len(str( datetime.datetime.now().month)) == 1:
				month = "0" + str( datetime.datetime.now().month)
			else:
				month = str( datetime.datetime.now().month)
			if len(str( datetime.datetime.now().day)) == 1:
				day = "0" + str( datetime.datetime.now().day)
			else:
				day = str( datetime.datetime.now().day)

			self.currentStartTimes = str( datetime.datetime.now().year) + month + day

	def gmClearBHZBTongIntegralRecord( self,cmd ):
		"""
		清除帮会争霸战报记录
		"""
		self.allTongIntegralMgr.clear()
