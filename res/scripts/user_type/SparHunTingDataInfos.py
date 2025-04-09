# -*- coding: utf-8 -*-

import KBEDebug
import json
from BattlefieldMember import BattlefieldMember
import csstatus
import csdefine
import Const
import KBEngine

class SparHunTingMemberInfMgr( dict ):
	"""
	晶石狩猎场 成员数据管理器
	"""
	def __init__( self ):
		pass
	
	def initData( self, dict ):
		for m  in dict[ "members" ]:
			self[ m.roleID ] = m
			
	def add( self, roleMB,integral = 0,money = 0, kill = 0, beKill = 0 ):
		m = None
		if roleMB.id not in self.keys():
			m = BattlefieldMember( roleMB.id,roleMB.getName(),roleMB.playerDBID,roleMB,integral,money,kill,beKill)
			self[ roleMB.id ] = m
		else:
			m = self[roleMB.id]
			m.roleMB = roleMB
		
		self.updateMoneyDataToOtherClient(m)
		self.receiveOtherMoneyData(m)
		self.updateIntegralDataToOtherClient(m)
		self.receiveOtherIntegralData(m)
		self.updateBeKillDataToOtherClient(m)
		self.receiveOtherBeKillData(m)
		self.updateKillDataToOtherClient(m)
		self.receiveOtherKillData(m)

	def remove( self, playerMB, flag = True	):
		if playerMB.id in self.keys():
			if not flag: 
				self[playerMB.id].roleMB = None
				return
			
			del self[ playerMB.id ]
			for m in self.values():
				if m.roleMB:
					m.roleMB.client.CLIENT_HunTingMemberLeave(playerMB.id)
	
	def addIntegral( self, roleID, integral ):
		if roleID in self.keys():
			m = self[ roleID ]
			m.addIntegral( integral )
			self.updateIntegralDataToOtherClient(m)
	
	def decIntegral( self, roleID, integral ):
		if roleID in self.keys():
			m = self[ roleID ]
			m.decIntegral( integral )
			self.updateIntegralDataToOtherClient(m)

	def addMoney( self, roleID, money ):
		if roleID in self.keys():
			m = self[ roleID ]
			m.addMoney(money)
			self.updateMoneyDataToOtherClient(m)
	
	def getIntegral( self, roleID ):
		if roleID in self.keys():
			return self[ roleID ].integral
			
		return 0

	def kill( self, diePlayerID, killerID ):
		"""
		"""
		killEntity = KBEngine.entities.get(killerID,None)
		if not killEntity:
			return
		if killEntity.getEntityFlag() == csdefine.ENTITY_FLAG_MONSTER:
			return
		if killEntity.getEntityFlag() == csdefine.ENTITY_FLAG_VEHICLEPET:
			killEntity = killEntity.getOwnerEntity()
		if not killEntity and killEntity.getEntityFlag() != csdefine.ENTITY_FLAG_ROLE:
			return
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
			self.updateBeKillDataToOtherClient( m )
			self.checkBeKillNum(m)
			n.onKill()
			self.updateKillDataToOtherClient( n )
			self.checkKillNum(n,campStr)
			self.checkFirstKill(n,campStr)

	def updateMoneyDataToOtherClient( self, member ):
		"""
		更新金钱数据到客户端 (包括自己)
		"""
		for m in self.values():
			if m.roleMB and member.roleMB and m.roleMB.getClient():
				m.roleMB.client.CLIENT_UpdateMoneyDataToOtherPlayer( member.roleID,member.money,member.roleName,member.roleMB.getCamp(),member.roleMB.getProfession(),member.roleMB.getLevel() )

	def receiveOtherMoneyData( self, member ):
		"""
		接收其他玩家的金钱数据 (包括自己)
		"""
		for m in self.values():
			if m.roleMB and member.roleMB and member.roleMB.getClient():
				member.roleMB.client.CLIENT_ReceiveOtherMoneyData( m.roleID,m.money,m.roleName,m.roleMB.getCamp(),m.roleMB.getProfession(),m.roleMB.getLevel() )

	def updateIntegralDataToOtherClient( self, member ):
		"""
		更新积分(金精)数据到客户端(包括自己)
		"""
		for m in self.values():
			if m.roleMB and member.roleMB and m.roleMB.getClient():
				m.roleMB.client.CLIENT_UpdateIntegralDataToOtherClient( member.roleID, member.integral )

	def receiveOtherIntegralData( self, member ):
		"""
		接收其他玩家的积分(金精)数据 (包括自己)
		"""
		for m in self.values():
			if m.roleMB and member.roleMB and member.roleMB.getClient():
				member.roleMB.client.CLIENT_ReceiveOtherIntegralData( m.roleID, m.integral )

	def updateBeKillDataToOtherClient( self, member ):
		"""
		更新其他玩家被击杀的数据到客户端( 包括自己 )
		"""
		for m in self.values():
			if m.roleMB and member.roleMB and m.roleMB.getClient():
				m.roleMB.client.CLIENT_UpdateBeKillDataToOtherClient( member.roleID, member.beKill )

	def receiveOtherBeKillData( self, member ):
		"""
		接收其他玩家被击杀的数据
		"""
		for m in self.values():
			if m.roleMB and member.roleMB and member.roleMB.getClient():
				member.roleMB.client.CLIENT_ReceiveOtherBeKillData( m.roleID, m.beKill )

	def updateKillDataToOtherClient( self, member ):
		"""
		更新其他玩家击杀的数据到客户端( 包括自己 )
		"""
		for m in self.values():
			if m.roleMB and member.roleMB and m.roleMB.getClient():
				m.roleMB.client.CLIENT_UpdateKillDataToOtherClient( member.roleID, member.kill )

	def receiveOtherKillData( self, member ):
		"""
		接收其他玩家击杀的数据
		"""
		for m in self.values():
			if m.roleMB and member.roleMB and member.roleMB.getClient():
				member.roleMB.client.CLIENT_ReceiveOtherKillData( m.roleID, m.kill )

	def checkKillNum( self, killer, campStr ):
		"""
		检查连续击杀次数
		"""
		num = killer.getKillNum()
		if num < 10:
			return
		killerName = killer.roleName
		for m in self.values():
			if m.roleMB:
				m.roleMB.statusMessage( csstatus.SPARHUNTING_GOD_LIKE,campStr,killerName )
				m.roleMB.showMessagePlaySound(Const.KILL_VOICE)
				if m.roleMB.getClient():
					m.roleMB.client.CLIENT_OnGodLike(killerName)

	def checkFirstKill( self, killer,campStr ):
		"""
		检查是否首杀
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
				if m.roleMB:
					m.roleMB.statusMessage( csstatus.SPARHUNTING_KILL_FIRST, campStr,killerName )
					m.roleMB.showMessagePlaySound(Const.KILL_VOICE)
					if m.roleMB.getClient():
						m.roleMB.client.CLIENT_OnFirstKill(killerName)

	def checkKillGodPlayer( self, killer, diePlayer,campStr ):
		"""
		检查是否击杀超神玩家
		"""
		dieKillNum = diePlayer.getKillNum()
		if dieKillNum >= 10:
			for m in self.values():
				if m.roleMB:
					m.roleMB.statusMessage( csstatus.SPARHUNTING_KILL_GOD_PLAYER,campStr,killer.roleName, diePlayer.roleName )

	def checkBeKillNum( self, diePlayer ):
		"""
		检查被连续击杀的次数
		"""
		bekillNum = diePlayer.getBeKillNum()
		if bekillNum >= 5:
			diePlayer.roleMB.statusMessage( csstatus.SPARHUNTING_FIVE_BKILL )
			diePlayer.roleMB.addBuff(diePlayer.roleMB, 12058708) # 连续死亡5以上 获得Buff加持

	def getThreeTopMemberNamesByMoney( self ):
		"""
		获得金钱榜前3的名称
		"""
		tempDict = {}
		rankList = []
		arrayName = []
		for m in self.values():
			tempDict[m.roleID] = m.money
		rankList.extend(sorted( tempDict.items(), key = lambda s:s[1], reverse = True ) )
		for rank in rankList[0:3]:
			arrayName.append( self[rank[0]].roleName )
		return arrayName

	def getAllMembers( self ):
		return self.values()

	def getCampMembers( self, camp ):
		result = []
		for m in self.values():
			if m.roleMB and m.roleMB.getCamp() == camp:
				result.append(m)
		return result
	
	def getDictFromObj( self, obj ):
		tempDict = {}
		tempDict[ "members" ] = []
		
		for mObj in obj.values():
			tempDict[ "members" ].append( mObj )
			
		return tempDict
	
	def createObjFromDict( self, dict ):
		obj = SparHunTingMemberInfMgr()
		obj.initData( dict )
		return obj
		
	def isSameType( self, obj ):
		return isinstance( obj, SparHunTingMemberInfMgr )

g_sparHunTingMemberInfMgr = SparHunTingMemberInfMgr()