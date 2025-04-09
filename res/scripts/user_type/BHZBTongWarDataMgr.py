# -*- coding: utf-8 -*-

import KBEDebug
import csstatus
import csdefine
from WarMemberInfo import WarMemberInfo

class BHZBTongWarData( object ):
	"""
	帮会争霸 帮会数据
	"""
	def __init__( self, tongName = "", tongDBID = 0, belongSide = 0 ):
		self.tongDBID = tongDBID
		self.tongName = tongName
		self.belongSide = belongSide
		self.members = {}

	def initData( self, dict ):
		self.tongDBID = dict["tongDBID"]
		self.tongName = dict["tongName"]
		for memberData in dict["members"]:
			self.members[memberData.roleDBID] = memberData

	def addMember( self, id,mailBox, name ):
		"""
		增加成员
		"""
		m = WarMemberInfo( mailBox.id, mailBox, id, name, self.belongSide )
		self.members[id] = m
		return self.members[id]

	def addMemberOnLogin( self, id, mailBox ):
		"""
		重登添加成员
		"""
		if id in self.members:
			member = self.members[id]
			del self.members[id]
			srcMemberID = member.roleID
			member.roleID = mailBox.id
			member.roleMB = mailBox
			self.members[id] = member
			return srcMemberID, self.members[id]
		return 0,None

	def hasMember( self, id ):
		"""
		是否有某成员
		"""
		if id in self.members:
			return True
		return False

	def getMember( self, id ):
		if id in self.members:
			return self.members[id]
		return None

	def getMemberByEntityID( self, entityID ):
		"""
		"""
		for id, member in self.members.items():
			if member.roleID == entityID:
				return self.tongDBID, id
		return None,None

	def addMemberKillEnemyNum( self, id):
		"""
		增加成员击杀数
		"""
		if id in self.members:
			self.members[id].addMemberKillEnemyNum()
			return self.members[id]
		return None

	def addMemberDeadNum( self, id ):
		"""
		增加成员死亡数
		"""
		if id in self.members:
			self.members[id].addMemberDeadNum()
			return self.members[id]
		return None

	def addMemberAssistsNum( self, id ):
		"""
		增加成员助攻数
		"""
		if id in self.members:
			self.members[id].addMemberAssistsNum()
			return self.members[id]
		return None

	def addMemberKillSoldierNum( self, id ):
		"""
		增加成员击杀士兵数
		"""
		if id in self.members:
			self.members[id].addMemberKillSoldierNum()
			return self.members[id]
		return None

	def addMemberSoldierDeadNum( self, id ):
		"""
		增加成员小兵死亡数
		"""
		if id in self.members:
			self.members[id].addMemberSoldierDeadNum()
			return self.members[id]
		return None


	def getTongName( self ):
		"""
		"""
		return self.tongName

	def getAllTongMembers( self ):
		"""
		"""
		return list(self.members.values())

	def getDictFromObj( self, obj ):
		tempDict = {}
		tempDict[ "members" ] = []
		tempDict["tongDBID"] = obj.tongDBID
		tempDict["tongName"] = obj.tongName
		tempDict["belongSide"] = obj.belongSide
		for mObj in obj.members.values():
			tempDict[ "members" ].append( mObj )
			
		return tempDict
	
	def createObjFromDict( self, dict ):
		obj = BHZBTongWarData()
		obj.initData( dict )
		return obj
		
	def isSameType( self, obj ):
		return isinstance( obj, BHZBTongWarData )


