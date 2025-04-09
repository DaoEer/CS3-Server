# -*- coding: utf-8 -*-

import KBEDebug
import json
from YXLMMember import YXLMMember
import csstatus
import ItemTypeEnum
import csdefine

class YXLMMemberMgr( dict ):
	"""
	英雄联盟 成员数据管理器
	"""
	def __init__( self ):
		pass
	
	def initData( self, dict ):
		for m  in dict[ "members" ]:
			self[ m.roleID ] = m
			
	def add( self, roleMB,integral = 0,money = 0, kill = 0, beKill = 0, ):
		member = self.getMemberByPlayerDBID( roleMB.playerDBID )
		if member:
			del self[member.roleID]
			srcMemberID = member.roleID
			roleMB.addJade( member.roleJade )
			member.roleID = roleMB.id
			member.roleMB = roleMB
			self[roleMB.id] = member
			self.updateMemberDataToOtherMemberOnLogin( srcMemberID,member.roleID )
			self.receiveYXLMOtherMemberData(member)
			return

		m = YXLMMember( roleMB.id,roleMB.getName(),roleMB.playerDBID,roleMB )
		self[roleMB.id] = m
		self.updateYXLMMemberDataToOtherClient(m)
		self.receiveYXLMOtherMemberData(m)

	def remove( self, roleMB ):
		"""
		"""
		if roleMB.id in self.keys():
			del self[roleMB.id]

	def updateMemberDataToOtherMemberOnLogin( self, srcMemberID, dstMemberID ):
		"""
		"""
		for m in self.values():
			if m.roleMB and m.roleID != dstMemberID and m.roleMB.getClient():
				m.roleMB.client.CLIENT_UpdateYXLMMemberDataToOtherOnLogin( srcMemberID, dstMemberID  )
	
	def kill( self, diePlayerID, killerID ):
		"""
		"""
		if diePlayerID in self.keys() and killerID in self.keys():
			m = self[diePlayerID]
			n = self[killerID]
			self.checkKillGodPlayer( n, m )
			m.onDie()
			n.onKill()
			self.updateYXLMKillDataToOtherClient( n )
			self.updateYXLMBeKillDataToOtherClient(m)
			self.checkKillNum(n)
			if self.checkFirstKill(n):
				for m in self.values():
					if m.roleMB.getClient():
						m.roleMB.client.CLIENT_OnFirstKill(n.roleName)

	def onAddItem( self, playerMB, itemID ):
		"""
		增加物品
		"""
		if playerMB.id in self.keys():
			member = self[playerMB.id]
			self.updateYXLMAddItemToOtherClient( member, itemID )

	def onRemoveItem( self, playerMB, itemID ):
		"""
		移除物品
		"""
		if playerMB.id in self.keys():
			member = self[playerMB.id]
			self.updateYXLMRemoveItemToOtherClient( member, itemID )

	def setWinCamp( self, camp, winStatusID, loseStatusID , zyjjRewardDatas):
		"""
		"""
		winMemberList = self.getMembersByCamp(camp)
		if camp == csdefine.CAMP_TAOSIM:
			loseMemberList = self.getMembersByCamp(csdefine.CAMP_DEMON)
		else:
			loseMemberList = self.getMembersByCamp( csdefine.CAMP_TAOSIM )
		for member in winMemberList:
			if member.roleMB and member.roleMB.getClient():
				#显示阵营竞技结算奖励
				member.roleMB.client.ShowZYJJReward(zyjjRewardDatas[member.roleMB.playerDBID])
				member.roleMB.client.CLIENT_ShowYXLMBattlefieldWin( camp, 0  )
		for member in loseMemberList:
			if member.roleMB and member.roleMB.getClient():
				#显示阵营竞技结算奖励
				member.roleMB.client.ShowZYJJReward(zyjjRewardDatas[member.roleMB.playerDBID])
				member.roleMB.client.CLIENT_ShowYXLMBattlefieldWin( camp, 0  )
		
		if winStatusID:
			winMemberList = self.getMembersByCamp(camp)
			for member in winMemberList:
				member.roleMB.statusMessage( winStatusID,"" )
		if not loseStatusID:
			return
		for loseMember in loseMemberList:
			loseMember.roleMB.statusMessage( loseStatusID,"" )
		

	def updateYXLMMemberDataToOtherClient( self, member ):
		"""
		更新自己成员数据到其他客户端
		"""
		itemInsList = member.roleMB.getItemListByKBType(ItemTypeEnum.BAG_SPACE_COPY_YXLM1)
		itemIDList = []
		for itemIns in itemInsList:
			itemIDList.append( itemIns.id )
		for m in self.values():
			if m.roleMB and member.roleMB and m.roleMB.getClient():
				m.roleMB.client.CLIENT_UpdateYXLMMemberDataToOtherClient(member.roleID, member.roleName, member.roleMB.getCamp(),member.kill,member.beKill,itemIDList )

	def receiveYXLMOtherMemberData( self, member ):
		"""
		接收其他玩家的成员数据
		"""
		for m in self.values():
			itemInsList = m.roleMB.getItemListByKBType(ItemTypeEnum.BAG_SPACE_COPY_YXLM1)
			itemIDList = []
			for itemIns in itemInsList:
				itemIDList.append( itemIns.id )
			if member.roleMB and member.roleMB and member.roleMB.getClient():
				member.roleMB.client.CLIENT_ReceiveYXLMOtherMemberData( m.roleID, m.roleName, m.roleMB.getCamp(),m.kill,m.beKill,itemIDList  )

	def updateYXLMKillDataToOtherClient( self, member ):
		"""
		更新其他玩家击杀的数据到客户端( 包括自己 )
		"""
		for m in self.values():
			if m.roleMB and member.roleMB and m.roleMB.getClient():
				m.roleMB.client.CLIENT_UpdateYXLMKillDataToOtherClient( member.roleID, member.kill )

	def updateYXLMBeKillDataToOtherClient( self, member ):
		"""
		更新其他玩家被击杀的数据到客户端( 包括自己 )
		"""
		for m in self.values():
			if m.roleMB and member.roleMB and m.roleMB.getClient():
				m.roleMB.client.CLIENT_UpdateYXLMBeKillDataToOtherClient( member.roleID, member.beKill )

	def updateYXLMAddItemToOtherClient( self, member, itemID ):
		"""
		更新其他玩家获得物品的数据到客户端( 包括自己 )
		"""
		for m in self.values():
			if m.roleMB and member.roleMB and m.roleMB.getClient():
				m.roleMB.client.CLIENT_UpdateYXLMAddItemToOtherClient( member.roleID, itemID )

	def updateYXLMRemoveItemToOtherClient( self, member, itemID ):
		"""
		更新其他玩家移除物品的数据到客户端( 包括自己 )
		"""
		for m in self.values():
			if m.roleMB and member.roleMB and m.roleMB.getClient():
				m.roleMB.client.CLIENT_UpdateYXLMRemoveItemToOtherClient( member.roleID, itemID )

	def checkKillGodPlayer( self, killer, diePlayer ):
		"""
		检查是否击杀超神玩家
		"""
		dieKillNum = diePlayer.getKillNum()
		if dieKillNum >= 7:
			for m in self.values():
				if m.roleMB.getClient():
					m.roleMB.client.CLIENT_OnEndLegendary(killer.roleName)

	def checkFirstKill( self, killer ):
		"""
		检查是否为首杀
		"""
		isFirstKill = True
		if killer.kill == 1:
			for m in self.values():
				if killer.roleID != m.roleID and m.kill != 0:
					isFirstKill = False
					break
		else:
			isFirstKill = False
		return isFirstKill

	def checkKillNum( self, killer ):
		"""
		检查连续击杀次数
		"""
		num = killer.getKillNum()
		msgID = 0
		if num == 3:
			pass
			#msgID = csstatus.SPARHUNTING_GOD_LIKE
		elif num == 5:
			pass
		elif num >= 7:
			for m in self.values():
				if m.roleMB.getClient():
					m.roleMB.client.CLIENT_OnGodLike( killer.roleName )

	def getAllMembers( self ):
		allMembers = []
		for member in self.values():
			if member.roleMB:
				allMembers.append(member)
		return allMembers

	def getMembersByCamp( self, camp ):
		"""
		通过Camp获得成员列表
		"""
		memberList = []
		for member in self.values():
			if member.roleMB and member.roleMB.getCamp() == camp:
				memberList.append(member)

		return memberList

	def getMemberByPlayerDBID( self, playerDBID ):
		"""
		通过DBID获得成员数据
		"""
		for member in self.values():
			if member.roleDBID == playerDBID:
				return member

		return None

	def getMembersAllKillNumberByCamp( self, camp ):
		"""
		"""
		memberList = self.getMembersByCamp( camp )
		killNum = 0
		for member in memberList:
			killNum += member.kill

		return killNum

	def getMembersAllJadeValueByCamp( self, camp ):
		"""
		"""
		memberList = self.getMembersByCamp( camp )
		jadeValue = 0
		for member in memberList:
			jadeValue +=member.roleMB.jade
		return jadeValue

	def getDictFromObj( self, obj ):
		tempDict = {}
		tempDict[ "members" ] = []
		
		for mObj in obj.values():
			tempDict[ "members" ].append( mObj )
			
		return tempDict
	
	def createObjFromDict( self, dict ):
		obj = YXLMMemberMgr()
		obj.initData( dict )
		return obj
		
	def isSameType( self, obj ):
		return isinstance( obj, YXLMMemberMgr )

g_YXLMMemberInfMgr = YXLMMemberMgr()