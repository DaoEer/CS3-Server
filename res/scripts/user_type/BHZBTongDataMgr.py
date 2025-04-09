# -*- coding: utf-8 -*-

import KBEDebug
import csstatus
import csdefine

class BHZBMemberData( object ):
	"""
	帮会争霸成员数据
	"""
	def __init__( self, tongDBID = 0 , playerDBID = 0, groupID = 0, isCaptain = False ):
		"""
		"""
		self.tongDBID = tongDBID
		self.playerDBID = playerDBID
		self.groupID = groupID
		self.isCaptain = isCaptain

	def initData( self, dict ):
		"""
		"""
		self.tongDBID = dict["tongDBID"]
		self.playerDBID = dict["playerDBID"]
		self.groupID = dict["groupID"]
		self.isCaptain = bool(dict["isCaptain"])

	def getDictFromObj( self, obj ):
		dict = {
			"tongDBID":obj.tongDBID,
			"playerDBID":obj.playerDBID,
			"groupID":obj.groupID,
			"isCaptain":obj.isCaptain,
		}
		return dict

	def createObjFromDict( self, dict ):
		obj = self.__class__()
		obj.initData( dict )
		return obj

	def isSameType( self, obj ):
		return isinstance( obj, BHZBMemberData )


class BHZBTongData( object ):
	"""
	帮会争霸帮会数据
	"""
	def __init__( self, tongDBID = 0,tongName = "",tongLevel = 0,camp = 0,membersInfos = []):
		"""
		"""
		self.tongDBID = tongDBID
		self.tongName = tongName
		self.tongLevel = tongLevel
		self.camp = camp
		self.members = {} #{playerDBID:PlayerItem}
		for memberInfo in membersInfos:
			if not memberInfo.captainDBID:
				continue
			captainDBID = int(memberInfo.captainDBID)
			self.members[captainDBID] = BHZBMemberData(tongDBID,captainDBID,memberInfo.groupID,True)
			for memberDBID in memberInfo.memberDBIDs:
				if not memberDBID:
					continue
				self.members[int(memberDBID)] = BHZBMemberData(tongDBID,int(memberDBID),memberInfo.groupID,False)

	def initData( self, dict ):
		"""
		"""
		self.tongDBID = dict["tongDBID"]
		self.tongName = dict["tongName"]
		self.tongLevel = dict["tongLevel"]
		self.camp = dict["camp"]
		self.members = {}
		for memberObj in dict["members"]:
			self.members[memberObj.playerDBID] = memberObj

	def changeSignUpBHZBMember( self, signUpMembers ):
		"""
		"""
		self.members.clear()
		for memberInfo in signUpMembers:
			if not memberInfo.captainDBID:
				continue
			captainDBID = int(memberInfo.captainDBID)
			self.members[captainDBID] = BHZBMemberData(self.tongDBID,captainDBID,memberInfo.groupID,True)
			for memberDBID in memberInfo.memberDBIDs:
				if not memberDBID:
					continue
				self.members[int(memberDBID)] = BHZBMemberData(self.tongDBID,int(memberDBID),memberInfo.groupID,False)

	def getDictFromObj( self, obj ):
		dict = {
			"tongDBID" 	: obj.tongDBID,
			"tongName"	: obj.tongName,
			"tongLevel" : obj.tongLevel,
			"camp" : obj.camp,
			"members": list(obj.members.values()),
		}
		return dict
	
	def createObjFromDict( self, dict ):
		obj = self.__class__()
		obj.initData( dict )
		return obj
		
	def isSameType( self, obj ):
		return isinstance( obj, BHZBTongData )

class BHZBTongDataMgr( dict ):
	"""
	帮会争霸据点数据管理器
	"""
	def __init__( self ):
		pass
	
	def initData( self, dict ):
		for m in dict[ "datas" ]:
			self[ m.tongDBID ] = m

	def addWarTongData( self, camp,tongDBID, tongName, tongLevel, signUpMembers ):
		"""
		"""
		if tongDBID in self:
			del self[tongDBID]
		self[tongDBID] = BHZBTongData( tongDBID, tongName, tongLevel, camp, signUpMembers )

	def changeSignUpBHZBMember( self, tongDBID, signUpMembers ):
		"""
		改变报名帮会争霸成员
		"""
		if tongDBID in self:
			self[tongDBID].changeSignUpBHZBMember( signUpMembers )

	def removeTongData( self, tongDBID ):
		"""
		"""
		if tongDBID in self:
			del self[tongDBID]

	def getDictFromObj( self, obj ):
		tempDict = {}
		tempDict[ "datas" ] = []
		for mObj in list(obj.values()):
			tempDict["datas"].append( mObj )
		return tempDict
	
	def createObjFromDict( self, dict ):
		obj = BHZBTongDataMgr()
		obj.initData( dict )
		return obj
		
	def isSameType( self, obj ):
		return isinstance( obj, BHZBTongDataMgr )

g_BHZBTongDataMgr = BHZBTongDataMgr()
g_BHZBTongData = BHZBTongData()
g_BHZBMemberData = BHZBMemberData()