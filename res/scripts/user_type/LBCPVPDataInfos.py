# -*- coding: utf-8 -*-

import KBEDebug
import json
from YXLMMember import YXLMMember
import csstatus
import ItemTypeEnum
import csdefine

class LBCPVPMemberMgr( dict ):
	"""
	高级练兵场PVP 成员数据管理器
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
			roleMB.jade = 0
			del self[roleMB.id]
			self.clearYXLMMemberData(roleMB)

	def clearYXLMMemberData(self, roleMB):
		"""
		清除玩家客户端数据
		"""
		if roleMB:
			roleMB.client.ClearYXLMMemberData()

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

	def die(self, deadID):
		"""
		"""
		if deadID in self.keys():
			d = self[deadID]
			d.onDie()
			self.updateYXLMBeKillDataToOtherClient(d)

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

	def setWinCamp( self, belongSide, winStatusID, loseStatusID , rewardExp, failRewardExp, declarePlayerName, occupyPlayerName, trainGroundName):
		"""
		"""
		camp = csdefine.CAMP_TAOSIM  if belongSide == csdefine.BELONG_SIDE_ATTACK  else csdefine.CAMP_DEMON
		for member in self.getAllMembers():
			r = member.roleMB
			#胜利方
			if r.getBelongSide() == belongSide:
				#客户端接口需要新写一个 或者修改原接口 这里暂时取巧一下 如果是进攻方胜利就传仙道阵营，如果是防守方胜利就传魔道阵营
				r.client.CLIENT_ShowYXLMBattlefieldWin(camp, rewardExp)
				r.statusMessage(winStatusID,"")
				
				#进攻方胜利
				if r.getBelongSide() == csdefine.BELONG_SIDE_ATTACK:
					r.statusMessage(csstatus.GROUND_ATTACK_SUCCESS, declarePlayerName, trainGroundName)
				#防守方胜利
				else:
					r.statusMessage(csstatus.GROUND_DEFENSE_SUCCESS, occupyPlayerName, trainGroundName)
			#失败方
			else:
				r.client.CLIENT_ShowYXLMBattlefieldWin(camp, failRewardExp)
				r.statusMessage(loseStatusID, "")
				#进攻方失败
				if r.getBelongSide() == csdefine.BELONG_SIDE_ATTACK:
					r.statusMessage(csstatus.GROUND_ATTACK_FAIL, trainGroundName)
				#防守方失败
				else:
					r.statusMessage(csstatus.GROUND_DEFENSE_FAIL, trainGroundName)


	def updateYXLMMemberDataToOtherClient( self, member ):
		"""
		更新自己成员数据到其他客户端
		"""
		itemInsList = member.roleMB.getItemListByKBType(ItemTypeEnum.BAG_SPACE_COPY_YXLM1)
		itemIDList = []
		for itemIns in itemInsList:
			itemIDList.append( itemIns.id )
		camp = csdefine.CAMP_TAOSIM if member.roleMB.getBelongSide()==csdefine.BELONG_SIDE_ATTACK else csdefine.CAMP_DEMON
		for m in self.values():
			if m.roleMB and member.roleMB and m.roleMB.getClient():
				m.roleMB.client.CLIENT_UpdateYXLMMemberDataToOtherClient(member.roleID, member.roleName, camp, member.kill,member.beKill,itemIDList )

	def receiveYXLMOtherMemberData( self, member ):
		"""
		接收其他玩家的成员数据
		"""
		for m in self.values():
			itemInsList = m.roleMB.getItemListByKBType(ItemTypeEnum.BAG_SPACE_COPY_YXLM1)
			itemIDList = []
			for itemIns in itemInsList:
				itemIDList.append( itemIns.id )
			
			camp = csdefine.CAMP_TAOSIM if m.roleMB.getBelongSide()==csdefine.BELONG_SIDE_ATTACK else csdefine.CAMP_DEMON
			if member.roleMB and member.roleMB and member.roleMB.getClient():
				member.roleMB.client.CLIENT_ReceiveYXLMOtherMemberData(m.roleID, m.roleName, camp, m.kill, m.beKill, itemIDList)

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

	def getMembersByCamp( self, belongSide ):
		"""
		通过Camp获得成员列表
		"""
		memberList = []
		for member in self.values():
			if member.roleMB and member.roleMB.getBelongSide() == belongSide:
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
		obj = LBCPVPMemberMgr()
		obj.initData( dict )
		return obj
		
	def isSameType( self, obj ):
		return isinstance( obj, LBCPVPMemberMgr )

g_YXLMMemberInfMgr = LBCPVPMemberMgr()