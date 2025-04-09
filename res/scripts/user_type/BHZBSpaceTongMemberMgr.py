# -*- coding: utf-8 -*-

import KBEDebug
import csstatus
import csdefine

class BHZBSpaceTongMember( object ):
	"""
	帮会争霸副本成员数据
	"""
	def __init__( self, roleDBID = 0 , groupID = 0, roleMB = None ):
		"""
		"""
		self.roleDBID = roleDBID
		self.groupID = groupID
		self.roleMB = roleMB

	def initData( self, dict ):
		"""
		"""
		self.roleDBID = dict["roleDBID"]
		self.groupID = dict["groupID"]
		self.roleMB = dict["roleMB"]

	def setGroupID( self, groupID ):
		"""
		"""
		self.groupID = groupID
		if self.roleMB and self.roleMB.getClient():
			self.roleMB.client.UpdataMyGroupIDToClient( self.groupID )

	def getGroupID( self ):
		return self.groupID

	def getDictFromObj( self, obj ):
		dict = {
			"roleDBID":obj.roleDBID,
			"groupID":obj.groupID,
			"roleMB":obj.roleMB,
		}
		return dict

	def createObjFromDict( self, dict ):
		obj = self.__class__()
		obj.initData( dict )
		return obj

	def isSameType( self, obj ):
		return isinstance( obj, BHZBSpaceTongMember )


class BHZBSpaceTongData( object ):
	"""
	帮会争霸副本帮会数据
	"""
	def __init__( self, tongDBID = 0):
		"""
		"""
		self.tongDBID = tongDBID
		self.commandAttacksDatas = {}
		self.commandProtectDatas = {}
		self.members = {}

	def addTongMemberData( self,roleDBID, roleMB, groupID ):
		"""
		增加帮会成员
		"""
		member = BHZBSpaceTongMember( roleDBID, groupID, roleMB )
		self.members[roleDBID] = member

	def updataMemberRoleMB( self, roleDBID,roleMB ):
		"""
		"""
		if roleDBID not in self.members:
			return
		self.members[roleDBID].roleMB = roleMB

	def updataCallTeamToProtect( self, groupTeamID, pointIndex ):
		"""
		召唤某一队去防守
		"""
		self.commandProtectDatas[pointIndex] = groupTeamID

	def updataCallTeamToAttack( self, groupTeamID, pointIndex ):
		"""
		召唤某一队去进攻
		"""
		self.commandAttacksDatas[pointIndex] = groupTeamID

	def isTeamToProtect( self, groupTeamID, pointIndex ):
		"""
		"""
		if pointIndex in self.commandProtectDatas:
			return self.commandProtectDatas[pointIndex] == groupTeamID
		return False

	def isTeamToAttack( self, groupTeamID, pointIndex ):
		"""
		"""
		if pointIndex in self.commandAttacksDatas:
			return self.commandAttacksDatas[pointIndex] == groupTeamID
		return False

	def getMemberGroupIDByPlayerDBID( self, roleDBID ):
		"""
		"""
		if roleDBID in self.members:
			return self.members[roleDBID].groupID
		return -1

	def isInMembers( self, roleDBID ):
		"""
		"""
		if roleDBID in self.members:
			return True
		return False

	def getAllMembers( self ):
		"""
		获得所有所有成员
		"""
		return list(self.members.values())

	def getAllMemberDBIDs( self ):
		"""
		"""
		return list( self.members.keys() )

	def initData( self, dict ):
		"""
		"""
		self.tongDBID = dict["tongDBID"]
		self.commandAttacksDatas = dict["commandAttacksDatas"]
		self.commandProtectDatas = dict["commandProtectDatas"]
		for member in dict["members"]:
			self.members[member.roleDBID] = member

	def getDictFromObj( self, obj ):
		dict = {
			"tongDBID" 	: obj.tongDBID,
			"commandAttacksDatas"	: obj.commandAttacksDatas,
			"commandProtectDatas" : obj.commandProtectDatas,
			"members": list( obj.members.values() ),
		}
		return dict
	
	def createObjFromDict( self, dict ):
		obj = self.__class__()
		obj.initData( dict )
		return obj
		
	def isSameType( self, obj ):
		return isinstance( obj, BHZBSpaceTongData )

