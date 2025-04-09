# -*- coding: utf-8 -*-

import KBEDebug
import json
from BattlefieldMember import BattlefieldMember
import csstatus
import csdefine

class YeZhanFengQiMemberMgr( dict ):
	"""
	血斗凤栖镇 成员数据管理器
	"""
	def __init__( self ):
		pass
	
	def initData( self, dict ):
		for m  in dict[ "members" ]:
			self[ m.roleID ] = m
			
	def add( self, roleMB,integral = 0,money = 0, kill = 0, beKill = 0 ):
		member = self.getMemberByPlayerDBID( roleMB.playerDBID )
		if member:
			del self[member.roleID]
			srcMemberID = member.roleID
			member.roleID = roleMB.id
			member.roleMB = roleMB
			self[roleMB.id] = member
			self.updateMemberDataToOtherMemberOnLogin( srcMemberID, member.roleID )
			self.receiveFengQiOtherMemberData(member)
			return
		m = BattlefieldMember( roleMB.id,roleMB.getName(),roleMB.playerDBID,roleMB,integral,money,kill,beKill)
		self[ roleMB.id ] = m
		self.updateFengQiMemberDataToOtherClient(m)
		self.receiveFengQiOtherMemberData(m)
		self.updateFengQiIntegralToOtherClient(m)
		self.updateFengQiKillDataToOtherClient(m)

	def remove( self, playerMB ):
		if playerMB.id in self.keys():
			del self[ playerMB.id ]
			for m in self.values():
				if m.roleMB.getClient():
					m.roleMB.client.CLIENT_FengQiMemberLeave(playerMB.id)
	
	def getIntegral( self, roleID ):
		if roleID in self.keys():
			return self[ roleID ].integral
			
		return 0

	def kill( self, diePlayerID, killerID ):
		"""
		"""
		if diePlayerID in self.keys() and killerID in self.keys():
			m = self[diePlayerID]
			n = self[killerID]
			campStr = ""
			if n.roleMB.getCamp() == csdefine.CAMP_TAOSIM:
				campStr = "仙道"
			if n.roleMB.getCamp() == csdefine.CAMP_DEMON:
				campStr = "魔道"
			self.checkKillGodPlayer( n, m, campStr )
			m.onDie()
			n.onKill()
			self.updateFengQiKillDataToOtherClient( n )
			self.checkKillNum(n,campStr)
			self.checkFirstKill(n,campStr)


	def addIntegral( self, roleID, integral ):
		if roleID in self.keys():
			m = self[ roleID ]
			m.addIntegral( integral )
			self.updateFengQiIntegralToOtherClient(m)
	
	def decIntegral( self, roleID, integral ):
		if roleID in self.keys():
			m = self[ roleID ]
			m.decIntegral( integral )
			self.updateFengQiIntegralToOtherClient(m)
			if self.getIntegral( roleID ) == 0:
				m.roleMB.fengQiMemberOut()

	def updateMemberDataToOtherMemberOnLogin( self, srcMemberID, dstMemberID ):
		"""
		"""
		for m in self.values():
			if m.roleMB and m.roleID != dstMemberID and m.roleMB.getClient():
				m.roleMB.client.CLIENT_UpdateFengQiMemberDataToOtherOnLogin( srcMemberID, dstMemberID )

	def updateFengQiMemberDataToOtherClient( self, member ):
		"""
		更新自己成员数据到其他客户端
		"""
		for m in self.values():
			if m.roleMB and member.roleMB and m.roleMB.getClient():
				m.roleMB.client.CLIENT_UpdateFengQiMemberDataToOtherClient(member.roleID, member.integral, member.roleName, member.roleMB.getProfession(),member.kill )

	def receiveFengQiOtherMemberData( self, member ):
		"""
		接收其他玩家的成员数据
		"""
		for m in self.values():
			if m.roleMB and member.roleMB and member.roleMB.getClient():
				member.roleMB.client.CLIENT_ReceiveFengQiOtherMemberData( m.roleID, m.integral, m.roleName, m.roleMB.getProfession(), m.kill )

	def updateFengQiIntegralToOtherClient( self, member ):
		"""
		更新积分数据到客户端(包括自己)
		"""
		for m in self.values():
			if m.roleMB and member.roleMB and m.roleMB.getClient():
				m.roleMB.client.CLIENT_UpdateFengQiIntegralToOtherClient( member.roleID, member.integral )

	def updateFengQiKillDataToOtherClient( self, member ):
		"""
		更新其他玩家击杀的数据到客户端( 包括自己 )
		"""
		for m in self.values():
			if m.roleMB and member.roleMB and m.roleMB.getClient():
				m.roleMB.client.UpdateFengQiKillDataToOtherClient( member.roleID, member.kill )

	def checkKillGodPlayer( self, killer, diePlayer, campStr ):
		"""
		检查是否击杀超神玩家
		"""
		dieKillNum = diePlayer.getKillNum()
		if dieKillNum >= 10:
			for m in self.values():
				if m.roleMB and m.roleMB.getClient():
					m.roleMB.statusMessage( csstatus.SPARHUNTING_KILL_GOD_PLAYER,campStr,killer.roleName, diePlayer.roleName )
					m.roleMB.client.OnEndLegendary(diePlayer.roleName)

	def checkFirstKill( self, killer, campStr ):
		"""
		检查是否为首杀
		"""
		isFirstKill = True
		if killer.kill == 1:
			for m in self.values():
				if killer.roleID != m.roleID and m.kill != 0:
					isFirstKill = False
		else:
			isFirstKill = False

		if isFirstKill:
			killerName = killer.roleName
			for m in self.values():
				if m.roleMB and m.roleMB.getClient():
					m.roleMB.statusMessage( csstatus.SPARHUNTING_KILL_FIRST, campStr,killerName )
					m.roleMB.client.CLIENT_OnFirstKill(killerName)

	def checkKillNum( self, killer,campStr ):
		"""
		检查连续击杀次数
		"""
		num = killer.getKillNum()
		if num < 10:
			return
		killerName = killer.roleName
		for m in self.values():
			if m.roleMB and m.roleMB.getClient():
				m.roleMB.statusMessage( csstatus.SPARHUNTING_GOD_LIKE,campStr,killerName )
				m.roleMB.client.CLIENT_OnGodLike(killerName)

	def getAllMembers( self ):
		return self.values()

	def getMembersByJoinNumber( self, joinNumber ):
		memberList =  sorted( self.values(), key = lambda m : m.integral, reverse = True )
		if memberList > joinNumber:
			return memberList[0:joinNumber]
		return memberList

	def getMemberByPlayerDBID( self, playerDBID ):
		"""
		获得成员 通过玩家的DBID
		"""
		for member in self.values():
			if member.roleDBID == playerDBID:
				return member
		return None

	def getFirstMember( self ):
		"""
		获得第一名
		"""
		memberList =  sorted( self.values(), key = lambda m : m.integral, reverse = True )
		if len(memberList):
			return memberList[0]
		return None
	
	def getDictFromObj( self, obj ):
		tempDict = {}
		tempDict[ "members" ] = []
		
		for mObj in obj.values():
			tempDict[ "members" ].append( mObj )
			
		return tempDict
	
	def createObjFromDict( self, dict ):
		obj = YeZhanFengQiMemberMgr()
		obj.initData( dict )
		return obj
		
	def isSameType( self, obj ):
		return isinstance( obj, YeZhanFengQiMemberMgr )

g_yeZhanFengQiMemberInfMgr = YeZhanFengQiMemberMgr()