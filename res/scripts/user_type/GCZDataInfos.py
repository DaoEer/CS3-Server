# -*- coding: utf-8 -*-

import KBEDebug
import csstatus
import csdefine
from WarMemberInfo import WarMemberInfo

class GCZMemberInfoMgr( dict ):
	"""
	攻城战 成员数据管理器
	"""
	def __init__( self ):
		self.protectName = ""
		self.attackName = ""
	
	def initData( self, dict ):
		self.protectName = dict["protectName"]
		self.attackName = dict["attackName"]
		for m  in dict[ "members" ]:
			self[ m.roleDBID ] = m

	def addMember( self, id,mailBox, name, belongSide, protectName = "", attackName = "" ):
		"""
		"""
		if protectName != "":
			self.protectName = protectName
		if attackName != "":
			self.attackName = attackName
		# if mailBox.getEntityFlag() != csdefine.ENTITY_FLAG_ROLE and self.getMemberByName( name ) != None:
		# 	member = self.getMemberByName( name )
		# 	del self[member.roleDBID]
		# 	srcMemberID = member.roleID
		# 	member.roleID = id
		# 	member.roleMB = mailBox
		# 	member.roleDBID = id
		# 	self[id] = member
		# 	self.updateGCZMemberDataToOtherClientOnLogin( srcMemberID, id )
		# 	return
		if id == 0 and mailBox != None and mailBox.getEntityFlag() == csdefine.ENTITY_FLAG_MONSTER:
			m = WarMemberInfo( id, mailBox, id,name,belongSide )
			self[id] = m
			self.updateGCZMemberDataToOtherClient(m)
			self.receiveGCZOtherMemberData(m)
			return
		if id in self and mailBox != None and mailBox.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE:
			member = self[id]
			del self[id]
			srcMemberID = member.roleID
			member.roleID = mailBox.id
			member.roleMB = mailBox
			self[id] = member
			self.updateGCZMemberDataToOtherClientOnLogin( srcMemberID, mailBox.id )
			self.receiveGCZOtherMemberData( member )
			return
		if mailBox == None:
			m = WarMemberInfo( id, mailBox, id,name,belongSide )
		else:
			m = WarMemberInfo( mailBox.id, mailBox, id,name,belongSide )
		self[id] = m
		self.updateGCZMemberDataToOtherClient(m)
		self.receiveGCZOtherMemberData(m)

	def addMemberKillEnemyNum( self, id):
		"""
		增加成员击杀数
		"""
		if id in self:
			self[id].addMemberKillEnemyNum()
			self.updateGCZKillEnemyDataToClient( self[id] )

	def addMemberDeadNum( self, id ):
		"""
		增加成员死亡数
		"""
		if id in self:
			self[id].addMemberDeadNum()
			self.updateGCZDeadDataToClient( self[id] )

	def addMemberAssistsNum( self, id ):
		"""
		增加成员助攻数
		"""
		if id in self:
			self[id].addMemberAssistsNum()
			self.updateGCZAssistsDataToClient( self[id] )

	def addMemberKillSoldierNum( self, id ):
		"""
		增加成员击杀士兵数
		"""
		if id in self:
			self[id].addMemberKillSoldierNum()
			self.updateGCZKillSoldierDataToClient( self[id] )

	def addMemberSoldierDeadNum( self, id ):
		"""
		增加成员的士兵死亡数
		"""
		if id in self:
			self[id].addMemberSoldierDeadNum()
			self.upDateGCZMemberSoldierDeadNumToClient( self[id] )

	def getIDByEntityID( self, entityID ):
		"""
		通过entityID 获得ID
		"""
		for m in self.values():
			if m.roleID == entityID:
				return m.roleDBID
		return None

	def getMemberByName( self, name ):
		"""
		通过名字判断是否已经成员内
		"""
		for m in self.values():
			if m.roleName == name:
				return m

		return None

	def updateGCZMemberDataToOtherClientOnLogin( self, srcMemberID, dstMemberID ):
		"""
		"""
		members = self.getMembersBySide( csdefine.BELONG_SIDE_ATTACK )
		for m in members:
			if m.roleMB and m.roleID != dstMemberID and m.roleMB.getClient():
				m.roleMB.client.CLIENT_UpdateGCZMemberDataToOtherClientOnLogin( srcMemberID, dstMemberID )

	def updateGCZMemberDataToOtherClient( self, member ):
		"""
		更新自己的成员数据到其他客户端
		"""
		name = ""
		enemyName = ""
		if member.belongSide == csdefine.BELONG_SIDE_ATTACK:
			name = self.attackName
			enemyName = self.protectName
		else:
			name = self.protectName
			enemyName = self.attackName
		members = self.getMembersBySide( csdefine.BELONG_SIDE_ATTACK )
		for m in members:
			if m.roleMB and m.roleMB.getClient():
				m.roleMB.client.CLIENT_UpdateGCZMemberDataToOtherClient( member.roleID, member.roleName, member.belongSide, member.killEnemy, member.dead, member.assists,member.killSoldier,member.totalGetExploit,name,member.ownerSoldierDeadNum,enemyName )

	def receiveGCZOtherMemberData( self, member ):
		"""
		接受其他成员数据
		"""
		for m in self.values():
			name = ""
			enemyName = ""
			if m.belongSide == csdefine.BELONG_SIDE_ATTACK:
				name = self.attackName
				enemyName = self.protectName
			else:
				name = self.protectName
				enemyName = self.attackName
			if member.roleMB and member.roleMB.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE and member.roleMB.getClient():
				member.roleMB.client.CLIENT_ReceiveGCZOtherMemberData( m.roleID, m.roleName, m.belongSide, m.killEnemy, m.dead, m.assists,m.killSoldier,m.totalGetExploit,name,m.ownerSoldierDeadNum,enemyName )

	def updateGCZKillEnemyDataToClient( self, member ):
		"""
		更新击杀敌人数据到客户端
		"""
		members = self.getMembersBySide( csdefine.BELONG_SIDE_ATTACK )
		for m in members:
			if m.roleMB and m.roleMB.getClient():
				m.roleMB.client.CLIENT_UpdateGCZKillEnemyDataToClient( member.roleID, member.killEnemy )

	def updateGCZKillSoldierDataToClient( self, member ):
		"""
		更新击杀士兵数据到客户端
		"""
		members = self.getMembersBySide( csdefine.BELONG_SIDE_ATTACK )
		for m in members:
			if m.roleMB and m.roleMB.getClient():
				m.roleMB.client.CLIENT_UpdateGCZKillSoldierDataToClient( member.roleID, member.killSoldier )

	def updateGCZDeadDataToClient( self, member ):
		"""
		更新死亡数据到客户端
		"""
		members = self.getMembersBySide( csdefine.BELONG_SIDE_ATTACK )
		for m in members:
			if m.roleMB and m.roleMB.getClient():
				m.roleMB.client.CLIENT_UpdateGCZDeadDataToClient( member.roleID, member.dead )

	def updateGCZAssistsDataToClient( self, member ):
		"""
		更新助攻数据到客户端
		"""
		members = self.getMembersBySide( csdefine.BELONG_SIDE_ATTACK )
		for m in members:
			if m.roleMB and m.roleMB.getClient():
				m.roleMB.client.CLIENT_UpdateGCZAssistsDataToClient( member.roleID, member.assists )

	def updateGCZTotalGetExploitDataToClient( self, member ):
		"""
		更新军功数据到客户端
		"""
		members = self.getMembersBySide( csdefine.BELONG_SIDE_ATTACK )
		for m in members:
			if m.roleMB and m.roleMB.getClient():
				m.roleMB.client.CLIENT_UpdateGCZTotalExploitDataToClient( member.roleID, member.totalGetExploit )

	def upDateGCZMemberSoldierDeadNumToClient( self, member ):
		"""
		更新己方士兵死亡数据到客户端
		"""
		members = self.getMembersBySide( csdefine.BELONG_SIDE_ATTACK )
		for m in members:
			if m.roleMB and m.roleMB.getClient():
				m.roleMB.client.CLIENT_UpDateGCZMemberSoldierDeadNumToClient( member.roleID,member.ownerSoldierDeadNum )

	def getMembersBySide( self, side ):
		"""
		获得某一方的成员
		"""
		members = []
		for m in self.values():
			if m.belongSide == side:
				members.append( m )
		return members

	def getDictFromObj( self, obj ):
		tempDict = {}
		tempDict[ "members" ] = []
		tempDict["protectName"] = obj.protectName
		tempDict["attackName"] = obj.attackName
		for mObj in obj.values():
			tempDict[ "members" ].append( mObj )
			
		return tempDict
	
	def createObjFromDict( self, dict ):
		obj = GCZMemberInfoMgr()
		obj.initData( dict )
		return obj
		
	def isSameType( self, obj ):
		return isinstance( obj, GCZMemberInfoMgr )

g_GCZMemberInfoMgr = GCZMemberInfoMgr()
