# -*- coding: utf-8 -*-

import KBEDebug
import csdefine

class TongCampWarMemberInfo:
	"""
	帮会阵营战  玩家数据
	"""
	def __init__( self ):
		self.dbid = 0
		self.mailbox = None
		self.tongDBID = 0
		self.jinYuan = 0
	
	def initData( self, dbid, mailbox, tongDBID ):
		self.dbid = dbid
		self.mailbox = mailbox
		self.tongDBID = tongDBID

	def getDictFromObj( self, obj ):
		tempDict = {}
		tempDict["dbid"] = obj.dbid
		tempDict["mailbox"] = obj.mailbox
		tempDict["tongDBID"] = obj.tongDBID
		tempDict["jinYuan"] = obj.jinYuan
		return tempDict
	
	def createObjFromDict( self, dict ):
		obj = TongCampWarMemberInfo()
		obj.dbid = dict["dbid"]
		obj.mailbox = dict["mailbox"]
		obj.tongDBID = dict["tongDBID"]
		obj.jinYuan = dict["jinYuan"]
		return obj
		
	def isSameType( self, obj ):
		return isinstance( obj, TongCampWarMemberInfo )

class TongCampWarBaseInfo:
	"""
	帮会阵营战 帮会数据
	"""
	def __init__( self ):
		self.tongDBID = 0
		self.members = {}
		self.tongName = ""
		self.jinYuan = 0
		self.totalCallNumber = 0
		self.tongLevel = 0
		self.camp = 0
	
	def init( self, tongDBID, tongName, tongLevel, jinYuan, totalCallNumber, camp):
		self.tongDBID = tongDBID
		self.tongName = tongName
		self.tongLevel = tongLevel
		self.jinYuan = jinYuan
		self.totalCallNumber = totalCallNumber
		self.camp = camp

	def initData( self, dict ):
		self.tongDBID = dict["tongDBID"]
		self.tongName = dict["tongName"]
		self.tongLevel = dict["tongLevel"]
		self.jinYuan = dict["jinYuan"]
		self.totalCallNumber = dict["totalCallNumber"]
		for m in dict["members"]:
			self.members[ m.dbid ] = m

	def addMember( self, dbid, mailbox, tongDBID ):
		"""
		"""
		if dbid in self.members:
			member = self.members[dbid]
			member.mailbox = mailbox
			return
		member = TongStarcraftMember()
		member.initData(dbid, mailbox,tongDBID )
		self.members[member.dbid] = member

	def removeMember( self, dbid ):
		"""
		"""
		if dbid in self.members:
			del self.members[dbid]

	def getMember( self, dbid ):
		"""
		获得成员
		"""
		return self.members.get(dbid,None)

	def getMembers( self ):
		"""
		获得所有成员
		"""
		return list(self.members.values())

	def getDictFromObj( self, obj ):
		dict = {}
		dict[ "tongDBID" ] = obj.tongDBID
		dict[ "members" ] = list(obj.members.values())
		dict["tongLevel"] = obj.tongLevel
		dict["tongName"] = obj.tongName
		dict["camp"] = obj.camp
		dict["jinYuan"] = obj.jinYuan
		dict["totalCallNumber"] = obj.totalCallNumber
		return dict
	
	def createObjFromDict( self, dict ):
		obj = TongCampWarBaseInfo()
		obj.initData( dict )
		return obj
		
	def isSameType( self, obj ):
		return isinstance( obj, TongCampWarBaseInfo )

class TongCampWarBaseInfos( dict ):
	"""
	帮会阵营战 帮会数据管理器
	"""
	def __init__( self ):
		pass
	
	def initData( self, dict ):
		for m  in dict[ "datas" ]:
			self[ m.tongDBID ] = m

	def addMember( self, tongDBID, tongName,dbid, mailbox, tongLevel, jinYuan,totalCallNumber,camp ):
		"""
		"""
		if tongDBID in self.keys():
			tongInfo = self[tongDBID]
		else:
			tongInfo = TongCampWarBaseInfo()
			tongInfo.init( tongDBID,tongName, tongLevel, jinYuan,totalCallNumber, camp )
			self[tongDBID] = tongInfo
		tongInfo.addMember( dbid,mailbox,tongDBID )
	
	def getMember( self, tongDBID, dbid ):
		"""
		获得成员
		"""
		if tongDBID not in self.keys():
			return None
		return self[tongDBID].getMember( dbid )

	def getMembers( self ):
		"""
		获得所有成员
		"""
		members = []
		for tong in self.values():
			members.extend(tong.getMembers())

		return members

	def getTongDBIDByEntityID( self, entityID ):
		"""
		通过entityID获得
		"""
		for tong in self.values():
			member = tong.getMemberByEntityID()
			if member:
				return member
		return None

	def getAllTongs( self ):
		return list(self.keys())

	def getDictFromObj( self, obj ):
		tempDict = {}
		tempDict[ "datas" ] = []
		
		for mObj in obj.values():
			tempDict[ "datas" ].append( mObj )
			
		return tempDict
	
	def createObjFromDict( self, dict ):
		obj = TongCampWarBaseInfos()
		obj.initData( dict )
		return obj
		
	def isSameType( self, obj ):
		return isinstance( obj, TongCampWarBaseInfos )

g_TongCampWarBaseInfos = TongCampWarBaseInfos()
g_TongCampWarBaseInfo = TongCampWarBaseInfo()
g_TongCampWarMemberInfo = TongCampWarMemberInfo()