class BHZBTongWarDataMgr( dict ):
	"""
	帮会争霸 帮会数据管理器
	"""
	def __init__( self ):
		pass
	
	def initData( self, dict ):
		for m  in dict[ "datas" ]:
			self[ m.tongDBID ] = m

	def addMember( self, tongName,tongDBID,belongSide, id,mailBox, name, enemyTongName ):
		"""
		增加成员
		"""
		if tongDBID not in self:
			self[tongDBID] = BHZBTongWarData( tongName,tongDBID,belongSide )

		if self[tongDBID].hasMember( id ):
			srcMemberID, member = self[tongDBID].addMemberOnLogin( id, mailBox )
			if srcMemberID <= 0:
				return
			self.updateGCZMemberDataToOtherClientOnLogin( srcMemberID, mailBox.id )
			self.receiveOtherMemberData( tongDBID, member, enemyTongName )
			return
		member = self[tongDBID].addMember( id, mailBox, name )
		self.updateMemberDataToOtherClient( tongDBID, member, enemyTongName )
		self.receiveOtherMemberData( tongDBID, member, enemyTongName )

	def addMemberKillEnemyNum( self, tongDBID, id ):
		"""
		增加成员击杀数
		"""
		if tongDBID not in self:
			return
		member = self[tongDBID].addMemberKillEnemyNum(id)
		if not member:
			return
		self.updateKillEnemyDataToClient( member )

	def addMemberDeadNum( self, tongDBID, id ):
		"""
		增加成员死亡数
		"""
		if tongDBID not in self:
			return
		member = self[tongDBID].addMemberDeadNum(id)
		if not member:
			return
		self.updateDeadDataToClient( member )

	def addMemberAssistsNum( self, tongDBID,id ):
		"""
		增加成员助攻数
		"""
		if tongDBID not in self:
			return
		member = self[tongDBID].addMemberAssistsNum(id)
		if not member:
			return
		self.updateAssistsDataToClient( member )

	def addMemberKillSoldierNum( self, tongDBID,id ):
		"""
		增加成员击杀士兵数
		"""
		if tongDBID not in self:
			return
		member = self[tongDBID].addMemberKillSoldierNum(id)
		if not member:
			return

		self.updateKillSoldierDataToClient( member )

	def addMemberSoldierDeadNum( self, tongDBID,id ):
		"""
		增加成员的士兵死亡数
		"""
		if tongDBID not in self:
			return
		member = self[tongDBID].addMemberSoldierDeadNum(id)
		if not member:
			return
		self.updateMemberSoldierDeadNumToClient( member )

	def updateGCZMemberDataToOtherClientOnLogin( self, srcMemberID, dstMemberID ):
		"""
		"""
		members = self.getAllHasClientMembers()
		for m in members:
			if m.roleMB and m.roleID != dstMemberID and m.roleMB.getClient():
				m.roleMB.client.CLIENT_UpdateGCZMemberDataToOtherClientOnLogin( srcMemberID, dstMemberID )

	def updateMemberDataToOtherClient( self, tongDBID, member,enemyTongName ):
		"""
		更新自己的成员数据到其他客户端
		"""
		name = self[tongDBID].getTongName()
		members = self.getAllHasClientMembers()
		for m in members:
			if m.roleMB and m.roleMB.getClient():
				m.roleMB.client.CLIENT_UpdateGCZMemberDataToOtherClient( member.roleID, member.roleName, member.belongSide, member.killEnemy, member.dead, member.assists,member.killSoldier,member.totalGetExploit,name,member.ownerSoldierDeadNum,enemyTongName )

	def receiveOtherMemberData( self, tongDBID, member,enemyTongName ):
		"""
		接收其他成员数据
		"""
		if tongDBID <= 0:
			return
		members = self.getAllMembers()
		for m in members:
			name = self.getBlongNameByBelongSide( m.belongSide )
			if m.roleMB and m.roleMB.getClient():
				member.roleMB.client.CLIENT_ReceiveGCZOtherMemberData( m.roleID, m.roleName, m.belongSide, m.killEnemy, m.dead, m.assists,m.killSoldier,m.totalGetExploit,name,m.ownerSoldierDeadNum,enemyTongName )

	def updateKillEnemyDataToClient( self, member ):
		"""
		更新击杀敌人数据到客户端
		"""
		members = self.getAllHasClientMembers()
		for m in members:
			if m.roleMB and m.roleMB.getClient():
				m.roleMB.client.CLIENT_UpdateGCZKillEnemyDataToClient( member.roleID, member.killEnemy )

	def updateKillSoldierDataToClient( self, member ):
		"""
		更新击杀士兵数据到客户端
		"""
		members = self.getAllHasClientMembers()
		for m in members:
			if m.roleMB and m.roleMB.getClient():
				m.roleMB.client.CLIENT_UpdateGCZKillSoldierDataToClient( member.roleID, member.killSoldier )

	def updateDeadDataToClient( self, member ):
		"""
		更新死亡数据到客户端
		"""
		members = self.getAllHasClientMembers()
		for m in members:
			if m.roleMB and m.roleMB.getClient():
				m.roleMB.client.CLIENT_UpdateGCZDeadDataToClient( member.roleID, member.dead )

	def updateAssistsDataToClient( self, member ):
		"""
		更新助攻数据到客户端
		"""
		members = self.getAllHasClientMembers()
		for m in members:
			if m.roleMB and m.roleMB.getClient():
				m.roleMB.client.CLIENT_UpdateGCZAssistsDataToClient( member.roleID, member.assists )

	def updateTotalGetExploitDataToClient( self, member ):
		"""
		更新军功数据到客户端
		"""
		members = self.getAllHasClientMembers()
		for m in members:
			if m.roleMB and m.roleMB.getClient():
				m.roleMB.client.CLIENT_UpdateGCZTotalExploitDataToClient( member.roleID, member.totalGetExploit )

	def updateMemberSoldierDeadNumToClient( self, member ):
		"""
		玩家小兵死亡数
		"""
		members = self.getAllHasClientMembers()
		for m in members:
			if m.roleMB and m.roleMB.getClient():
				m.roleMB.client.CLIENT_UpDateGCZMemberSoldierDeadNumToClient( member.roleID,member.ownerSoldierDeadNum )

	def getAllHasClientMembers( self ):
		"""
		获得所有有客户端的玩家 兼容PVE和PVP
		"""
		members = []
		tongDBIDs = [i for i in self.keys() if i > 0]
		for tongDBID in tongDBIDs:
			members.extend(self[tongDBID].getAllTongMembers())

		return members

	def getAllMembers( self ):
		"""
		获得所有成员数据
		"""
		members = []
		for tongDBID in self.keys():
			members.extend(self[tongDBID].getAllTongMembers())

		return members

	def getBlongNameByBelongSide( self, belongSide ):
		"""
		获得属于某一方的名称
		"""
		for tongObj in self.values():
			if tongObj.belongSide == belongSide:
				return tongObj.getTongName()
		return ""

	def getTongDBIDAndIDByEntityID( self, entityID ):
		"""
		获得帮会DBID 和ID 
		"""
		tongDBID = None
		id = None
		for tongObj in self.values():
			tongDBID,id = tongObj.getMemberByEntityID( entityID )
		return tongDBID,id

	def getBelongSideByTongDBID( self, tongDBID ):
		"""
		获得帮会DBID  和玩家PlayerDBID
		"""
		if tongDBID in self:
			return self[tongDBID].belongSide
		return 0

	def getMembersBySide( self, belongSide ):
		"""
		获得某一方的所有玩家
		"""
		members = []
		for tongObj in self.values():
			if tongObj.belongSide == belongSide:
				members.extend( tongObj.getAllTongMembers() )
		return members

	def getDictFromObj( self, obj ):
		tempDict = {}
		tempDict[ "datas" ] = []
		for mObj in obj.values():
			tempDict[ "datas" ].append( mObj )
			
		return tempDict
	
	def createObjFromDict( self, dict ):
		obj = BHZBTongWarDataMgr()
		obj.initData( dict )
		return obj
		
	def isSameType( self, obj ):
		return isinstance( obj, BHZBTongWarDataMgr )

g_BHZBTongWarDataMgr = BHZBTongWarDataMgr()
g_BHZBTongWarData = BHZBTongWarData()