class BHZBSpaceTongMemberMgr( dict ):
	"""
	帮会争霸副本帮会数据管理器
	"""
	def __init__( self ):
		pass
	
	def initData( self, dict ):
		for m in dict[ "datas" ]:
			self[ m.tongDBID ] = m

	def addTongMemberData( self, tongDBID, roleDBID, roleMB, groupID ):
		"""
		帮会成员数据
		"""
		if tongDBID not in self:
			self[tongDBID] = BHZBSpaceTongData( tongDBID )

		if self[tongDBID].isInMembers( roleDBID ):
			self[tongDBID].updataMemberRoleMB( roleDBID,roleMB )
		else:
			self[tongDBID].addTongMemberData( roleDBID, roleMB, groupID )
		self.receiveAllProtectData(tongDBID,roleMB)
		self.receiveAllAttackData(tongDBID,roleMB)
		if roleMB.getClient():
			roleMB.client.UpdataMyGroupIDToClient( groupID )

	def callTeamToProtect( self, tongDBID,groupTeamID, pointIndex, pointName ):
		"""
		召唤某一队去防守
		"""
		if tongDBID not in self:
			return
		self[tongDBID].updataCallTeamToProtect( groupTeamID, pointIndex )
		self.updataToTongMemberClientProtectData( tongDBID,groupTeamID, pointIndex,pointName )

	def callTeamToAttack( self, tongDBID, groupTeamID, pointIndex,pointName ):
		"""
		召唤某一队去进攻
		"""
		if tongDBID not in self:
			return
		self[tongDBID].updataCallTeamToAttack( groupTeamID, pointIndex )
		self.updataToTongMemberClientAttackData( tongDBID,groupTeamID, pointIndex,pointName )

	def isTeamToProtect( self, tongDBID,groupTeamID, pointIndex ):
		"""
		"""
		if tongDBID not in self:
			return False
		return self[tongDBID].isTeamToProtect( groupTeamID, pointIndex )

	def isTeamToAttack( self, tongDBID,groupTeamID, pointIndex ):
		"""
		"""
		if tongDBID not in self:
			return False
		return self[tongDBID].isTeamToAttack( groupTeamID, pointIndex )

	def changeMemberGroup( self, tongDBID, groupDict ):
		"""
		改变成员分组
		"""
		if tongDBID not in self:
			return
		
		for groupID, playerDBIDs in groupDict.items():
			for playerDBID in playerDBIDs:
				if playerDBID not in self[tongDBID].members:
					continue
				self[tongDBID].members[playerDBID].setGroupID(groupID)

		totalPlayerDBIDs = []
		for playerDBIDs in groupDict.values():
			totalPlayerDBIDs.extend( playerDBIDs )

		for playerDBID, member in self[tongDBID].members.items():
			if playerDBID not in totalPlayerDBIDs:
				member.setGroupID(0)

	def receiveAllProtectData( self, tongDBID, roleMB ):
		"""
		接受所有队伍的防守数据到客户端
		"""
		if tongDBID not in self:
			return
		for pointIndex, groupTeamID in self[tongDBID].commandProtectDatas.items():
			if roleMB.getClient():
				roleMB.client.UpdataToTongMemberClientProtectData( groupTeamID, pointIndex )

	def receiveAllAttackData( self, tongDBID, roleMB ):
		"""
		更新所有队伍的进攻数据到客户端
		"""
		if tongDBID not in self:
			return
		for pointIndex, groupTeamID in self[tongDBID].commandAttacksDatas.items():
			if roleMB.getClient():
				roleMB.client.UpdataToTongMemberClientAttackData( groupTeamID, pointIndex )

	def updataToTongMemberClientProtectData( self, tongDBID,groupTeamID, pointIndex,pointName ):
		"""
		将防守数据发送到客户端
		"""
		if tongDBID not in self:
			return

		for member in self[tongDBID].getAllMembers():
			if member.roleMB and member.roleMB.getClient() and groupTeamID > 0 and member.groupID == groupTeamID:
				member.roleMB.client.statusMessage( csstatus.BHZB_TONG_CALL_TO_PROTECT_POINT, pointName )
			if member.roleMB and member.roleMB.getClient():
				member.roleMB.client.UpdataToTongMemberClientProtectData( groupTeamID, pointIndex )

	def updataToTongMemberClientAttackData( self, tongDBID,groupTeamID, pointIndex,pointName ):
		"""
		将进攻数据发送到客户端
		"""
		if tongDBID not in self:
			return
		for member in self[tongDBID].getAllMembers():
			if member.roleMB and member.roleMB.getClient() and groupTeamID > 0 and member.groupID == groupTeamID:
				member.roleMB.client.statusMessage( csstatus.BHZB_TONG_CALL_TO_ATTACK_POINT, pointName )
			if member.roleMB and member.roleMB.getClient():
				member.roleMB.client.UpdataToTongMemberClientAttackData( groupTeamID,pointIndex )

	def getMemberGroupIDByPlayerDBID( self, tongDBID, roleDBID ):
		"""
		获得玩家所在的组
		"""
		if tongDBID in self:
			return self[tongDBID].getMemberGroupIDByPlayerDBID( roleDBID )
		return 0

	def getMemberByPlayerDBID( self, tongDBID, roleDBID ):
		"""
		"""
		if tongDBID in self:
			return self[tongDBID].members.get( roleDBID, None )
		return None

	def getTongAllMemberByTongDBID( self, tongDBID ):
		"""
		获得某帮会的所有成员
		"""
		if tongDBID in self:
			return self[tongDBID].getAllMembers()
		return []

	def getTongAllMemberDBIDsByTongDBID( self, tongDBID ):
		if tongDBID in self:
			return self[tongDBID].getAllMemberDBIDs()

		return []

	def getAllMembers( self ):
		"""
		获得所有成员
		"""
		totalMembers = []
		for tongObj in self.values():
			totalMembers.extend(tongObj.getAllMembers())

		return totalMembers

	def getDictFromObj( self, obj ):
		tempDict = {}
		tempDict[ "datas" ] = []
		for mObj in list(obj.values()):
			tempDict["datas"].append( mObj )
		return tempDict
	
	def createObjFromDict( self, dict ):
		obj = BHZBSpaceTongMemberMgr()
		obj.initData( dict )
		return obj
		
	def isSameType( self, obj ):
		return isinstance( obj, BHZBSpaceTongMemberMgr )

g_BHZBSpaceTongMemberMgr = BHZBSpaceTongMemberMgr()
g_BHZBSpaceTongData = BHZBSpaceTongData()
g_BHZBSpaceTongMember = BHZBSpaceTongMember()